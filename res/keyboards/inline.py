from res import EditResumePrefixes, EditWorkloadPrefixes, SelectResumePrefixes, EditSkillsPrefixes
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from core import callback_data


def select_resume_kb(resumes):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=resume.title,
            callback_data=callback_data(SelectResumePrefixes.SELECT_RESUME.value, id=resume.id)
        )] for resume in resumes
    ])

edit_resume_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Изменить название ✏️",
        callback_data=callback_data(EditResumePrefixes.EDIT_TITLE.value)
    )],
    [InlineKeyboardButton(
        text="Изменить рабоую нагрузку ✏️",
        callback_data=callback_data(EditResumePrefixes.EDIT_WORKLOAD.value)
    )],
    [InlineKeyboardButton(
        text="Измеить скиллы ✏️",
        callback_data=callback_data(EditResumePrefixes.EDIT_SKILLS.value)
    )],
    [InlineKeyboardButton(
        text="Сохранить ✔️",
        callback_data=callback_data(EditResumePrefixes.SAVE_RESUME_CHANGES.value)
    )]
])

edit_workload_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Part time",
        callback_data=callback_data(EditWorkloadPrefixes.SET_WORKLOAD_PART_TIME.value)
    )],
    [InlineKeyboardButton(
        text="Full time",
        callback_data=callback_data(EditWorkloadPrefixes.SET_WORKLOAD_FULL_TIME.value)
    )],
    [InlineKeyboardButton(
        text="Назад 🔙",
        callback_data=callback_data(EditWorkloadPrefixes.BACK_TO_EDIT_RESUME.value, rollback_state=False)
    )]
])

choice_skills_edit_mode_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Добавить ➕",
        callback_data=callback_data(EditSkillsPrefixes.CHOOSE_ADD.value)
    )],
    [InlineKeyboardButton(
        text="Удалить 🗑",
        callback_data=callback_data(EditSkillsPrefixes.CHOOSE_REMOVE.value)
    )],
    [InlineKeyboardButton(
        text="Назад 🔙",
        callback_data=callback_data(EditSkillsPrefixes.BACK_TO_EDIT_RESUME.value, rollback_state=False)
    )],
])


def edit_skills_remove_kb(skills, will_remove_skills):
    kb = [
        [InlineKeyboardButton(
            text=skill + (" ✅" if skill in will_remove_skills else " ❌"),
            callback_data=callback_data(EditSkillsPrefixes.REMOVE_SKILL.value, skill=skill)
        )] for skill in skills
    ]
    kb.append([InlineKeyboardButton(
        text="Сохранить изменения ✔️",
        callback_data=callback_data(EditSkillsPrefixes.SAVE_CHANGES.value)
    )])
    kb.append([InlineKeyboardButton(
        text="Назад 🔙",
        callback_data=callback_data(EditSkillsPrefixes.BACK_TO_EDIT_RESUME.value, rollback_state=True)
    )])
    return InlineKeyboardMarkup(inline_keyboard=kb)
