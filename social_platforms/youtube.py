"""YouTube platform integration with video generation from images.

Creates short videos from static images using ffmpeg and uploads them to YouTube
via the YouTube Data API v3.

Environment variables:
- YOUTUBE_CLIENT_ID: Google OAuth2 client ID
- YOUTUBE_CLIENT_SECRET: Google OAuth2 client secret  
- YOUTUBE_REFRESH_TOKEN: OAuth2 refresh token for YouTube uploads
- YOUTUBE_VIDEO_DURATION: Video length in seconds (default: 5)
- YOUTUBE_AUDIO_FILE: Optional audio file to add to videos

OAuth2 Setup:
1. Create a Google Cloud project and enable YouTube Data API v3
2. Create OAuth2 credentials (desktop application type)
3. Use Google's OAuth2 flow to get a refresh token with youtube.upload scope
4. Set the refresh token in YOUTUBE_REFRESH_TOKEN
"""

import os
import subprocess
import logging
import tempfile
from pathlib import Path
from typing import Optional
import json

import requests

logger = logging.getLogger(__name__)


class YouTubePoster:
    """Handler for posting videos to YouTube from static images."""

    platform_name = "YouTube"

    def __init__(self):
        self.client_id = os.getenv('YOUTUBE_CLIENT_ID')
        self.client_secret = os.getenv('YOUTUBE_CLIENT_SECRET')
        self.refresh_token = os.getenv('YOUTUBE_REFRESH_TOKEN')
        
        if not all([self.client_id, self.client_secret, self.refresh_token]):
            raise ValueError("Missing YouTube OAuth2 credentials: YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN")
        
        self.video_duration = int(os.getenv('YOUTUBE_VIDEO_DURATION', '5'))
        self.audio_file = os.getenv('YOUTUBE_AUDIO_FILE')
        
        # Check for ffmpeg
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise ValueError("ffmpeg is required for video generation. Install ffmpeg and ensure it's in PATH.")

    def _get_access_token(self) -> Optional[str]:
        """Get fresh access token using refresh token."""
        try:
            data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'refresh_token': self.refresh_token,
                'grant_type': 'refresh_token'
            }
            
            resp = requests.post('https://oauth2.googleapis.com/token', data=data, timeout=30)
            
            if resp.status_code == 200:
                token_data = resp.json()
                return token_data.get('access_token')
            else:
                logger.error(f"Token refresh failed {resp.status_code}: {resp.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error refreshing access token: {e}")
            return None

    def _create_video_from_image(self, image_path: Path) -> Optional[Path]:
        """Create a short video from a static image using ffmpeg."""
        try:
            # Create temporary output file
            with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
                output_path = Path(tmp.name)
            
            # Base ffmpeg command: static image for duration
            cmd = [
                'ffmpeg', '-y',  # overwrite output
                '-loop', '1',    # loop the image
                '-i', str(image_path),
                '-t', str(self.video_duration),  # duration
                '-pix_fmt', 'yuv420p',  # compatibility
                '-vf', 'scale=1280:720:force_original_aspect_ratio=decrease:eval=frame,pad=1280:720:(ow-iw)/2:(oh-ih)/2',  # 720p with padding
            ]
            
            # Add audio if specified
            if self.audio_file and Path(self.audio_file).exists():
                cmd.extend(['-i', self.audio_file, '-c:a', 'aac', '-shortest'])
            else:
                cmd.extend(['-an'])  # no audio
            
            cmd.extend(['-c:v', 'libx264', str(output_path)])
            
            logger.info(f"Creating video from {image_path.name}...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"ffmpeg failed: {result.stderr}")
                return None
            
            logger.info(f"Video created: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating video: {e}")
            return None

    def _upload_video(self, video_path: Path, title: str, description: str) -> bool:
        """Upload video to YouTube."""
        try:
            access_token = self._get_access_token()
            if not access_token:
                return False
            
            # Video metadata
            metadata = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': ['lain', 'serial experiments lain', 'anime'],
                    'categoryId': '24'  # Entertainment
                },
                'status': {
                    'privacyStatus': 'public'  # or 'private', 'unlisted'
                }
            }
            
            # Upload in two steps: metadata then file
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            # Initial request
            url = 'https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status'
            resp = requests.post(url, headers=headers, json=metadata, timeout=30)
            
            if resp.status_code not in (200, 201):
                logger.error(f"YouTube upload init failed {resp.status_code}: {resp.text}")
                return False
            
            upload_url = resp.headers.get('Location')
            if not upload_url:
                logger.error("No upload URL returned from YouTube")
                return False
            
            # Upload video file
            with open(video_path, 'rb') as f:
                video_headers = {
                    'Content-Type': 'video/mp4',
                    'Content-Length': str(video_path.stat().st_size)
                }
                
                resp = requests.put(upload_url, headers=video_headers, data=f, timeout=300)
            
            if resp.status_code in (200, 201):
                data = resp.json()
                video_id = data.get('id')
                logger.info(f"Video uploaded to YouTube: https://youtube.com/watch?v={video_id}")
                return True
            else:
                logger.error(f"YouTube video upload failed {resp.status_code}: {resp.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error uploading to YouTube: {e}")
            return False
        
        finally:
            # Clean up video file
            try:
                if video_path.exists():
                    video_path.unlink()
            except Exception:
                pass

    def post(self, image_path: Path, text: str) -> bool:
        """Create video from image and upload to YouTube."""
        try:
            # Create video from image
            video_path = self._create_video_from_image(image_path)
            if not video_path:
                return False
            
            # Generate title and description
            title = f"Lain Iwakura - {text[:50]}"
            description = f"{text}\n\n#SerialExperimentsLain #Lain #Anime"
            
            # Upload to YouTube
            return self._upload_video(video_path, title, description)
            
        except Exception as e:
            logger.error(f"YouTube posting error: {e}")
            return False