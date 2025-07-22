from fastapi import HTTPException


class ExceptionSaveDataBase(HTTPException):
    def __init__(self, error):
        super().__init__(
            status_code=500,
            detail=f"Произошла ошибка при сохранении записи в БД: {error}"
        )
