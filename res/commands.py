from enum import Enum

class Commands(Enum):
    INSERT_USER = "insert_user"
    INSERT_RESUME = "insert_resume"
    GET_ALL_USERS = "get_all_users"
    EDIT_RESUME = "edit_resume"