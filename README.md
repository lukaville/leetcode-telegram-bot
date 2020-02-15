# LeetCode Telegram notification bot

Telegram bot that follows a set of LeetCode users and notifies about new accepted submissions from these users.

## Running

```bash
docker build -t leetcodebot .
```

```bash
docker run -d --name leetcodebot --env TELEGRAM_API_TOKEN=[token] leetcodebot
```
