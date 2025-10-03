import os
import requests
from typing import Type
from dotenv import load_dotenv # type: ignore
from crewai.tools import BaseTool # type: ignore
from functools import cached_property
from pydantic import BaseModel, Field # type: ignore

load_dotenv()

class InstagramClient:
    """Cliente para integração com a API do Instagram (via Facebook Graph API)."""

    def __init__(self):
        self.access_token = os.getenv("IG_ACCESS_TOKEN")
        self.endpoint = os.getenv("FB_ENDPOINT")
        self.page_id = os.getenv("FB_PAGE_ID")

        if not self.access_token or not self.endpoint or not self.page_id:
            raise ValueError("⚠️ Configurações do Instagram não encontradas no .env")

    def create_media_object(self, image_url: str, caption: str) -> str:
        """Cria um objeto de mídia no Instagram e retorna o ID do contêiner."""
        create_url = f"{self.endpoint}{self.page_id}/media"
        payload = {
            "image_url": image_url,
            "caption": caption,
            "access_token": self.access_token
        }
        response = requests.post(create_url, data=payload)
        res_json = response.json()

        if "id" in res_json:
            return res_json["id"]
        else:
            raise Exception(f"Erro ao criar objeto de mídia: {res_json.get('error', 'Unknown error')}")
        
    def publish_media(self, creation_id: str) -> str:
        """Publica o objeto de mídia criado e retorna o ID da postagem."""
        publish_url = f"{self.endpoint}{self.page_id}/media_publish"
        payload = {
            "creation_id": creation_id,
            "access_token": self.access_token
        }
        response = requests.post(publish_url, data=payload)
        res_json = response.json()

        if "id" in res_json:
            return res_json["id"]
        else:
            raise Exception(f"Erro ao publicar mídia: {res_json.get('error', 'Unknown error')}")


class InstagramPostInput(BaseModel):
    """Parâmetros para criar e publicar um post no Instagram."""
    image_url: str = Field(..., description="URL da imagem a ser postada no Instagram.")
    caption: str = Field(..., description="Legenda que acompanha a imagem.")


class InstagramPostTool(BaseTool):
    name: str = "instagram_post_tool"
    description: str = "Cria e publica um post (imagem + legenda) no Instagram, retornando o ID da postagem."
    args_schema: Type[BaseModel] = InstagramPostInput

    def _run(self, image_url: str, caption: str) -> str:
        client = InstagramClient()
        return client.create_media_object(image_url, caption)

    async def _arun(self, image_url: str, caption: str) -> str:
        raise NotImplementedError("Execução assíncrona não implementada.")
       
class PublishMediaInput(BaseModel):
    """Parâmetros para publicar mídia no Instagram."""
    creation_id: str = Field(..., description="ID do contêiner de mídia previamente criado.")


class PublishMediaTool(BaseTool):
    name: str = "publish_instagram_media"
    description: str = "Publica uma mídia previamente criada no Instagram e retorna o ID da postagem."
    args_schema: Type[BaseModel] = PublishMediaInput

    def _run(self, creation_id: str) -> str:
        client = InstagramClient()
        return client.publish_media(creation_id)

    async def _arun(self, creation_id: str) -> str:
        raise NotImplementedError("Execução assíncrona não implementada.")


# Exemplo de uso
caption = '''DI Sorrisos – Transformando sorrisos!

            🦷 Agende seu atendimento:
            📍 R. Pinto de Aguiar, 2475 – Sala 111 – Imbuí Torres Center
            📞 contato: 71 98298-5180
            📲 Siga: @disorrisos'''


