from pydantic_settings import BaseSettings
from dotenv import load_dotenv


# Define the absolute path to the .env file
env_path = r"ML\Database\.env"

# Explicitly load the .env file
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    ML_DATABASE_HOSTNAME: str
    ML_DATABASE_PORT: int
    ML_DATABASE_PASSWORD: str
    ML_DATABASE_NAME: str
    ML_DATABASE_USERNAME: str
    ML_SECRET_KEY: str
    ML_ALGORITHM: str
    ML_ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = env_path  # Use the same absolute path here

settings = Settings() # type: ignore[call-arg]