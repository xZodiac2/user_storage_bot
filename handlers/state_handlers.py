import re
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import Message
from database import get_user_by_id, resume_title_max_length, name_max_length, UserOrm, insert_user, ResumeOrm, \
    Workload, insert_resume
from handlers import router
from res import str_edit_resume_message, edit_resume_ikb, str_select_resume_message, select_resume_ikb, \
    create_resume_select_workload_ikb
from state import UserId, EditResume, User, Resume


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
            text=str_select_resume_message(user),
            reply_markup=select_resume_ikb(user.resumes)
        )
    except ValueError:
        await message.answer("Неверный формат id")


@router.message(StateFilter(EditResume.edit_title))
async def handle_edit_resume_title_state(message: Message, state: FSMContext):
    if len(message.text) > resume_title_max_length:
        await message.answer("Название не должно быть больше 100 символов")
        return

    await state.update_data(title=message.text)
    updated_resume = await state.get_data()
    await state.set_state(EditResume.choice_what_to_edit)

    await message.answer(
        text=str_edit_resume_message(
            updated_resume["title"],
            updated_resume["workload"],
            ", ".join(updated_resume["skills"])
        ),
        reply_markup=edit_resume_ikb
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
        text=str_edit_resume_message(
            updated_resume["title"],
            updated_resume["workload"],
            ", ".join(updated_resume["skills"]),
        ),
        reply_markup=edit_resume_ikb
    )


@router.message(StateFilter(User.name))
async def handle_user_name_state(message: Message, state: FSMContext):
    if len(message.text) > name_max_length:
        await message.answer(f"Длина имени не должна превышать {name_max_length} символов")
        return

    await state.update_data(name=message.text)
    await state.set_state(User.age)
    await message.answer("Теперь введите возраст пользователя")


@router.message(StateFilter(User.age))
async def handle_user_age_state(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        await state.update_data(age=age)
        await state.set_state(User.email)
        await message.answer("Теперь введите email")
    except ValueError:
        await message.answer("Возраст должен быть целочисленным, например: 20")


@router.message(StateFilter(User.email))
async def handle_user_email_state(message: Message, state: FSMContext):
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not bool(re.match(email_pattern, message.text)):
        await message.answer("Некорректный формат email")
        return

    await state.update_data(email=message.text)
    data = await state.get_data()
    await state.clear()

    user = UserOrm.build(data["name"], data["age"], data["email"])
    await insert_user(user)
    await message.answer(f"Пользователь успешно зарегестрирован! Id: {user.id}")


@router.message(StateFilter(Resume.owner_id))
async def handle_resume_owner_id_state(message: Message, state: FSMContext):
    try:
        id = int(message.text)
        await state.update_data(owner_id=id)
        await state.set_state(Resume.title)
        await message.answer("Теперь введи название резюме")
    except ValueError:
        await message.answer("Неверный формат id. Необходимо целочисленное значение")


@router.message(StateFilter(Resume.title))
async def handle_resume_title_state(message: Message, state: FSMContext):
    if len(message.text) > resume_title_max_length:
        await message.answer(f"Длина название не должна превышать {resume_title_max_length} символов")
        return

    await state.update_data(title=message.text)
    await state.set_state(Resume.workload)
    await message.answer(
        text="Теперь выбери рабочую нагрзку",
        reply_markup=create_resume_select_workload_ikb
    )

@router.message(StateFilter(Resume.skills))
async def handle_resume_skills_state(message: Message, state: FSMContext):
    if "," in message.text:
        skills = message.text.split(",")
    else:
        skills = [message.text]
    await state.update_data(skills=skills)
    data = await state.get_data()
    await state.clear()

    resume = ResumeOrm.build(
        data["title"],
        data["skills"],
        Workload.value_of(data["workload"]),
        data["owner_id"]
    )
    await insert_resume(resume)
    await message.answer(f"Резюме добавлено! Id: {resume.id}")