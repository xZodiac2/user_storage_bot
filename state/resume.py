from aiogram.fsm.state import StatesGroup, State


class Resume(StatesGroup):
    owner_id = State()
    title = State()
    workload = State()
    skills = State()

class EditResume(StatesGroup):
    choice_what_to_edit = State()
    edit_title = State()
    edit_skills_add = State()
