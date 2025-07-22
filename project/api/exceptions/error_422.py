from fastapi import HTTPException


class UniqueEmailEmployee(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=422,
            detail="Email уже используется"
        )
