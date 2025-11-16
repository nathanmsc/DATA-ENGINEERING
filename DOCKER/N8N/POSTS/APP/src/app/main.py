"""
FastAPI application for automated Instagram posting with AI-generated images.
"""
import os
import time
import mimetypes
import warnings
from pathlib import Path
from datetime import datetime

import uvicorn  # type: ignore[import]
import requests
from fastapi import FastAPI  # type: ignore[import]
from fastapi.responses import FileResponse  # type: ignore[import]
from fastapi.staticfiles import StaticFiles  # type: ignore[import]

from app.crew import App
from app.utils.inputs import Inputs
from app.tools.cloudflareapi import CloudflareAPIClient  # type: ignore[import]
from app.tools.mergeimages import MergeImageTool
from app.tools.googleapi import (  # type: ignore[import]
    GetRandomPostTool,
    GetPostByLineTool,
    GetPostDailyTool,
    UploadFileTool,
    GoogleDriveClient,
)
from app.tools.instagramapi import InstagramPostTool, PublishMediaTool  # type: ignore[import]
from app.tools.promptimage import PromptImageTool, PromptImageClient

# ============================================================================
# Configuration
# ============================================================================
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
IMG_DIR = BASE_DIR / "static" / "img"

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# ============================================================================
# FastAPI App Initialization
# ============================================================================
app = FastAPI(
    title="CrewAI Instagram Poster",
    version="2.0.0",
    description="Automated Instagram posting with AI-generated images"
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ============================================================================
# Tool Instances
# ============================================================================
cloudflare = CloudflareAPIClient()
mergeimages = MergeImageTool()
instagram_publish = InstagramPostTool()
publish_media = PublishMediaTool()
client_image = PromptImageClient()
daily = GetPostDailyTool()


# ============================================================================
# Helper Functions
# ============================================================================
def wait_for_media_ready(creation_id: str, access_token: str, timeout: int = 30) -> bool:
    """
    Wait for Instagram media to be processed.
    
    Args:
        creation_id: Instagram media creation ID
        access_token: Instagram access token
        timeout: Maximum wait time in seconds
        
    Returns:
        True if media is ready, False if timeout
    """
    url = f"https://graph.facebook.com/v21.0/{creation_id}"
    params = {"fields": "status_code", "access_token": access_token}
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        response = requests.get(url, params=params).json()
        status = response.get("status_code")
        
        if status == "FINISHED":
            return True
        
        time.sleep(2)
    
    return False


def download_file(url: str, local_path: Path, timeout: int = 20) -> dict:
    """
    Download a file from URL to local path.
    
    Args:
        url: Source URL
        local_path: Destination path
        timeout: Request timeout in seconds
        
    Returns:
        Dict with success status and error message if any
    """
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code != 200:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}"
            }
        
        local_path.parent.mkdir(parents=True, exist_ok=True)
        with open(local_path, "wb") as f:
            f.write(response.content)
        
        return {"success": True}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================================
# API Endpoints
# ============================================================================
@app.get("/")
async def root():
    """API information and available endpoints."""
    return {
        "app": "Instagram Auto Post",
        "version": "2.0.0",
        "endpoints": {
            "/": "API information",
            "/health": "Check configuration status",
            "/post_weekday": "Publish daily post automatically",
            "/text_to_image/{prompt}": "Generate image from text prompt",
            "/merge_images": "Merge background and logo images",
            "/publish_from_ia": "Publish using CrewAI"
        }
    }


@app.get("/health")
async def health_check():
    """Verify all required configurations are present."""
    required_env_vars = {
        "google_credentials": "GOOGLE_CREDENTIALS_FILE",
        "google_scopes": "GOOGLE_SCOPES",
        "sheet_id": "SHEET_ID",
        "worksheet_daily": "WORKSHEET_DAILY",
        "logo_file_id": "LOGO_FILE_ID",
        "gdrive_folder_id": "GDRIVE_FOLDER_ID",
        "instagram_token": "IG_ACCESS_TOKEN",
        "facebook_page_id": "FB_PAGE_ID",
        "facebook_endpoint": "FB_ENDPOINT"
    }
    
    checks = {key: bool(os.getenv(var)) for key, var in required_env_vars.items()}
    all_ok = all(checks.values())
    missing = [key for key, value in checks.items() if not value]
    
    return {
        "status": "healthy ✅" if all_ok else "unhealthy ⚠️",
        "checks": checks,
        "missing_env_vars": missing if missing else None
    }


@app.get("/robots.txt", include_in_schema=False)
async def robots():
    """Serve robots.txt file."""
    file_path = STATIC_DIR / "robots.txt"
    
    if not file_path.exists():
        return {"error": f"File not found: {file_path}"}
    
    media_type, _ = mimetypes.guess_type(str(file_path))
    return FileResponse(file_path, media_type=media_type or "text/plain")


@app.get("/text_to_image/{prompt_image}")
async def text_to_image(prompt_image: str):
    """
    Generate image from text prompt using AI.
    
    Args:
        prompt_image: Text description for image generation
        
    Returns:
        Dict with image URLs and paths
    """
    try:
        # Generate image
        tool = PromptImageTool()
        result = tool._run(prompt_image=prompt_image, num_outputs=1)
        image_url = result.get("stream")
        
        if not image_url:
            return {"error": "API did not return a valid URL"}
        
        # Download and save locally
        IMG_DIR.mkdir(parents=True, exist_ok=True)
        local_file = IMG_DIR / "stream.webp"
        
        download_result = download_file(image_url, local_file)
        if not download_result["success"]:
            return {"error": f"Failed to download: {download_result['error']}"}
        
        # Upload to Cloudflare R2
        r2_path = "generated/stream.png"
        public_url = cloudflare.upload_file(
            local_path=str(local_file),
            object_name=r2_path
        )
        
        return {
            "prompt_image": prompt_image,
            "image_source_url": image_url,
            "local_file": "/static/img/stream.webp",
            "r2_public_url": public_url
        }
    
    except Exception as e:
        return {"error": str(e)}


