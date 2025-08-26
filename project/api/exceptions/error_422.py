from fastapi import HTTPException


class UniqueEmailEmployee(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=422,
            detail="Email уже используется"
        )


class CountFollowersOrLikesMoreZero(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=422,
            detail=(
                "Запрещено редактировать соц.сеть если кол-во "
                "подписчиков и/или лайков больше нуля"
            )
        )


class SocialNetworkAddedEarlier(HTTPException):
    def __init__(self, title: str, username: str):
        super().__init__(
            status_code=422,
            detail=(
                f"Социальная сеть уже была добавлена. "
                f"Соц.сеть - {title}, логин/id - {username}"
            )
        )
