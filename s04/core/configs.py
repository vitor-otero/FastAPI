from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    """
    General configuration settings
    """
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://tests:12345678@localhost:5432/testsDB'
    DBBaseModel = declarative_base()

    class Config:
        case_sensitive = True

settings = Settings()