from enum import Enum
from typing import List


class SubmissionStatus(Enum):
    SUCCESS = 1
    FAILED = 2


class Submission:
    def __init__(self, problem_id: str, status: SubmissionStatus):
        self._problem_id = problem_id
        self._status = status

    @property
    def status(self) -> SubmissionStatus:
        return self._status

    @property
    def problem_id(self) -> str:
        return self._problem_id


class UserInfo:
    def __init__(self, recent_submissions: List[Submission]):
        self._recent_submissions = recent_submissions

    @property
    def recent_submissions(self) -> List[Submission]:
        return self._recent_submissions
