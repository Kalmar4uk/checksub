import os
import sys
from pathlib import Path

from api.routers import social_networks, tokens, users
from api.routers.routers import (router_social_network, router_token,
                                 router_user)
from dotenv import load_dotenv
from fastapi import FastAPI
from redis import ConnectionError, Redis

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# FastApi init
app = FastAPI(root_path="/api")

# Include routers
app.include_router(router_user)
app.include_router(router_token)
app.include_router(router_social_network)

# JWT parameters
SECRET_KEY_JWT = os.getenv("SECRET_KEY_JWT")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1500
REFRESH_TOKEN_EXPIRE_DAYS = 7