@app.get("/merge_images")
async def merge_images():
    """
    Merge background image with logo overlay.
    
    Returns:
        Dict with merged image paths and URLs
    """
    try:
        IMG_DIR.mkdir(parents=True, exist_ok=True)
        
        # Define paths
        background_url = "https://mindsetcloud.net/generated/stream.png"
        logo_url = "https://mindsetcloud.net/static/img/logo.png"
        local_output = IMG_DIR / "merged.webp"
        
        # Execute merge
        merge_result = mergeimages._run(
            background=background_url,
            logo=logo_url,
            output_file=str(local_output)
        )
        
        # Upload to R2
        r2_path = "generated/merged.png"
        public_url = cloudflare.upload_file(
            local_path=str(local_output),
            object_name=r2_path
        )
        
        return {
            "result": merge_result,
            "local_file": "/static/img/merged.webp",
            "r2_public_url": public_url
        }
    
    except Exception as e:
        return {"error": str(e)}


@app.get("/post_weekday")
async def post_weekday():
    """
    Automated daily Instagram post workflow:
    1. Fetch content from Google Sheets based on weekday
    2. Generate AI image from prompt
    3. Download and merge with logo
    4. Upload to R2 storage
    5. Post to Instagram
    
    Returns:
        Dict with post details and status
    """
    try:
        # Step 1: Get weekday and fetch content
        day = datetime.now().weekday() + 2
        sheet_id = "1Xnnn8magRSgVRcu3mjcHE7MVg5g0hZL2YjuCvcGCjRs"
        caption_dict = daily._run(sheet_id, day)
        
        if not caption_dict:
            return {"error": "No content found for today"}
        
        caption_text = caption_dict.get("Content")
        prompt_text = caption_dict.get("Prompt_image")
        
        if not prompt_text:
            return {"error": "Image prompt not found"}
        
        # Step 2: Generate AI image
        urls = client_image.generate_image(prompt_text, num_outputs=1)
        image_url = urls.get("stream")
        
        if not image_url:
            return {"error": f"Invalid API response: {urls}"}
        
        # Step 3: Download generated image
        IMG_DIR.mkdir(parents=True, exist_ok=True)
        stream_local_path = IMG_DIR / "stream.webp"
        
        stream_result = download_file(image_url, stream_local_path)
        if not stream_result["success"]:
            return {"error": f"Failed to download stream: {stream_result['error']}"}
        
        # Step 4: Download logo
        logo_url = "https://mindsetcloud.net/static/img/logo.png"
        logo_local_path = IMG_DIR / "logo.png"
        
        logo_result = download_file(logo_url, logo_local_path)
        if not logo_result["success"]:
            return {"error": f"Failed to download logo: {logo_result['error']}"}
        
        # Step 5: Merge images
        merged_local_path = IMG_DIR / "merged.webp"
        merge_result = mergeimages._run(
            background=str(stream_local_path),
            logo=str(logo_local_path),
            output_file=str(merged_local_path)
        )
        
        if not merged_local_path.exists():
            return {"error": f"Merge failed: {merge_result}"}
        
        # Step 6: Upload to R2
        r2_merged_key = "generated/merged.png"
        merged_r2_url = "https://mindsetcloud.net/generated/merged.png"
        cloudflare.upload_file(
            local_path=str(merged_local_path),
            object_name=r2_merged_key
        )
        
        # Step 7: Publish to Instagram
        creation_id = instagram_publish._run(
            image_url=merged_r2_url,
            caption=caption_text
        )
        
        # Step 8: Wait for Instagram processing
        if not wait_for_media_ready(creation_id, os.getenv("IG_ACCESS_TOKEN")):
            return {"error": "Instagram media processing timeout"}
        
        post_id = publish_media._run(creation_id)
        
        return {
            "day": day,
            "caption": caption_text,
            "prompt_image": prompt_text,
            "stream_url": image_url,
            "local_files": {
                "stream": str(stream_local_path),
                "logo": str(logo_local_path),
                "merged": str(merged_local_path)
            },
            "final_image_r2_url": merged_r2_url,
            "instagram_post_id": post_id,
            "status": "✅ Post created and published successfully"
        }
    
    except Exception as e:
        return {"error": str(e)}


@app.get("/publish_from_ia")
async def publish_from_ia():
    """
    Publish Instagram post using CrewAI with random inputs.
    
    Returns:
        CrewAI execution result
    """
    try:
        inputs = Inputs().get_radom_inputs()
        return App().crew().kickoff(inputs=inputs)
    except Exception as e:
        return {"error": f"CrewAI execution failed: {str(e)}"}


@app.get("/get_radom_post")
async def get_random_post():
    """
    Get random post inputs for testing.
    
    Returns:
        Random post configuration
    """
    try:
        return Inputs().get_radom_inputs()
    except Exception as e:
        return {"error": str(e)}


@app.get("/post_by_row/{row_id}")
async def post_by_row(row_id: int):
    """
    Publish post from specific spreadsheet row.
    
    Args:
        row_id: Row number in spreadsheet
        
    Returns:
        Post details
    """
    try:
        return {"row_id": row_id}
    except Exception as e:
        return {"error": str(e)}


# ============================================================================
# Application Entry Point
# ============================================================================
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )