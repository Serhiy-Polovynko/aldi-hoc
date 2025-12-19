from functools import lru_cache
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator, computed_field

from aldi_hoc_companion.core.ai_models import MODEL_PRICING

# Get the project root directory (where .env should be located)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = PROJECT_ROOT / ".env"
LOGS_DIR = PROJECT_ROOT / "logs"

# Load .env into os.environ (needed for libraries like openai that read env directly)
load_dotenv(ENV_FILE_PATH)




# Allowed model names for validation
ALLOWED_MODELS = Literal[
    "gpt-5.2", "gpt-5.1", "gpt-5", "gpt-5-mini", "gpt-5-nano", "gpt-5.2-pro", "gpt-5-pro",
    "gpt-4o", "gpt-4o-mini",
    "gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano",
    "o1", "o1-mini", "o3", "o3-mini", "o4-mini",
    "gpt-3.5-turbo"
]


class Settings(BaseSettings):
    """
    Central application configuration using pydantic-settings.
    Automatically loads values from .env with validation & typing.
    """
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    # -----------------------
    # Environment
    # -----------------------
    environment: str = Field(default="dev")
    log_level: str = Field(default="INFO")

    # -----------------------
    # Database
    # -----------------------
    db_host: str = Field(default="localhost")
    db_port: int = Field(default=5432)
    db_name: str = Field(default="aldi_hoc_companion")
    db_user: str = Field()
    db_password: str = Field()

    # -----------------------
    # OpenAI Model Configuration
    # -----------------------
    openai_api_key: str | None = Field(default=None)
    openai_model: str = Field(default="gpt-4o-mini", description="Model to use: gpt-4o or gpt-4o-mini")
    openai_base_url: str | None = Field(default=None)

    # -----------------------
    # Logging
    # -----------------------
    log_dir: Path = Field(default=LOGS_DIR, description="Directory for log files")

    # -----------------------
    # Validators
    # -----------------------
    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str):
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        v = v.upper()
        if v not in allowed:
            raise ValueError(f"log_level must be one of {allowed}")
        return v

    @field_validator("openai_model")
    @classmethod
    def validate_openai_model(cls, v: str):
        allowed = set(MODEL_PRICING.keys())
        if v not in allowed:
            raise ValueError(f"openai_model must be one of {allowed}")
        return v

    # -----------------------
    # Computed Properties
    # -----------------------
    @computed_field
    @property
    def model_input_cost_per_token(self) -> float:
        """Cost per input token in USD."""
        return MODEL_PRICING[self.openai_model]["input_per_million"] / 1_000_000

    @computed_field
    @property
    def model_output_cost_per_token(self) -> float:
        """Cost per output token in USD."""
        return MODEL_PRICING[self.openai_model]["output_per_million"] / 1_000_000

    @computed_field
    @property
    def model_description(self) -> str:
        """Human-readable model description."""
        return MODEL_PRICING[self.openai_model]["description"]

    @computed_field
    @property
    def pydantic_ai_model_string(self) -> str:
        """Model string for Pydantic-AI (e.g., 'openai:gpt-4o')."""
        return f"openai:{self.openai_model}"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


def get_model_pricing() -> dict:
    return MODEL_PRICING
