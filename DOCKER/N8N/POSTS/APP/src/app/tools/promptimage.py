import os
import time
import requests
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from typing import Dict, Any, Type, List
from dotenv import load_dotenv

load_dotenv()


class PromptImageClient:
    """Cliente para interação com a API HuggingFace Replicate."""

    def __init__(self, token: str = None, endpoint: str = None):
        self.token = token or os.getenv("TL_TOKEN")
        self.endpoint = endpoint or os.getenv("REPLICATE_ENDPOINT")
        if not self.token or not self.endpoint:
            raise ValueError("Token ou endpoint não configurados")

        self.headers = {
            "Authorization": f"Bearer {self.token}",  # ⚠️ importante!
            "Content-Type": "application/json"
        }

    def generate_image(self, prompt_image: str, num_outputs: int = 1):
        payload = {"input": {"prompt": prompt_image, "num_outputs": num_outputs}}
        response = requests.post(self.endpoint, headers=self.headers, json=payload)
        res_json = response.json()

        # Para status 201, ainda está "starting", então retornamos a URL de polling
        if response.status_code in [200, 201]:
            # Retorna o link 'get' para checar o resultado
            return res_json.get("urls", {})
        else:
            raise Exception(f"Erro HTTP {response.status_code}: {res_json}")




class PromptImageInput(BaseModel):
    """Parâmetros para gerar uma imagem a partir de um prompt."""
    prompt_image: str = Field(..., description="Descrição textual da imagem a ser gerada.")
    num_outputs: int = Field(1, description="Número de imagens a serem geradas.", ge=1, le=4)


class PromptImageTool(BaseTool):
    name: str = "PromptImageTool"
    description: str = "Gera uma imagem a partir de um prompt textual usando a API HuggingFace Replicate."
    args_schema: Type[BaseModel] = PromptImageInput

    def _run(self, prompt_image: str, num_outputs: int = 1) -> List[str]:
        client = PromptImageClient()
        return client.generate_image(prompt_image, num_outputs)

    async def _arun(self, prompt_image: str, num_outputs: int = 1) -> List[str]:
        raise NotImplementedError("Async not implemented for PromptImageTool.")

