import pydantic # type: ignore[import]
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

class Writter(BaseModel):
    caption: str = Field(Description='Legenda do post', max_length=2200)
    
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
    post_content: str = Field(Description='Texto do contéudo da postagem', max_length=2200)
    prompt_image: str = Field(Description='Prompt para geração de imagem', max_length=1000)
    hashtags: list[str] = Field(Description='Lista de #palavraschaves hashtags', max_length=30)

    
    @field_validator("post_content", "prompt_image", mode="before")
    def parse_str(cls, v):
        return str(v)

    @field_validator("hashtags", mode="before")
    def parse_hashtags(cls, v):
        if isinstance(v, str):
            return [tag.strip() for tag in v.split(",")]
        return v
    
    class Config:
        extra = pydantic.Extra.forbid
        arbitrary_types_allowed = True
        validate_assignment = True
    
