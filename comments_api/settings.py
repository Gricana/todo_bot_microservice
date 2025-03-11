from pydantic import ValidationError
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str =  "postgres"
    DB_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_TIMEOUT: int

    DJANGO_BACKEND_URL: str
    DEBUG: bool = True

    class Config:
        env_file = "infra/api/comments_api.env"

    def model_post_init(self, __context):
        object.__setattr__(
            self,
            "DATABASE_URL",
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}",
        )
        object.__setattr__(
            self, "REDIS_URL", f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"
        )


try:
    settings = Settings()
    print("Settings loaded successfully.")
except ValidationError as e:
    print("Error loading settings:", e)
