from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://inventory_user:inventory_pass@inventory-db:5432/inventory_db"
    service_name: str = "inventory-service"
    environment: str = "local"

    class Config:
        env_file = ".env"

settings = Settings()