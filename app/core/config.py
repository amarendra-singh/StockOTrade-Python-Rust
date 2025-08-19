import os 
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./stockotrade.db")
    
    # Add other configuration variables as needed
    PROJECT_NAME: str = "StockOTrade"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

settings = Settings()

