from typing import Optional

from pydantic import BaseModel


class CourseCreate(BaseModel):
    title: str
    description: str
    duration_hours: int


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration_hours: Optional[int] = None
    status: Optional[str] = None
