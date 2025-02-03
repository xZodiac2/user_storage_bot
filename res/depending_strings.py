from database import UserOrm


def select_resume_message(user: UserOrm):
    return f"""
Id: {user.id}
Name: {user.name}
Выберите резюме для реактирования"""


def edit_resume_message(title, workload, skills):
    return f"""
Выберите пункт, который хотели бы изменить

Название: {title}
Рабочая нагрузка: {workload}
Скиллы: {skills}"""
