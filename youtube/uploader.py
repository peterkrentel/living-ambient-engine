"""
YouTube Video Uploader - Content Factory
Uses YouTube Data API v3 for automated video publishing.

Setup:
1. Create Google Cloud project: https://console.cloud.google.com
2. Enable YouTube Data API v3
3. Create OAuth2 credentials (Desktop app)
4. Download client_secrets.json to project root
5. Run once to authorize: python -m youtube.uploader --auth
"""

import os
import json
import pickle
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime

# Google API imports (will be installed via requirements)
try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False


SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
TOKEN_FILE = 'youtube_token.pickle'
CLIENT_SECRETS_FILE = 'client_secrets.json'


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
        
    def authenticate(self) -> bool:
        """Authenticate with YouTube API using OAuth2."""
        creds = None
        
        # Load existing token
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
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
            Dict with video_id and url
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
        
        # Upload video
        request = self.youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploading... {int(status.progress() * 100)}%")
        
        video_id = response['id']
        video_url = f"https://youtube.com/watch?v={video_id}"
        
        # Upload thumbnail if provided
        if thumbnail_path and os.path.exists(thumbnail_path):
            self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path, mimetype='image/png')
            ).execute()
        
        return {
            'video_id': video_id,
            'url': video_url,
            'title': title
        }

