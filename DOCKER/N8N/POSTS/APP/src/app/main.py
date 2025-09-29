import sys
import uvicorn # type: ignore[import]
import warnings
from app.crew import App
from fastapi import FastAPI # type: ignore[import]
from datetime import datetime
from app.tools.googleapi import GetRandomPostTool # type: ignore[import]
from app.tools.instagramapi import InstagramPostTool # type: ignore[import]
from app.utils.inputs import Inputs

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

app = FastAPI(title="CrewAI Instagram Poster", version="1.0.0")

get_instructions = GetRandomPostTool()
result = get_instructions._run()
instagram_publish = InstagramPostTool()

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
    

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")





