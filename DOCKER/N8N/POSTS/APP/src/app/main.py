import sys
import os
import mimetypes
import uvicorn # type: ignore[import]
import warnings
from pathlib import Path
from app.crew import App
from fastapi import FastAPI # type: ignore[import]
from datetime import datetime
from app.utils.inputs import Inputs
from fastapi.responses import FileResponse # type: ignore[import]
from app.tools.mergeimages import MergeImageTool
from app.tools.googleapi import GetRandomPostTool, GetPostByLineTool, GetPostDailyTool, UploadFileTool, GoogleDriveClient # type: ignore[import]
from app.tools.instagramapi import InstagramPostTool, PublishMediaTool # type: ignore[import]
from app.tools.promptimage import PromptImageTool, PromptImageClient

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

app = FastAPI(title="CrewAI Instagram Poster", version="1.0.0")

get_instructions = GetRandomPostTool()
result = get_instructions._run()
instagram_publish = InstagramPostTool()
mergeimages = MergeImageTool()
row = GetPostByLineTool()
daily = GetPostDailyTool()
client_image = PromptImageClient()
prompt_image = PromptImageTool()
publish = PublishMediaTool()
upload = UploadFileTool()
drive = GoogleDriveClient()
 
@app.get("/")
async def root():
    """Informações sobre a API."""
    return {
        "app": "Instagram Auto Post",
        "version": "2.0.0",
        "endpoints": {
            "/": "Informações da API",
            "/post_weekday": "Publica post do dia automaticamente",
            "/health": "Verifica status das configurações"
        }
    }


@app.get("/health")
async def health_check():
    """Verifica se todas as configurações necessárias estão presentes."""
    checks = {
        "google_credentials": bool(os.getenv("GOOGLE_CREDENTIALS_FILE")),
        "google_scopes": bool(os.getenv("GOOGLE_SCOPES")),
        "sheet_id": bool(os.getenv("SHEET_ID")),
        "worksheet_daily": bool(os.getenv("WORKSHEET_DAILY")),
        "logo_file_id": bool(os.getenv("LOGO_FILE_ID")),
        "gdrive_folder_id": bool(os.getenv("GDRIVE_FOLDER_ID")),
        "instagram_token": bool(os.getenv("IG_ACCESS_TOKEN")),
        "facebook_page_id": bool(os.getenv("FB_PAGE_ID")),
        "facebook_endpoint": bool(os.getenv("FB_ENDPOINT"))
    }
    
    all_ok = all(checks.values())
    missing = [key for key, value in checks.items() if not value]
    
    return {
        "status": "healthy ✅" if all_ok else "unhealthy ⚠️",
        "checks": checks,
        "missing_env_vars": missing if missing else None
    }


@app.get("/robots.txt", include_in_schema=False)
async def robots():
    BASE_DIR = Path(__file__).resolve().parent
    STATIC_DIR = BASE_DIR / "static"

    file_path = STATIC_DIR / "robots.txt"

    if not file_path.exists():
        return {"error": f"Arquivo {file_path} não encontrado."}

    media_type, _ = mimetypes.guess_type(str(file_path))
    if media_type is None:
        media_type = "text/plain"

    return FileResponse(file_path, media_type=media_type)


@app.get("/publish_from_ia")
async def publish_from_ia():
    """
    CrewAI Instagram Poster is running.
    """
    inputs = Inputs().get_radom_inputs()
    
    try:
        return App().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    
@app.get("/get_radom_post")
async def get_radom_post():
    """
    Instagram Poster is running.
    """
    inputs = Inputs().get_radom_inputs()
    
    try:
        return inputs
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    
@app.get("/text_to_image/{prompt_image}")
async def text_to_image(prompt_image: str):
    try:
        tool = PromptImageTool()
        #urls: List[str] = tool._run(prompt_image=prompt_image, num_outputs=1)
        urls = 'http://localhost'
        return {"prompt_image": prompt_image, "image_urls": urls}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/post_by_row/{row_id}")
async def post_by_row(row_id: int):
    try:
        
        return {row_id}
    except Exception as e:
        return {'error': str(e)}

@app.get("/static/{file_path:path}")
async def serve_static(file_path: str):
   
    BASE_DIR = 'static'
    file_path = os.path.join(BASE_DIR, file_path)

    if not os.path.exists(file_path):
        return {"error": f"Arquivo {file_path} não encontrado."}

    # Detecta o tipo de mídia pelo sufixo
    media_type, _ = mimetypes.guess_type(file_path)
    if media_type is None:
        media_type = "application/octet-stream"

    return FileResponse(file_path, media_type=media_type)
    
@app.get("/post_weekday")
async def post_weekday():
    try:
        day = datetime.now().weekday() + 2

        sheet_id = '1Xnnn8magRSgVRcu3mjcHE7MVg5g0hZL2YjuCvcGCjRs'
        caption_dict = daily._run(sheet_id, day)
        if not caption_dict:
            return {"error": "Nenhum conteúdo encontrado para hoje."}

        caption_text = caption_dict.get("Content")
        prompt_text = caption_dict.get("Prompt_image")
        if not prompt_text:
            return {"error": "Prompt de imagem não encontrado."}

        urls = client_image.generate_image(prompt_text, num_outputs=1)
        background = urls.get("stream") or urls.get("url") or urls.get("output")
        if not background:
            return {"error": f"API não retornou URL válida: {urls}"}

        print(background)

        logo = 'https://drive.usercontent.google.com/download?id=1kGfY-jxfz9t1_3Xt1MlkhjXndpwy6qdN&export=download&authuser=0'
        output_file = "/home/user/DATA-ENGINEERING/DOCKER/N8N/POSTS/APP/src/app/static/img/merged.png"

        mergeimages._run(
            background=background,
            logo=logo,
            output_file=output_file
        )


        public_url = 'https://rqq06t0x-8000.brs.devtunnels.ms/static/img/merged.png'

        creation_id = instagram_publish._run(
            image_url=public_url,
            caption=caption_text
        )

        post_id = PublishMediaTool()._run(creation_id)

        return {
            "day": day,
            "caption": caption_text,
            "prompt_image": prompt_text,
            "image_url_generated": background,
            "final_image_drive_url": public_url,
            "instagram_post_id": post_id,
            "status": "✅ Post preparado e publicado com sucesso"
        }

    except Exception as e:
        return {"error": str(e)}



@app.get("/merge_images")
async def merge_images():
    try:
        logo = 'https://drive.usercontent.google.com/download?id=1kGfY-jxfz9t1_3Xt1MlkhjXndpwy6qdN&export=download&authuser=0'
        output_file = "/home/user/DATA-ENGINEERING/DOCKER/N8N/POSTS/APP/src/app/static/img/merged.png"

        result = mergeimages._run(
            background=logo,
            logo=logo,
            output_file=output_file
        )

        return {
            "result": result
        }
    except Exception as e:
        return {"error": str(e)}


    

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")





