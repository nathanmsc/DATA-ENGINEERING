import json
import pydantic # type: ignore[import]
from typing import Dict, Any
from pydantic import BaseModel, field_validator, Field # type: ignore[import]

class Caption(BaseModel):
    
    topic: str = Field(Description='Tópico principal do post', max_length=100)
    description: str = Field(Description='Descrição detalhada do post', max_length=500)
    prompt_image: str = Field(Description='Prompt para geração de imagem por IA', max_length=1000)
    voice: str = Field(Description='Voz do texto (ex: Descolado e acessível, Educativo e leve)', max_length=50)
    audience: str = Field(Description='Público alvo (ex: pacientes, adultos)', max_length=100)
    platform: str = Field(Description='Plataforma de destino (ex: Instagram)', max_length=50)
    
    @field_validator("topic", "description", "prompt_image", "voice", "audience", "platform", mode="before")
    def parse_str(cls, v):
        return str(v)
    
    class Config:
        extra = pydantic.Extra.forbid
        arbitrary_types_allowed = True
        validate_assignment = True

class Writer(BaseModel):
    caption: str = Field(Description='Legenda do post', max_length=1024)
    
    @field_validator("caption", mode="before")
    def parse_str(cls, v):
        return str(v)
    
    class Config:
        extra = pydantic.Extra.forbid
        arbitrary_types_allowed = True
        validate_assignment = True

class Imager(BaseModel):
    prompt_image: str = Field(Description='Prompt para geração de imagem', max_length=1000)
    
    @field_validator("prompt_image", mode="before")
    def parse_str(cls, v):
        return str(v)
    
    class Config:
        extra = pydantic.Extra.forbid
        arbitrary_types_allowed = True
        validate_assignment = True

class Hashtags(BaseModel):
    hashtags: list[str] = Field(Description='Lista de #palavraschaves hashtags', max_length=30)
    
    @field_validator("hashtags", mode="before")
    def parse_hashtags(cls, v):
        if isinstance(v, str):
            return [tag.strip() for tag in v.split(",")]
        return v
    
    class Config:
        extra = pydantic.Extra.forbid
        arbitrary_types_allowed = True
        validate_assignment = True


class Consolidator(BaseModel):
   
    document: Dict[str, str] = Field(default_factory=dict, description="document json chave:valor")

    @field_validator("document", mode="before")
    def parse_dict(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("O campo 'document' deve ser um JSON válido.")
        if isinstance(v, dict):
            return v
        raise ValueError("O campo 'document' deve ser um dicionário ou uma string JSON.")    

    class Config:
        extra = pydantic.Extra.forbid
        arbitrary_types_allowed = True
        validate_assignment = True
    
