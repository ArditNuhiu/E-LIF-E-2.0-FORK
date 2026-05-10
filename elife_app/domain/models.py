from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    gender: str  # male / female


class DailyEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    date: date
    sleep_quality: int = Field(ge=0, le=10)
    stress: int = Field(ge=0, le=10)
    friends: int = Field(ge=0, le=1)
    water_intake: float = Field(ge=0, le=5)
    exercise: int = Field(ge=0, le=1)
    mood: int = Field(ge=0, le=10)
    work_hours: float = Field(ge=0, le=16)
    hobbies: int = Field(ge=0, le=1)
    steps: int = Field(ge=0, le=50000)
    meds: int = Field(ge=0, le=1)
    period: int = Field(ge=0, le=1)
    period_pain: Optional[int] = Field(default=None, ge=0, le=10)
    period_flow: Optional[int] = Field(default=None, ge=0, le=3)
    score: int = Field(default=0)
