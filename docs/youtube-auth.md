# YouTube OAuth2 Authentication Guide

Getting YouTube uploads working is a pain. Here's what actually works.

## Prerequisites

- Google account
- Python 3.9+ with `google-auth-oauthlib` and `google-api-python-client`

## Step 1: Google Cloud Console Setup

1. Go to https://console.cloud.google.com
2. Create a new project (e.g., "living-ambient-engine")
3. Enable **YouTube Data API v3**: https://console.cloud.google.com/apis/library/youtube.googleapis.com
4. Enable **YouTube Analytics API** (needed for [`analytics-personal.yml`](../.github/workflows/analytics-personal.yml) / `fetch_analytics`, not only uploads): https://console.cloud.google.com/apis/library/youtubeanalytics.googleapis.com

## Step 2: OAuth Consent Screen (THE TRICKY PART)

1. Go to **APIs & Services → OAuth consent screen**
2. Choose **External** (unless you have Google Workspace)
3. Fill in app name, your email
4. **IMPORTANT:** Leave it in "Testing" mode (don't publish)
5. Click the **person icon** (👤) in the left sidebar → **Audience**
6. Add yourself as a **Test User** (your exact Gmail address)
7. **SAVE**

Without adding yourself as a test user, you'll get `403: access_denied` forever.

## Step 3: Create OAuth Credentials

1. Go to **APIs & Services → Credentials**
2. Click **Create Credentials → OAuth client ID**
3. Choose **Desktop app**
4. Download the JSON
5. Rename to `client_secrets.json` and put in project root

## Step 4: Run Local Auth

```bash
source venv/bin/activate
pip install google-auth-oauthlib google-api-python-client
python youtube_upload.py --auth
```

This opens a browser. **Use Chrome with the correct profile** (the one with your test user email).

You'll see "Google hasn't verified this app" - click:
1. **Advanced**
2. **Go to [App Name] (unsafe)**
3. **Continue/Allow**

**DON'T CLOSE THE BROWSER** until you see "Authentication successful" or it redirects to localhost.

The token saves to `youtube_token.pickle`.

## Step 5: GitHub Secrets

Encode and add to GitHub:

```bash
# Token (base64 encoded pickle file)
base64 -i youtube_token.pickle | tr -d '\n'
# → Add as YOUTUBE_TOKEN_PICKLE

# Client secrets (raw JSON, one line)
cat client_secrets.json | tr -d '\n'
# → Add as YOUTUBE_CLIENT_SECRETS
```

Add both at: `https://github.com/YOUR_USER/YOUR_REPO/settings/secrets/actions`

## Troubleshooting

| Error | Fix |
|-------|-----|
| `403: access_denied` | Add yourself as test user in OAuth consent screen |
| `403` / `insufficient authentication scopes` on `channels?mine=true` (CI / `fetch_analytics`) | Your pickle was minted **without** read + analytics scopes (e.g. old upload-only token). **Re-auth** with current app scopes (next section), then update `YOUTUBE_TOKEN_PICKLE`. Also confirm **YouTube Analytics API** is enabled in Google Cloud (step 1 above). |
| `Address already in use` | Kill port 8080: `lsof -ti:8080 \| xargs kill -9` |
| Token not saving | Don't close browser until redirect completes |
| "Google hasn't verified" | Click Advanced → Go to app (unsafe) |
| Wrong Google account | Use Chrome with correct profile, or incognito + login |

### Re-create the token with the right scopes (upload + read + analytics)

The repo requests these in [`youtube/uploader.py`](../youtube/uploader.py) (`SCOPES`): **`youtube.upload`**, **`youtube.readonly`**, **`yt-analytics.readonly`**. Uploads can still work if an older token only had `youtube.upload`; **personal analytics needs read + analytics** to list your channel and pull metrics.

1. Delete local `youtube_token.pickle` (or move it aside).
2. `source venv/bin/activate` and `python youtube_upload.py --auth`.
3. In the consent screen, **allow all** requested permissions (read + Analytics, not upload-only).
4. Encode and replace the GitHub secret:
   ```bash
   base64 -i youtube_token.pickle | tr -d '\n'
   ```
   → paste into **`YOUTUBE_TOKEN_PICKLE`** (Actions → Secrets).

Optional: before pushing to GitHub, print scopes locally:

```bash
python -c "import pickle; c=pickle.load(open('youtube_token.pickle','rb')); print(c.scopes)"
```

You should see URLs containing `youtube.readonly` and `yt-analytics.readonly` (and usually `youtube.upload`).

## Token Refresh

Tokens last ~6 months. If uploads start failing with auth errors:

1. Delete `youtube_token.pickle`
2. Re-run `python youtube_upload.py --auth`
3. Update `YOUTUBE_TOKEN_PICKLE` secret in GitHub

## Files

| File | Purpose | Git |
|------|---------|-----|
| `client_secrets.json` | OAuth client config | ❌ .gitignore |
| `youtube_token.pickle` | Auth token | ❌ .gitignore |
| `YOUTUBE_CLIENT_SECRETS` | GitHub secret | N/A |
| `YOUTUBE_TOKEN_PICKLE` | GitHub secret (base64) | N/A |

