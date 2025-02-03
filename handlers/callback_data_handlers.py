from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database import get_resume_by_id, Workload, ResumeUpdateModel, update_resume
from handlers import router
from res import edit_resume_kb, edit_resume_message, EditResumePrefixes, EditWorkloadPrefixes, SelectResumePrefixes, \
    EditSkillsPrefixes
from core import parse_callback_data, CallbackPrefixFilter
from res.keyboards.inline import edit_workload_kb, choice_skills_edit_mode_kb, edit_skills_remove_kb
from state import EditResume


@router.callback_query(CallbackPrefixFilter(SelectResumePrefixes.SELECT_RESUME.value))
async def on_resume_selected(callback: CallbackQuery, state: FSMContext):
    data_builder = parse_callback_data(callback.data)
    id = int(data_builder["id"])
    resume = await get_resume_by_id(id)

    await state.set_state(EditResume.choice_what_to_edit)
    await state.update_data(
        id=resume.id,
        title=resume.title,
        skills=resume.get_skills(),
        workload=resume.workload.value
    )

    await callback.message.answer(
        text=edit_resume_message(resume.title, resume.workload.value, ", ".join(resume.get_skills())),
        reply_markup=edit_resume_kb
    )
    await callback.answer()


@router.callback_query(CallbackPrefixFilter(EditResumePrefixes.EDIT_TITLE.value))
async def on_edit_title(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введите новое название")
    await state.set_state(EditResume.edit_title)

    await callback.answer()


@router.callback_query(CallbackPrefixFilter(EditResumePrefixes.EDIT_WORKLOAD.value))
async def on_edit_workload(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Выберите новую рабоучю нагрузку.",
        reply_markup=edit_workload_kb
    )
    await callback.answer()


@router.callback_query(CallbackPrefixFilter(EditWorkloadPrefixes.SET_WORKLOAD_FULL_TIME.value))
async def on_set_workload_full_time(callback: CallbackQuery, state: FSMContext):
    await state.update_data(workload=Workload.FULL_TIME.value)
    updated_resume = await state.get_data()

    await callback.message.edit_text(
        text=edit_resume_message(
            updated_resume["title"],
            updated_resume["workload"],
            ", ".join(updated_resume["skills"])
        ),
        reply_markup=edit_resume_kb
    )
    await callback.answer()


@router.callback_query(CallbackPrefixFilter(EditWorkloadPrefixes.SET_WORKLOAD_PART_TIME.value))
async def on_set_workload_part_time(callback: CallbackQuery, state: FSMContext):
    await state.update_data(workload=Workload.PART_TIME.value)
    updated_resume = await state.get_data()

    await callback.message.edit_text(
        text=edit_resume_message(
            updated_resume["title"],
            updated_resume["workload"],
            ", ".join(updated_resume["skills"])
        ),
        reply_markup=edit_resume_kb
    )
    await callback.answer()


@router.callback_query(CallbackPrefixFilter(EditWorkloadPrefixes.BACK_TO_EDIT_RESUME.value))
async def on_back_to_edit_resume(callback: CallbackQuery, state: FSMContext):
    data_builder = parse_callback_data(callback.data)
    if data_builder["rollback_state"]:
        await state.set_state(EditResume.choice_what_to_edit)

    updated_resume = await state.get_data()

    await callback.message.edit_text(
        text=edit_resume_message(
            updated_resume["title"],
            updated_resume["workload"],
            ", ".join(updated_resume["skills"])
        ),
        reply_markup=edit_resume_kb
    )
    await callback.answer()


@router.callback_query(CallbackPrefixFilter(EditResumePrefixes.EDIT_SKILLS.value))
async def on_edit_skills(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Выберите действие",
        reply_markup=choice_skills_edit_mode_kb
    )
    await callback.answer()


@router.callback_query(CallbackPrefixFilter(EditSkillsPrefixes.CHOOSE_ADD.value))
async def on_edit_skills_add(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введите один новый скилл, или несколько через запятую")
    await state.set_state(EditResume.edit_skills_add)
    await callback.answer()


@router.callback_query(CallbackPrefixFilter(EditSkillsPrefixes.CHOOSE_REMOVE.value))
async def on_edit_skills_remove(callback: CallbackQuery, state: FSMContext):
    await state.update_data(will_remove_skills=[])
    resume = await state.get_data()

    await callback.message.edit_text(
        text="Выберите скллы для удаления",
        reply_markup=edit_skills_remove_kb(resume["skills"], [])
    )
    await callback.answer()


@router.callback_query(CallbackPrefixFilter(EditSkillsPrefixes.REMOVE_SKILL.value))
async def on_remove_skill(callback: CallbackQuery, state: FSMContext):
    data_builder = parse_callback_data(callback.data)
    skill_to_delete = data_builder["skill"]

    resume = await state.get_data()
    skills = resume["skills"]
    will_remove_skills = resume["will_remove_skills"] + [skill_to_delete]
    await state.update_data(will_remove_skills=will_remove_skills)

    await callback.message.edit_text(
        text="Выберите скллы для удаления",
        reply_markup=edit_skills_remove_kb(skills, will_remove_skills)
    )

    await callback.answer()

@router.callback_query(CallbackPrefixFilter(EditSkillsPrefixes.SAVE_CHANGES.value))
async def on_save_skill_changes(callback: CallbackQuery, state: FSMContext):
    updated_resume = await state.get_data()
    skills = updated_resume["skills"]
    will_remove_skills = updated_resume["will_remove_skills"]
    for skill in will_remove_skills:
        skills.remove(skill)
    await state.update_data(skills=skills, will_remove_skills=[])

    await callback.message.edit_text(
        text=edit_resume_message(
            updated_resume["title"],
            updated_resume["workload"],
            ", ".join(updated_resume["skills"])
        ),
        reply_markup=edit_resume_kb
    )
    await callback.answer()

@router.callback_query(CallbackPrefixFilter(EditResumePrefixes.SAVE_RESUME_CHANGES.value))
async def on_save_resume_changes(callback: CallbackQuery, state: FSMContext):
    updated_resume = await state.get_data()
    await state.clear()

    update_model = ResumeUpdateModel(
        title=updated_resume["title"],
        skills=updated_resume["skills"],
        workload=Workload.value_of(updated_resume["workload"])
    )
    await update_resume(updated_resume["id"], update_model)
    await callback.message.edit_text("Изменения сохранены!")
    await callback.answer()



