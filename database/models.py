from dataclasses import dataclass

from database import Workload

@dataclass
class ResumeUpdateModel:
    title: str
    skills: list[str]
    workload: Workload