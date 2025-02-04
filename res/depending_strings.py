from database import UserOrm


def str_user_info(user):
    resumes = [f"{resume.id}. {resume.title}" for resume in user.resumes]
    return f"""
Id: {user.id}
Имя: {user.name}
Резюме: {", ".join(resumes) if resumes else "Нет резюме"}"""


def str_select_resume_message(user: UserOrm):
    return f"""
Id: {user.id}
Имя: {user.name}
Выберите резюме для реактирования"""


def str_edit_resume_message(title, workload, skills):
    return f"""
Выберите пункт, который хотели бы изменить

Название: {title}
Рабочая нагрузка: {workload}
Скиллы: {skills}"""
