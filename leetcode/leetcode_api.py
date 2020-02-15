import re

import aiohttp
from aiohttp import ClientSession

from leetcode.models import UserInfo, Submission, SubmissionStatus


class LeetCodeApi:
    def __init__(self):
        self._base_url = 'https://leetcode.com/'

    async def _get(self, url) -> str:
        full_url = self._base_url + url
        async with ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(full_url) as response:
                return await response.text()

    async def get_user_info(self, user_name) -> UserInfo:
        html = await self._get(user_name + '/')
        submissions_block_search = re.search(pattern='<h3 class="panel-title">Most recent submissions</h3>(.*)</ul>',
                                             string=html,
                                             flags=(re.MULTILINE | re.DOTALL))
        submissions_block = submissions_block_search.group(1)

        submissions_search = re.findall(pattern='<a href="/problems/.*?</a>',
                                        string=submissions_block,
                                        flags=(re.MULTILINE | re.DOTALL))

        submissions = []

        for submission_html in submissions_search:
            problem_id_search = re.search('<a href="/problems/(.*?)/"', string=submission_html)
            problem_id = problem_id_search.group(1)
            accepted_search = re.search(
                '<span class=".*?" .*?>.*?Accepted.*?</span>',
                string=submission_html,
                flags=(re.MULTILINE | re.DOTALL)
            )

            status = SubmissionStatus.SUCCESS if accepted_search is not None else SubmissionStatus.FAILED

            new_submission = Submission(
                problem_id=problem_id,
                status=status
            )

            submissions.append(new_submission)

        return UserInfo(user_name=user_name, recent_submissions=submissions)
