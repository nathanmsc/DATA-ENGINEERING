from PIL import Image
import requests
from io import BytesIO

def merge_images(id_background):
    # IDs dos arquivos no Google Drive
    id_logo = '1XziOJF1E-GQBzLVXOQc55iez2ZIa2vWI'

    # URLs diretas para download
    url_background = f'https://drive.google.com/uc?export=download&id={id_background}'
    url_logo = f'https://drive.google.com/uc?export=download&id={id_logo}'

    # Carrega a imagem principal
    response = requests.get(url_background)
    img = Image.open(BytesIO(response.content)).convert("RGBA")

    # Carrega a logomarca
    response_logo = requests.get(url_logo)
    logo = Image.open(BytesIO(response_logo.content)).convert("RGBA")

    # Redimensiona a logomarca (opcional)
    largura_logo = img.width // 6  # 1/6 da largura da imagem
    logo = logo.resize((largura_logo, int(logo.height * largura_logo / logo.width)))

    # Define a posição da logomarca (ex: canto inferior direito)
    pos_x = img.width - logo.width - 10
    pos_y = img.height - logo.height - 10
    posicao = (pos_x, pos_y)

    # Sobrepõe a logomarca na imagem
    img_com_logo = img.copy()
    img_com_logo.paste(logo, posicao, logo)

    # Salva o resultado
    img_com_logo.save("merge.png")

    # Mostra o resultado
    img_com_logo.show()


# Chama a função
merge_images('13mGkmkWbOmhasQNO5QVr78R5ENGfIBD_')
