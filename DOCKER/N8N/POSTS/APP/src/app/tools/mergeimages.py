# app/tools/mergeimages.py
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from PIL import Image
import requests
from io import BytesIO
import os


class MergeImageInput(BaseModel):
    """Input schema para MergeImageTool."""
    background: str = Field(..., description="URL ou caminho local da imagem de fundo")
    logo: str = Field(..., description="URL ou caminho local do logo")
    output_file: str = Field(..., description="Caminho onde salvar a imagem mesclada")


class MergeImageTool(BaseTool):
    name: str = "Merge Images Tool"
    description: str = (
        "Mescla duas imagens: coloca um logo no canto inferior direito "
        "de uma imagem de fundo. Aceita URLs ou caminhos locais."
    )
    args_schema: Type[BaseModel] = MergeImageInput

    def _run(
        self,
        background: str,
        logo: str,
        output_file: str = "merged.png"
    ) -> str:
        """
        Mescla imagem de fundo com logo no canto inferior direito.
        
        Args:
            background: URL ou caminho local da imagem de fundo
            logo: URL ou caminho local do logo
            output_file: Caminho onde salvar o resultado
            
        Returns:
            Caminho do arquivo salvo
        """
        try:
            # Função auxiliar para carregar imagem (URL ou local)
            def load_image(source: str) -> Image.Image:
                if source.startswith(('http://', 'https://')):
                    # É uma URL
                    response = requests.get(source, timeout=20)
                    response.raise_for_status()
                    return Image.open(BytesIO(response.content)).convert("RGBA")
                else:
                    # É um arquivo local
                    if not os.path.exists(source):
                        raise FileNotFoundError(f"Arquivo não encontrado: {source}")
                    return Image.open(source).convert("RGBA")

            # Carregar imagens
            bg_img = load_image(background)
            logo_img = load_image(logo)

            # Dimensões
            bg_width, bg_height = bg_img.size
            logo_width, logo_height = logo_img.size

            # Redimensionar logo se necessário (máximo 20% da largura do fundo)
            max_logo_width = int(bg_width * 0.2)
            if logo_width > max_logo_width:
                ratio = max_logo_width / logo_width
                new_logo_height = int(logo_height * ratio)
                logo_img = logo_img.resize((max_logo_width, new_logo_height), Image.Resampling.LANCZOS)
                logo_width, logo_height = logo_img.size

            # Posição: canto inferior direito com margem de 5%
            margin = int(bg_width * 0.05)
            x = bg_width - logo_width - margin
            y = bg_height - logo_height - margin

            # Criar cópia do background e colar logo
            result = bg_img.copy()
            result.paste(logo_img, (x, y), logo_img)

            # Garantir que o diretório de saída existe
            output_dir = os.path.dirname(output_file)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            # Salvar resultado (detecta formato pela extensão)
            file_ext = os.path.splitext(output_file)[1].lower()
            
            if file_ext == ".webp":
                # Salvar como WebP
                result.convert("RGB").save(output_file, "WEBP", quality=95)
            elif file_ext == ".png":
                # Salvar como PNG
                result.convert("RGB").save(output_file, "PNG", quality=95)
            elif file_ext in [".jpg", ".jpeg"]:
                # Salvar como JPEG
                result.convert("RGB").save(output_file, "JPEG", quality=95)
            else:
                # Default: PNG
                result.convert("RGB").save(output_file, "PNG", quality=95)

            return f"✅ Imagem mesclada salva em: {output_file}"

        except requests.RequestException as e:
            return f"❌ Erro ao baixar imagem: {str(e)}"
        except FileNotFoundError as e:
            return f"❌ {str(e)}"
        except Exception as e:
            return f"❌ Erro ao mesclar imagens: {str(e)}"