import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

from .replies import safe_reply, html
from .media import send_photo, send_file
class Bot:
    def __init__(self, token: str):
        self.app = ApplicationBuilder().token(token).build()

    @classmethod
    def from_env(cls, key="BOT_TOKEN"):
        load_dotenv()
        token = os.getenv(key)
        if not token:
            raise RuntimeError(f"{key} not found in environment")
        return cls(token)

    def command(self, name, handler):
        self.app.add_handler(CommandHandler(name, handler))

    async def safe_reply(safe, update, text, **kwargs):
        await safe_reply(update, text, **kwargs)

    def html(self, text):
        return html(text)

    async def send_photo(self, update, photo, caption=None, **kwargs):
        await send_photo(update, photo, caption, **kwargs)

    async def send_file(safe, update, file, **kwargs):
        await send_file(update, file, **kwargs)

    def run(self):
        print("🚀 Pycrafts bot Running....")
        self.app.run_polling()
