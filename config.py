from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    secret_token : str
    admin_username : str
    admin_password : str
    database_url : str

class config:
    env_file = ".env"

settings = Settings()
    