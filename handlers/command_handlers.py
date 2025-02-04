from database import get_all_users
from handlers import router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from res import str_user_info, Commands
from state import UserId, User, Resume


@router.message(Command(Commands.INSERT_USER.value))
async def on_insert_user(message: Message, state: FSMContext):
    await state.set_state(User.name)
    await message.answer("Введите имя пользователя")

@router.message(Command(Commands.INSERT_RESUME.value))
async def on_insert_resume(message: Message, state: FSMContext):
    await message.answer("Введите id пользователя, которому хотите добавить резюме")
    await state.set_state(Resume.owner_id)

@router.message(Command(Commands.GET_ALL_USERS.value))
async def on_get_all_users(message: Message):
    users = await get_all_users()
    for user in users:
        await message.answer(str_user_info(user))

@router.message(Command(Commands.EDIT_RESUME.value))
async def on_edit_resume(message: Message, state: FSMContext):
    await message.answer("Введите id пользователя, резюме которого хотите изменить")
    await state.set_state(UserId.user_id)

