from fastapi import APIRouter

router_token = APIRouter(prefix="/token", tags=["Токены"])
router_user = APIRouter(prefix="/users", tags=["Пользователи"])
router_social_network = APIRouter(prefix="/social_networks", tags=["Социальные сети"])
