import os
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path
from typing import Type, Optional
from crewai.tools import BaseTool  # type: ignore
from pydantic import BaseModel, Field  # type: ignore


class MergeImageInput(BaseModel):
    """Parâmetros para mesclar uma imagem de fundo com logomarca (Google Drive)."""
    background: str = Field(..., description="url do arquivo da imagem de fundo.")
    logo: str = Field(..., description="url da logomarca")
    output_file: str = Field("merge.png", description="Caminho de saída da imagem mesclada")


class MergeImageTool(BaseTool):
    name: str = "merge_image"
    description: str = "Mescla uma imagem de fundo com uma logomarca."
    args_schema: Type[BaseModel] = MergeImageInput
    
    def _run(self, background: str, logo: str, output_file: str) -> str:
        """Executa a mesclagem das imagens."""
        try:
            # Garantir que o diretório de saída existe
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Download da imagem de fundo
            background_response = requests.get(background, timeout=10)
            background_response.raise_for_status()
            bg_bytes = BytesIO(background_response.content)
            
            # Download da logo
            logo_response = requests.get(logo, timeout=10)
            logo_response.raise_for_status()
            logo_bytes = BytesIO(logo_response.content)
            
            # Abrir imagens
            img = Image.open(bg_bytes).convert("RGBA")
            logo_img = Image.open(logo_bytes).convert("RGBA")
            
            # Redimensionar logo
            largura_logo = img.width // 6
            nova_altura = int(logo_img.height * largura_logo / logo_img.width)
            logo_resized = logo_img.resize((largura_logo, nova_altura), Image.Resampling.LANCZOS)
            
            # Calcular posição (canto inferior direito)
            pos_x = img.width - logo_resized.width - 10
            pos_y = img.height - logo_resized.height - 10
            posicao = (pos_x, pos_y)
            
            # Mesclar imagens
            img_com_logo = img.copy()
            img_com_logo.paste(logo_resized, posicao, logo_resized)
            
            # Converter para RGB se necessário (para salvar como JPEG)
            if output_file.lower().endswith(('.jpg', '.jpeg')):
                img_com_logo = img_com_logo.convert("RGB")
            
            # Salvar imagem
            img_com_logo.save(output_file, quality=95)
            
            # Verificar se o arquivo foi criado
            if not os.path.exists(output_file):
                raise Exception(f"Arquivo não foi criado em: {output_file}")
            
            print(f"Imagem salva com sucesso em: {output_file}")
            return output_file
            
        except requests.exceptions.Timeout:
            error_msg = "Erro: Timeout ao baixar as imagens"
            print(error_msg)
            return error_msg
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Erro na requisição: {str(e)}"
            print(error_msg)
            return error_msg
            
        except Image.UnidentifiedImageError:
            error_msg = "Erro: O arquivo baixado não é uma imagem válida"
            print(error_msg)
            return error_msg
        
        except PermissionError as e:
            error_msg = f"Erro de permissão ao salvar arquivo: {str(e)}"
            print(error_msg)
            return error_msg
            
        except Exception as e:
            error_msg = f"Erro inesperado: {str(e)}"
            print(error_msg)
            return error_msg
    
    async def _arun(self, *args, **kwargs) -> str:
        """Execução assíncrona não implementada."""
        raise NotImplementedError("Execução assíncrona não implementada.")


# Teste
'''tool = MergeImageTool()
local = "/home/user/DATA-ENGINEERING/DOCKER/N8N/POSTS/APP/src/app/static/img/merge_2img.png"
url = 'http://localhost:8000/static/img/logo.png'
result = tool._run(url, url, local)
print(f"Resultado: {result}")'''