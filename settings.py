from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class TokenSettings(BaseModel):
    secret_key: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    token: TokenSettings

    debug: bool
    base_dir: Path = Path(__file__).resolve().parent
    hall_dir: Path = base_dir / "halls"


settings = Settings()  # type: ignore
