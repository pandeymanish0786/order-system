from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://order_user:order_pass@order-db:5432/order_db"
    service_name: str = "order-service"
    environment: str = "local"
    inventory_service_url: str = "http://inventory-service:8000"

    class Config:
        env_file = ".env"

settings = Settings()