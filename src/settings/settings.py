import abc
import os
from typing import List

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = Field("positron")
    VERSION: str = Field("1.1")
    DEBUG: bool = Field(True)


class PostgresSettings(BaseSettings):
    USER: str = Field(validation_alias="POSTGRES_USER")
    PASSWORD: str = Field(validation_alias="POSTGRES_PASSWORD")
    HOST: str = Field(validation_alias="POSTGRES_HOST")
    PORT: str = Field(validation_alias="POSTGRES_PORT")
    DB_NAME: str = Field(validation_alias="POSTGRES_DB_NAME")
    ECHO_LOG: bool = Field(
        validation_alias=AliasChoices("POSTGRES_ECHO_LOG", "POSTGRES_LOG")
    )
    
    @property
    def URL(self):
        return (
            f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@"
            f"{self.HOST}:{self.PORT}/{self.DB_NAME}"
        )
    

settings = Settings()
postgres_settings = PostgresSettings()
