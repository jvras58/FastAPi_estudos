from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Classe que representa as configurações setadas no .env da aplicação.
    """

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encode='utf-8', secrets_dir='.secrets'
    )

    DATABASE_URL: str

    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # SECRETS
    SECRET_KEY: str

    # Permissões
    ADMINISTRADOR: str = 'administrador'
    CLIENTE: str = 'cliente'


@lru_cache
def get_settings() -> Settings:
    return Settings()
