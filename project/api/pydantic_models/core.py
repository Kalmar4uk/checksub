from pydantic import BaseModel, Field


class Base(BaseModel):
    """Базовая модель которая добавляет id"""
    id: int = Field(examples=[1])
