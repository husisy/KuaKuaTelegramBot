import os
import logging
import dotenv
import openai
import collections

import telegram
import telegram.ext

dotenv.load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]
_TELEGRAM_BOT_API = os.environ['TELEGRAM_BOT_API']
_TELEGRAM_CHAT_ID_AVAILABLE = {int(x) for x in os.environ.get('TELEGRAM_CHAT_ID_AVAILABLE', '').split(',') if x}

print(_TELEGRAM_CHAT_ID_AVAILABLE)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class NaiveChatGPT:
    def __init__(self) -> None:
        self.message_list = [{"role": "system", "content": "You are a helpful assistant."},]
        self.response = None #for debug only

    def chat(self, message='', reset=False):
        if reset:
            self.message_list = self.message_list[:1]
        message = str(message)
        if message: #skip if empty
            self.message_list.append({"role": "user", "content": str(message)})
            self.response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.message_list)
            tmp0 = self.response.choices[0].message.content
            self.message_list.append({"role": "assistant", "content": tmp0})
            return tmp0

_chat_id_to_gpt_dict = collections.defaultdict(NaiveChatGPT)

def is_available_decorator(func):
    async def hf0(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
        print('[mydebug][chat-id]', update.effective_chat.id, type(update.effective_chat.id))
        print('[mydebug][user]', update.effective_user)
        print('[mydebug][text]', update.message.text)
        if update.effective_chat.id in _TELEGRAM_CHAT_ID_AVAILABLE:
            await func(update, context)
        # otherwise, just no response
    return hf0

@is_available_decorator
async def hello(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'泥嚎 {update.effective_user.first_name}')

@is_available_decorator
async def help(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE) -> None:
    tmp0 = '''
/hello - 打招呼
/help - 显示帮助
/gpt_reset - 重置 GPT 对话
'''
    await update.message.reply_text(tmp0)

@is_available_decorator
async def unknown(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

@is_available_decorator
async def gpt_chat(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    model = _chat_id_to_gpt_dict[update.effective_chat.id]
    tmp0 = model.chat(update.message.text, reset=False)
    await update.message.reply_text(tmp0)

@is_available_decorator
async def gpt_reset(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    model = _chat_id_to_gpt_dict[update.effective_chat.id]
    model.chat('', reset=True)


if __name__ == '__main__':
    app = telegram.ext.ApplicationBuilder().token(_TELEGRAM_BOT_API).build()

    app.add_handler(telegram.ext.CommandHandler("hello", hello))

    app.add_handler(telegram.ext.CommandHandler("help", help))

    app.add_handler(telegram.ext.MessageHandler(telegram.ext.filters.TEXT & (~telegram.ext.filters.COMMAND), gpt_chat))

    app.add_handler(telegram.ext.CommandHandler("gpt_reset", gpt_reset))

    # Other handlers, MUST be last
    app.add_handler(telegram.ext.MessageHandler(telegram.ext.filters.COMMAND, unknown))

    app.run_polling()
