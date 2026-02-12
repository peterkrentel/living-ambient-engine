"""
YouTube Video Uploader - Generative Ambient Art Engine
Uses YouTube Data API v3 for automated video publishing.

Setup:
1. Create Google Cloud project: https://console.cloud.google.com
2. Enable YouTube Data API v3
3. Create OAuth2 credentials (Desktop app)
4. Download client_secrets.json to project root
5. Run once to authorize: python -m youtube.uploader --auth
"""

import os
import sys
import json
import pickle
import random
import time
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime

# Google API imports (will be installed via requirements)
try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False


SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.readonly',  # For listing channel videos
    'https://www.googleapis.com/auth/yt-analytics.readonly'
]
TOKEN_FILE = os.environ.get('YOUTUBE_TOKEN_FILE', 'youtube_token.pickle')
CLIENT_SECRETS_FILE = 'client_secrets.json'

# Retry configuration
MAX_RETRIES = 5
INITIAL_BACKOFF = 1.0  # seconds
MAX_BACKOFF = 64.0  # seconds
RETRYABLE_STATUS_CODES = [500, 502, 503, 504]  # Server errors


class QuotaExceededError(Exception):
    """Raised when YouTube API quota is exceeded."""
    pass


class YouTubeUploader:
    """Upload videos to YouTube with metadata."""

    def __init__(self, client_secrets_path: str = CLIENT_SECRETS_FILE):
        if not GOOGLE_API_AVAILABLE:
            raise ImportError(
                "Google API libraries not installed. Run:\n"
                "pip install google-auth-oauthlib google-api-python-client"
            )
        self.client_secrets_path = client_secrets_path
        self.youtube = None
        self._is_ci = os.environ.get('GITHUB_ACTIONS') == 'true' or os.environ.get('CI') == 'true'

    def authenticate(self) -> bool:
        """Authenticate with YouTube API using OAuth2.

        In CI environments, requires pre-existing token file.
        Never attempts interactive authentication in CI.
        """
        creds = None

        # CI-safe: Fail fast if no token in CI environment
        if self._is_ci and not os.path.exists(TOKEN_FILE):
            raise FileNotFoundError(
                f"❌ CI Error: YouTube token not found at '{TOKEN_FILE}'.\n"
                "Make sure YOUTUBE_TOKEN_PICKLE secret is configured.\n"
                "Never attempt interactive authentication in CI."
            )

        # Load existing token
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)

        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            elif self._is_ci:
                # In CI, we can't get new credentials interactively
                raise RuntimeError(
                    "❌ CI Error: Token expired and cannot refresh.\n"
                    "Re-authenticate locally and update the YOUTUBE_TOKEN_PICKLE secret."
                )
            else:
                # Local interactive authentication
                if not os.path.exists(self.client_secrets_path):
                    raise FileNotFoundError(
                        f"Client secrets not found: {self.client_secrets_path}\n"
                        "Download from Google Cloud Console > APIs > Credentials"
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_path, SCOPES
                )
                creds = flow.run_local_server(port=8080)

            # Save token for future use
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)

        self.youtube = build('youtube', 'v3', credentials=creds)
        return True

    def _retry_with_backoff(self, operation_name: str, func, *args, **kwargs):
        """Execute function with exponential backoff on retryable errors.

        Args:
            operation_name: Human-readable name for logging
            func: Callable to execute
            *args, **kwargs: Arguments to pass to func

        Returns:
            Result of func()

        Raises:
            QuotaExceededError: If YouTube quota is exceeded
            HttpError: If non-retryable HTTP error occurs
            Exception: If max retries exceeded
        """
        last_exception = None

        for attempt in range(MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except HttpError as e:
                last_exception = e
                error_reason = str(e)

                # Check for quota exceeded (non-retryable)
                if e.resp.status == 403 and 'quotaExceeded' in error_reason:
                    raise QuotaExceededError(
                        "YouTube API daily quota exceeded.\n"
                        "Wait until quota resets (midnight Pacific Time) or request higher quota."
                    )

                # Check for retryable server errors
                if e.resp.status in RETRYABLE_STATUS_CODES:
                    if attempt < MAX_RETRIES - 1:
                        backoff = min(INITIAL_BACKOFF * (2 ** attempt), MAX_BACKOFF)
                        jitter = random.uniform(0, backoff * 0.1)
                        sleep_time = backoff + jitter
                        print(f"⚠️  {operation_name}: Server error {e.resp.status}, retrying in {sleep_time:.1f}s... (attempt {attempt + 1}/{MAX_RETRIES})")
                        time.sleep(sleep_time)
                        continue

                # Non-retryable HTTP error
                raise

            except (ConnectionError, TimeoutError, OSError) as e:
                # Network errors are retryable
                last_exception = e
                if attempt < MAX_RETRIES - 1:
                    backoff = min(INITIAL_BACKOFF * (2 ** attempt), MAX_BACKOFF)
                    jitter = random.uniform(0, backoff * 0.1)
                    sleep_time = backoff + jitter
                    print(f"⚠️  {operation_name}: Network error, retrying in {sleep_time:.1f}s... (attempt {attempt + 1}/{MAX_RETRIES})")
                    time.sleep(sleep_time)
                    continue
                raise

        raise Exception(f"{operation_name} failed after {MAX_RETRIES} retries: {last_exception}")
    
    def upload(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: list = None,
        category_id: str = "10",  # Music category
        privacy: str = "public",
        thumbnail_path: Optional[str] = None
    ) -> Dict:
        """
        Upload video to YouTube.
        
        Args:
            video_path: Path to MP4 file
            title: Video title
            description: Video description
            tags: List of tags
            category_id: YouTube category (10 = Music, 22 = People & Blogs)
            privacy: public, private, or unlisted
            thumbnail_path: Optional custom thumbnail
            
        Returns:
            Dict with video_id, url, title, and thumbnail_uploaded (bool)
        """
        if not self.youtube:
            self.authenticate()
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags or [],
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy,
                'selfDeclaredMadeForKids': False
            }
        }
        
        media = MediaFileUpload(
            video_path,
            mimetype='video/mp4',
            resumable=True,
            chunksize=1024*1024
        )
        
        # Upload video with retry logic
        request = self.youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )

        response = None
        last_progress = -1
        while response is None:
            # Use retry with backoff for each chunk
            status, response = self._retry_with_backoff(
                "Video chunk upload",
                request.next_chunk
            )
            if status:
                progress = int(status.progress() * 100)
                # Only print if progress changed (avoid spam)
                if progress != last_progress:
                    print(f"Uploading... {progress}%")
                    last_progress = progress

        video_id = response['id']
        video_url = f"https://youtube.com/watch?v={video_id}"
        print(f"✅ Video uploaded: {video_url}")

        # Upload thumbnail if provided (with retry)
        # Note: This requires YouTube account verification. If it fails, we'll continue without it.
        thumbnail_uploaded = False
        if thumbnail_path and os.path.exists(thumbnail_path):
            try:
                def upload_thumbnail():
                    return self.youtube.thumbnails().set(
                        videoId=video_id,
                        media_body=MediaFileUpload(thumbnail_path, mimetype='image/png')
                    ).execute()

                self._retry_with_backoff("Thumbnail upload", upload_thumbnail)
                thumbnail_uploaded = True
                print("✅ Custom thumbnail uploaded successfully")
            except QuotaExceededError:
                # Re-raise quota errors - caller needs to handle these
                raise
            except HttpError as e:
                # Thumbnail upload failed - this is usually due to account not being verified
                # or missing permissions (403 error). Continue without the custom thumbnail.
                print(f"⚠️  Warning: Could not upload custom thumbnail: {e}")
                print("   The video was uploaded successfully, but using YouTube's auto-generated thumbnail.")
                print("   To enable custom thumbnails, verify your YouTube account at:")
                print("   https://www.youtube.com/verify")
            except Exception as e:
                # Catch any other unexpected errors
                print(f"⚠️  Warning: Unexpected error uploading thumbnail: {e}")
                print("   The video was uploaded successfully, but using YouTube's auto-generated thumbnail.")

        return {
            'video_id': video_id,
            'url': video_url,
            'title': title,
            'thumbnail_uploaded': thumbnail_uploaded
        }

