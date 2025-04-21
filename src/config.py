from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Settings for the FastAPI application."""

    debug: bool = False
    title: str = "A2A Server Management"
    summary: str | None = None
    description: str | None = None
    version: str = "0.1.0"
    terms_of_service: str | None = None
    contact: dict | None = None
    license_info: dict | None = None
    root_path: str | None = None

    def kwargs(self) -> dict:
        """Convert settings to a dictionary for FastAPI initialization."""
        return self.model_dump(exclude_none=True)


class Settings(BaseSettings):
    """Main settings class."""

    app_settings: AppSettings = AppSettings()


settings = Settings()
