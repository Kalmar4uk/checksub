from fastapi import HTTPException


class UserNotFound(HTTPException):
    def __init__(self, user_id: int | None = None, email: str | None = None):
        if email:
            super().__init__(
                status_code=404,
                detail=f"Пользователь с email {email} не найден"
            )
        else:
            super().__init__(
                status_code=404,
                detail=f"Пользователь с id {user_id} не найден"
            )


class SocialNetworkNotFound(HTTPException):
    def __init__(self, social_network_id: int):
        super().__init__(
            status_code=404,
            detail=f"Социальная сеть с id {social_network_id} не найдена"
        )
