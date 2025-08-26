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
    def __init__(
            self,
            social_network_id: int | None = None,
            username: str | None = None,
            title: str | None = None
    ):
        if social_network_id:
            super().__init__(
                status_code=404,
                detail=f"Социальная сеть с id {social_network_id} не найдена"
            )
        elif username and title:
            super().__init__(
                status_code=404,
                detail=(
                    f"В социальной сети {title} "
                    f"нет пользователя с логином/id {username} "
                    f"или он удален"
                )
            )
        elif username:
            super().__init__(
                status_code=404,
                detail=(
                    f"Социальная сеть {username} не добавлялась "
                    f"или была удалена ранее"
                )
            )
        else:
            super().__init__(
                status_code=404,
                detail="Полученные социальные сети не найдены"
            )
