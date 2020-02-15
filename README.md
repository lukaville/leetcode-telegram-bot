# LeetCode Telegram notification bot

Telegram bot that follows a set of LeetCode users and notifies about new accepted submissions from these users.

## Running

```bash
docker build -t leetcodebot .
```

```bash
docker run -d --name leetcodebot -v /data/leetcodebot:/data --env PROXY=http://[proxy] --env TELEGRAM_API_TOKEN=[token] leetcodebot
```
