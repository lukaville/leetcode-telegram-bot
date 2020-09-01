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

    def __repr__(self):
        return str(self.__dict__)


class UserInfo:
    def __init__(self, user_name: str, recent_submissions: List[Submission]):
        self._user_name = user_name
        self._recent_submissions = recent_submissions

    @property
    def recent_submissions(self) -> List[Submission]:
        return self._recent_submissions

    @property
    def user_name(self) -> str:
        return self._user_name
