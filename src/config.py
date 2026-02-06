from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """
    Loads our base settings from the ENV in production or
    the .env file in development.
    """

    mode: str = Field(..., validation_alias="MODE")

    db_user: str = Field(..., validation_alias="DB_USER")
    db_pw: str = Field(..., validation_alias="DB_PW")
    db_host: str = Field(..., validation_alias="DB_HOST")
    db_port: int = Field(5432, validation_alias="DB_PORT")
    db_name: str = Field(..., validation_alias="DB_NAME")
    db_service_name: str = Field(..., validation_alias="DB_SERVICE_NAME")

    jwt_algorithm: str = Field(..., validation_alias="JWT_ALGORITHM")
    jwt_secret_key: str = Field(..., validation_alias="JWT_SECRET_KEY")

    bootstrap_token: str = Field(..., validation_alias="BOOTSTRAP_TOKEN")

    class config:
        env_file = "...env"


settings = Settings()  # type: ignore
