from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    endpoint_extra_source_service: str

settings = Settings()