from dataclasses import dataclass

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from enum import Enum
import json

class Base(DeclarativeBase):
    pass

class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))
    resumes: Mapped[list["ResumeOrm"]] = relationship("ResumeOrm")

    @staticmethod
    def build(name):
        return UserOrm(name=name)

class Workload(Enum):
    FULL_TIME = "fulltime"
    PART_TIME = "parttime"

    @classmethod
    def value_of(cls, of: str):
        if of == cls.FULL_TIME.value:
            return cls.FULL_TIME
        elif of == cls.PART_TIME.value:
            return cls.PART_TIME


@dataclass
class ResumeOrm(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    workload: Mapped[Workload] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    _skills: Mapped[str] = mapped_column(server_default="[]")

    def set_skills(self, skills: list[str]):
        self._skills = json.dumps(skills)

    def get_skills(self) -> list[str]:
        return json.loads(self._skills)

    @classmethod
    def build(cls, title, skills, workload, user_id):
        return cls(title=title, workload=workload, user_id=user_id, _skills=json.dumps(skills))




