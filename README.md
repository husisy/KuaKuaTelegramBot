# KuaKua Telegram bot

1. link
   * [telegram-bot/documentation](https://core.telegram.org/bots)
   * [python-telegram-bot/github](https://github.com/python-telegram-bot/python-telegram-bot)
   * [python-telegram-bot/wiki](https://github.com/python-telegram-bot/python-telegram-bot/wiki)
   * [python-telegram-bot/documentation](https://python-telegram-bot.org/)
2. install
   * `conda install -c conda-forge python-telegram-bot`
   * `pip install python-telegram-bot`
3. TODO
   * `/emoji`
   * `/help`: list all avalable commands
   * add `chatid` to `.env` to limit the bot to only one group (default to no response)
   * chatgpt: `/gpt4`, `/gpt3`, `/gpt_reset`
4. telegram bot
   * name: `kua_kua_doge_23333_bot`
   * PTB: `python-telegram-bot`

## how to contribute

1. `git clone xxx`
2. `cp .env.example .env` and fill the `.env` file
   * `TELEGRAM_BOT_API`: use `for_test_only_8413310117_bot` for test only
   * `TELEGRAM_CHAT_ID_AVAILABLE`: only id listed here can receive the response from the bot
   * `OPENAI_API_KEY`

```bash
micromamba create -n ptb
micromamba install -n ptb python-telegram-bot python-dotenv openai
```

## 部署`kua_kua_doge_23333_bot`

1. 先在自己电脑上开发（见上一段）
2. 然后推送到github
3. 然后手动登录到xxx服务器上（找zc要登录信息）

```bash
# turn off the bot
ps ax | grep main_ptb.py #get PID
kill <PID> #replace <PID>

# turn on the bot
micromamba activate ptb
nohup python main_ptb.py >> log/main_ptb.log 2>&1 &
```
