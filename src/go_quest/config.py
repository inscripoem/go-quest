import binascii
import functools
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

from advanced_alchemy.utils.text import slugify
from litestar.utils.module_loader import module_to_os_path

from go_quest.lib.envs import get_env


# ======== Constants ========


DEFAULT_MODULE_NAME = "go_quest"
BASE_DIR: Final[Path] = module_to_os_path(DEFAULT_MODULE_NAME)


# ======== Settings ========


@dataclass
class AppSettings:
    """Application configuration"""

    APP_LOC: str = "go_quest.asgi:create_app"
    """Path to app executable, or factory."""
    NAME: str = field(default_factory=get_env("LITESTAR_APP_NAME", "GoQuest"))
    """Application name."""
    URL: str = field(default_factory=get_env("APP_URL", "http://localhost:8000"))
    """The frontend base URL"""
    DEBUG: bool = field(default_factory=get_env("LITESTAR_DEBUG", False))
    """Run `Litestar` with `debug=True`."""
    SECRET_KEY: str = field(
        default_factory=get_env("SECRET_KEY", binascii.hexlify(os.urandom(32)).decode(encoding="utf-8")),
    )
    """Application secret key."""

    @property
    def slug(self) -> str:
        """Return a slugified name.

        Returns:
            `self.NAME`, all lowercase and hyphens instead of spaces.
        """
        return slugify(self.NAME)


@dataclass
class ServerSettings:
    """Server configurations."""

    HOST: str = field(default_factory=get_env("LITESTAR_HOST", "0.0.0.0"))
    """Server network host."""
    PORT: int = field(default_factory=get_env("LITESTAR_PORT", 8000))
    """Server port."""
    RELOAD: bool = field(default_factory=get_env("LITESTAR_RELOAD", False))
    """Turn on hot reloading."""
    RELOAD_DIRS: list[str] = field(default_factory=get_env("LITESTAR_RELOAD_DIRS", [f"{BASE_DIR}"]))
    """Directories to watch for reloading."""
    SCALAR_PATH: str = field(default_factory=get_env("SCALAR_PATH", "/scalar"))
    """Path to serve OpenAPI scalars."""


@dataclass
class Settings:
    app: AppSettings = field(default_factory=AppSettings)
    server: ServerSettings = field(default_factory=ServerSettings)

    @classmethod
    def from_env(cls, dotenv_filename: str = ".env") -> "Settings":
        from litestar.cli._utils import console

        env_file = Path(f"{os.curdir}/{dotenv_filename}")
        if env_file.is_file():
            from dotenv import load_dotenv

            console.print(f"[yellow]Loading environment configuration from {dotenv_filename}[/]")

            load_dotenv(env_file, override=True)
        return Settings()


@functools.lru_cache(maxsize=1, typed=True)
def get_settings() -> Settings:
    return Settings.from_env()
