import os

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()


# FastApi init
app = FastAPI(root_path="/api")

# JWT parameters
SECRET_KEY_JWT = os.getenv("SECRET_KEY_JWT")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1500
REFRESH_TOKEN_EXPIRE_DAYS = 7
