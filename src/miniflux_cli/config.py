"""Configuration management via Pydantic Settings."""

from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_CONFIG_PATH = Path.home() / ".config" / "miniflux-cli" / "config.toml"


class Config(BaseSettings):
    """Miniflux CLI configuration."""

    model_config = SettingsConfigDict(
        env_prefix="MINIFLUX_",
        env_file=".env",
        extra="ignore",
    )

    url: str
    api_key: str | None = None
    username: str | None = None
    password: str | None = None
    timeout: float = 30.0

    @field_validator("url")
    @classmethod
    def _strip_trailing_slash(cls, v: str) -> str:
        return v.rstrip("/")

    def get_client_kwargs(self) -> dict:
        """Return kwargs suitable for miniflux.Client initialization."""
        kwargs: dict = {"base_url": self.url, "timeout": self.timeout}
        if self.api_key:
            kwargs["api_key"] = self.api_key
        elif self.username and self.password:
            kwargs["username"] = self.username
            kwargs["password"] = self.password
        else:
            raise ValueError("Either api_key or both username and password must be provided.")
        return kwargs
