from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import get_session
from database import UserOrm
from database.models import ResumeUpdateModel
from database.orm import ResumeOrm


async def insert_user(user: UserOrm):
    async with get_session() as session:
        session.add(user)
        await session.commit()

async def insert_resume(resume: ResumeOrm):
    async with get_session() as session:
        session.add(resume)
        await session.commit()


async def get_all_users() -> list[UserOrm]:
    async with get_session() as session:
        stmt = (
            select(UserOrm)
            .options(selectinload(UserOrm.resumes))
        )
        cursor = await session.execute(stmt)
        return cursor.scalars().all()


async def get_user_by_id(id: int) -> UserOrm | None:
    async with get_session() as session:
        stmt = (
            select(UserOrm)
            .filter_by(id=id)
            .options(selectinload(UserOrm.resumes))
        )
        cursor = await session.execute(stmt)
        return cursor.scalar_one_or_none()


async def get_resume_by_id(id: int) -> ResumeOrm | None:
    async with get_session() as session:
        return await session.get(ResumeOrm, id)


async def update_resume(id: int, new_resume: ResumeUpdateModel):
    async with get_session() as session:
        resume = await session.get(ResumeOrm, id)
        resume.workload = new_resume.workload
        resume.title = new_resume.title
        resume.set_skills(new_resume.skills)
        await session.commit()