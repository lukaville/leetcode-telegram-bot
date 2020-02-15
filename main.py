import asyncio

from leetcode.leetcode_api import LeetCodeApi


async def main():
    api = LeetCodeApi()
    user_info = await api.get_user_info('')
    print(user_info)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
