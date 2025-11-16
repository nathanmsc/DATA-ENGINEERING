import os
import boto3
from io import BytesIO
from functools import cached_property
from typing import Optional, Dict, Any

from dotenv import load_dotenv  # type: ignore

# Carrega variáveis do .env
load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# =====================================================
# CLOUD FLARE API Client (organizado)
# =====================================================
class CloudflareAPIClient:
    """Cliente unificado Cloudflare R2"""

    @cached_property
    def r2(self):
        """Cliente boto3 para Cloudflare R2, criado apenas uma vez."""
        return boto3.client(
            "s3",
            endpoint_url=f"https://{os.getenv('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com",
            aws_access_key_id=os.getenv("R2_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("R2_SECRET_ACCESS_KEY"),
            region_name="auto",
        )

    # -------------------------------------------------
    # UPLOAD LOCAL FILE → R2
    # -------------------------------------------------
    def upload_file(self, local_path: str, object_name: str) -> str:
        bucket = os.getenv("R2_BUCKET")

        self.r2.upload_file(local_path, bucket, object_name)

        return f"{os.getenv('R2_PUBLIC_DOMAIN')}/{object_name}"

    # -------------------------------------------------
    # UPLOAD BYTES → R2
    # -------------------------------------------------
    def upload_bytes(self, data: bytes, object_name: str) -> str:
        bucket = os.getenv("R2_BUCKET")

        self.r2.put_object(
            Bucket=bucket,
            Key=object_name,
            Body=data,
            ContentType="image/png",
        )

        return f"{os.getenv('R2_PUBLIC_DOMAIN')}/{object_name}"

    # -------------------------------------------------
    # LIST OBJECTS
    # -------------------------------------------------
    def list_objects(self, prefix: str = ""):
        bucket = os.getenv("R2_BUCKET")
        return self.r2.list_objects_v2(Bucket=bucket, Prefix=prefix).get("Contents", [])

    # -------------------------------------------------
    # DELETE SINGLE OBJECT
    # -------------------------------------------------
    def delete_object(self, object_name: str):
        bucket = os.getenv("R2_BUCKET")
        self.r2.delete_object(Bucket=bucket, Key=object_name)
        return f"Objeto removido: {object_name}"

    # -------------------------------------------------
    # DELETE DIRECTORY (PREFIX)
    # -------------------------------------------------
    def delete_directory(self, prefix: str):
        """
        Remove todos os arquivos dentro de um diretório (prefixo) no R2.
        Exemplo: prefix="static/img/"
        """
        bucket = os.getenv("R2_BUCKET")

        response = self.r2.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix
        )

        if "Contents" not in response:
            return f"Nenhum arquivo encontrado no prefixo {prefix}"

        objects_to_delete = [{"Key": obj["Key"]} for obj in response["Contents"]]

        self.r2.delete_objects(
            Bucket=bucket,
            Delete={"Objects": objects_to_delete}
        )

        return f"Diretório '{prefix}' removido com {len(objects_to_delete)} arquivos."


