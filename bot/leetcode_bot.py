import asyncio
import json
import logging
import os
import traceback
from itertools import chain
from typing import List, Dict, Set

from leetcode.leetcode_api import LeetCodeApi
from leetcode.models import UserInfo, Submission, SubmissionStatus

_DEFAULT_UPDATE_PERIOD_SECONDS = 10
_DEFAULT_BETWEEN_REQUESTS_SECONDS = 1


class LeetCodeBot:
    def __init__(self, config_path):
        self._config_path = config_path
        self._api = LeetCodeApi()
        self._update_period = _DEFAULT_UPDATE_PERIOD_SECONDS
        self._config: Dict[str, List[str]] = {}
        self._user_infos: Dict[str, UserInfo] = {}
        self._notify_handler = None

    async def start(self, notify_handler):
        if os.path.isfile(self._config_path):
            with open(self._config_path, mode='r') as file:
                self._config = json.load(file)

        self._notify_handler = notify_handler
        asyncio.create_task(self._loop())

    async def _loop(self):
        while True:
            user_names = set(chain(*self._config.values()))

            for user_name in user_names:
                chat_ids = set([chat for chat, users in self._config.items() if user_name in users])

                try:
                    await self._check_for_updates(user_name, chat_ids)
                except Exception:
                    traceback.print_exc()

                await asyncio.sleep(_DEFAULT_BETWEEN_REQUESTS_SECONDS)
            await asyncio.sleep(self._update_period)

    async def _check_for_updates(self, user_name: str, chat_ids: Set[str]):
        user_info = await self._api.get_user_info(user_name)

        is_not_first_update = user_name in self._user_infos

        if is_not_first_update:
            for chat in chat_ids:
                await self._send_updates(
                    chat,
                    self._user_infos[user_name].recent_submissions,
                    user_info.recent_submissions,
                    user_info
                )

        self._user_infos[user_name] = user_info

    async def _send_updates(self,
                            chat: str,
                            previous: List[Submission],
                            current: List[Submission],
                            user_info: UserInfo):
        previous_accepted = set(
            [submission.problem_id for submission in previous if submission.status == SubmissionStatus.SUCCESS]
        )

        for submission in current:
            if submission.status == SubmissionStatus.SUCCESS and submission.problem_id not in previous_accepted:
                await self._new_accepted_submission(chat, user_info, submission)

    async def _new_accepted_submission(self, chat: str, user: UserInfo, submission: Submission):
        logging.info(f"New accepted submission {submission.problem_id} from {user.user_name}")

        await self._send_message(
            chat=chat,
            message=f"{user.user_name} solved problem https://leetcode.com/problems/{submission.problem_id}/"
        )

    async def _send_message(self, chat: str, message: str):
        await self._notify_handler(chat, message)

    async def configure(self, user_names, chat_id):
        self._config[chat_id] = user_names

        try:
            with open(self._config_path, mode='w') as file:
                file.write(json.dumps(self._config))
        except:
            logging.error("Error writing configuration")
