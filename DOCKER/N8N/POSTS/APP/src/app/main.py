import sys
import uvicorn # type: ignore[import]
import warnings
from app.crew import App
from fastapi import FastAPI # type: ignore[import]
from datetime import datetime
from app.utils.inputs import Inputs
from app.tools.googleapi import GetRandomPostTool, MergeImageTool, GetPostByLineTool, GetPostDailyool # type: ignore[import]
from app.tools.instagramapi import InstagramPostTool # type: ignore[import]
from app.tools.promptimage import PromptImageTool

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

app = FastAPI(title="CrewAI Instagram Poster", version="1.0.0")

get_instructions = GetRandomPostTool()
result = get_instructions._run()
instagram_publish = InstagramPostTool()
mergeimages = MergeImageTool()
row = GetPostByLineTool()
daily = GetPostDailyool()
prompt_image = PromptImageTool()

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
    
@app.get("/post_weekday")    
async def post_weekday():

    day = datetime.now().weekday() + 2
    content = daily._run(day)
    prompt_image = content.get('Prompt_image')
    #url_background = prompt_image._run(prompt_image="A futuristic cyberpunk city at night", num_outputs=1)

    '''result = mergeimages.run(
        url_background=url_background,
        logo_id="1FOU1upy94M-cG6qpc3JtQO8bzKU0_2Dc",
        output_file="image.png"
    )'''

    return prompt_image


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")





