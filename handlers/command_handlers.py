import random
from database import UserOrm, insert_user, get_all_users, ResumeOrm, Workload, insert_resume
from handlers import router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from state import UserId

usernames = ["Bobr", "Volk", "ILya", "Nikita", "Artem", "Danil", "Robert"]
def get_name():
    index = random.randint(0, len(usernames) - 1)
    return usernames[index]

@router.message(Command("insert_user"))
async def on_insert_user(message: Message):
    name = get_name()
    user = UserOrm.build(name)
    await insert_user(user)
    await message.answer("Пользователь успешно добавлен")


@router.message(Command("insert_resume"))
async def on_insert_resume(message: Message):
    user_ids = [user.id for user in await get_all_users()]
    random_id = random.choice(user_ids)
    resume = ResumeOrm.build(
        "Telegram-bot developer " + str(random.randint(1, 10000000)),
        ["Python", "Sqlalchemy", "Aiogram"],
        Workload.PART_TIME,
        random_id
    )
    await insert_resume(resume)
    await message.answer("Резюме добавлено")


@router.message(Command("get_all_users"))
async def on_get_all_users(message: Message):
    users = await get_all_users()
    for user in users:
        resumes = [f"{resume.id}. {resume.title}" for resume in user.resumes]
        text = f"""
Id: {user.id}
Name: {user.name}
Resumes: {". ".join(resumes)}"""
        await message.answer(text)


@router.message(Command("edit_resume"))
async def on_edit_resume(message: Message, state: FSMContext):
    await message.answer("Введите id пользователя, резюме которого хотите изменить")
    await state.set_state(UserId.user_id)

