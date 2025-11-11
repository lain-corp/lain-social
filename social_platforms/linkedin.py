"""LinkedIn platform integration for image posts (UGC API).

This implements the registerUpload -> upload -> create UGC post flow.
Requires:
  - LINKEDIN_ACCESS_TOKEN: OAuth2 access token with w_member_social (or rw_organization_admin) scope
  - LINKEDIN_OWNER_URN: Owner URN, e.g. 'urn:li:person:xxxx' or 'urn:li:organization:yyyy'

Notes:
  - Organization posting requires a token authorized for that organization and the owner URN must be the organization URN.
  - The upload URL returned by LinkedIn may accept a direct PUT of the binary image.
  - See: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/community-management/shares/vector-upload
"""

import os
import logging
from pathlib import Path
from typing import Optional
import mimetypes
import requests

logger = logging.getLogger(__name__)


class LinkedInPoster:
    """Handler for posting images to LinkedIn using UGC endpoints."""

    platform_name = "LinkedIn"

    def __init__(self):
        self.access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.owner_urn = os.getenv('LINKEDIN_OWNER_URN')
        if not self.access_token or not self.owner_urn:
            raise ValueError("Missing LINKEDIN_ACCESS_TOKEN or LINKEDIN_OWNER_URN environment variables")

        self.base_url = os.getenv('LINKEDIN_API_BASE_URL', 'https://api.linkedin.com')
        # Recommended header per LinkedIn docs
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'X-Restli-Protocol-Version': '2.0.0'
        }

    def _register_upload(self) -> Optional[dict]:
        url = f"{self.base_url}/v2/assets?action=registerUpload"
        payload = {
            "registerUploadRequest": {
                "owner": self.owner_urn,
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }
                ]
            }
        }

        resp = requests.post(url, json=payload, headers={**self.headers, 'Content-Type': 'application/json'}, timeout=30)
        if resp.status_code not in (200, 201):
            logger.error(f"LinkedIn registerUpload failed {resp.status_code}: {resp.text}")
            return None

        return resp.json().get('value')

    def _upload_binary(self, upload_url: str, image_path: Path) -> bool:
        mime_type, _ = mimetypes.guess_type(str(image_path))
        if not mime_type:
            mime_type = 'application/octet-stream'

        try:
            with open(image_path, 'rb') as f:
                # LinkedIn upload URL typically expects a PUT of the raw bytes
                resp = requests.put(upload_url, data=f.read(), headers={'Content-Type': mime_type}, timeout=60)

            if resp.status_code not in (200, 201):
                logger.error(f"LinkedIn binary upload failed {resp.status_code}: {resp.text}")
                return False

            return True

        except Exception as e:
            logger.error(f"Error uploading binary to LinkedIn: {e}")
            return False

    def _create_ugc_post(self, asset_urn: str, text: str) -> bool:
        url = f"{self.base_url}/v2/ugcPosts"
        body = {
            "author": self.owner_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "IMAGE",
                    "media": [
                        {
                            "status": "READY",
                            "description": {"text": "Lain Iwakura"},
                            "media": asset_urn,
                            "title": {"text": "Lain"}
                        }
                    ]
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }

        resp = requests.post(url, json=body, headers={**self.headers, 'Content-Type': 'application/json'}, timeout=30)
        if resp.status_code not in (201, 200):
            logger.error(f"LinkedIn ugcPosts create failed {resp.status_code}: {resp.text}")
            return False

        return True

    def post(self, image_path: Path, text: str) -> bool:
        try:
            register_value = self._register_upload()
            if not register_value:
                return False

            # Extract asset URN and upload URL
            asset = register_value.get('asset')
            upload_mech = register_value.get('uploadMechanism', {})
            # Different key depending on response; try common one
            upload_info = None
            for key in upload_mech:
                upload_info = upload_mech.get(key)
                if upload_info:
                    break

            upload_url = None
            if upload_info:
                upload_url = upload_info.get('uploadUrl') or upload_info.get('uploadUrls')

            if isinstance(upload_url, list):
                upload_url = upload_url[0]

            if not asset or not upload_url:
                logger.error(f"Invalid registerUpload response: asset={asset} upload_url={upload_url}")
                return False

            # Upload binary
            if not self._upload_binary(upload_url, image_path):
                return False

            # Create post referencing the asset URN
            return self._create_ugc_post(asset, text)

        except Exception as e:
            logger.error(f"Error posting to LinkedIn: {e}")
            return False
