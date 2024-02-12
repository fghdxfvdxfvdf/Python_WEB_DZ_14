# from pydantic import BaseSettings
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str = 'postgresql+psycopg2://postgres:567234@localhost:5432/hw_13'
    secret_key: str = 'secret_key'
    algorithm: str = 'HS256'
    mail_username: str = 'Max_Greb@meta.ua'
    mail_password: str = 'dygcsUYCVZiyvyl484dsvhbdh6dfzv'
    mail_from: str = 'example@meta.ua'
    mail_port: int = 465
    mail_server: str = 'smtp.meta.ua'
    redis_host: str = 'localhost'
    redis_port: int = 6379
    cloudinary_name: str = 'name'
    cloudinary_api_key: int = 326488457974591
    cloudinary_api_secret: str = 'secret'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()