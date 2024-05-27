from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    API_URI: str
    OPENAI_API_KEY: str
    ENVIRONMENT: str


config: Config = Config()
