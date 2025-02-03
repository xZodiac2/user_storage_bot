from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from database import ResumeUpdateModel, get_resume_by_id, get_user_by_id, update_resume
from handlers import router
from res import edit_resume_message, edit_resume_kb, select_resume_message
from res.keyboards.inline import select_resume_kb
from state import UserId, EditResume
from core import callback_data


@router.message(StateFilter(UserId.user_id))
async def handle_user_id_state(message: Message, state: FSMContext):
    try:
        id = int(message.text)
        user = await get_user_by_id(id)
        if not user:
            await message.answer("Пользователь не найден")
            return
        await state.clear()

        await message.answer(
            text=select_resume_message(user),
            reply_markup=select_resume_kb(user.resumes)
        )
    except ValueError:
        await message.answer("Неверный формат id")


@router.message(StateFilter(EditResume.edit_title))
async def handle_edit_resume_title_state(message: Message, state: FSMContext):
    if len(message.text) > 100:
        await message.answer("Название не должно быть больше 100 символов")
        return

    await state.update_data(title=message.text)
    updated_resume = await state.get_data()
    await state.set_state(EditResume.choice_what_to_edit)

    await message.answer(
        text=edit_resume_message(
            updated_resume["title"],
            updated_resume["workload"],
            ", ".join(updated_resume["skills"])
        ),
        reply_markup=edit_resume_kb
    )

@router.message(StateFilter(EditResume.edit_skills_add))
async def handle_edit_resume_skills_state(message: Message, state: FSMContext):
    old_skills = (await state.get_data())["skills"]
    if "," in message.text:
        new_skills = old_skills + [skill.strip() for skill in message.text.split(",")]
    else:
        new_skills = old_skills + [message.text]

    await state.update_data(skills=new_skills)
    await state.set_state(EditResume.choice_what_to_edit)
    updated_resume = await state.get_data()

    await message.answer(
        text=edit_resume_message(
            updated_resume["title"],
            updated_resume["workload"],
            ", ".join(updated_resume["skills"]),
        ),
        reply_markup=edit_resume_kb
    )
