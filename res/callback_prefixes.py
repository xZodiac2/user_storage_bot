from enum import Enum

class SelectResumePrefixes(Enum):
    SELECT_RESUME = "select_resume"

class EditResumePrefixes(Enum):
    EDIT_TITLE = "edit_title"
    EDIT_WORKLOAD = "edit_workload"
    EDIT_SKILLS = "edit_skills"
    SAVE_RESUME_CHANGES = "save_resume_changes"

class EditWorkloadPrefixes(Enum):
    SET_WORKLOAD_PART_TIME = "set_workload_part_time"
    SET_WORKLOAD_FULL_TIME = "set_workload_full_time"
    BACK_TO_EDIT_RESUME = "back_to_edit_resume"

class EditSkillsPrefixes(Enum):
    CHOOSE_REMOVE = "choose_delete"
    CHOOSE_ADD = "choose_add"
    REMOVE_SKILL = "remove_skill"
    SAVE_CHANGES = "save_skill_changes"
    BACK_TO_EDIT_RESUME = "back_to_edit_resume"