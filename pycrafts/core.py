import os
import logging
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from .ctx import Ctx
from .error_handler import handle_error
from .rate_limiter import is_rate_limited
from .loader import load_handlers

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)

class Bot:
    def __init__(self, token: str):
        self.app = ApplicationBuilder().token(token).build()
        self.app.add_error_handler(handle_error)
        self._middlewares = []

    @classmethod
    def from_env(cls, key="BOT_TOKEN"):
        load_dotenv()
        token = os.getenv(key)
        if not token:
            raise RuntimeError(f"{key} not found in .env")
        return cls(token)

    def middleware(self, func):
        self._middlewares.append(func)
        return func

    async def _run_middlewares(self, ctx, extra: list = None) -> bool:
        for mw in self._middlewares + (extra or []):
            result = await mw(ctx)
            if result is False:
                return False
        return True

    def _wrap(self, func, cooldown: int = 0, middleware: list = None, name: str = ""):
        async def wrapper(update, context):
            ctx = Ctx(update, context)

            futures = context.application.bot_data.get("__futures__", {})
            key = f"ask_{ctx.user.id}_{ctx.chat.id}"
            if key in futures and update.message:
                f = futures.pop(key)
                if not f.done():
                    f.set_result(update.message.text)
                return

            if cooldown and is_rate_limited(ctx.user.id, name, cooldown):
                await ctx.reply(f"⏳ Please wait {cooldown}s before using this again.")
                return

            if not await self._run_middlewares(ctx, middleware):
                return

            await func(ctx)
        return wrapper

    def command(self, name, cooldown: int = 0, middleware: list = None):
        def decorator(func):
            self.app.add_handler(
                CommandHandler(name, self._wrap(func, cooldown, middleware, name))
            )
            return func
        return decorator

    def on_message(self, filter=filters.TEXT & ~filters.COMMAND):
        def decorator(func):
            self.app.add_handler(MessageHandler(filter, self._wrap(func)))
            return func
        return decorator

    def on_callback(self, pattern=None):
        def decorator(func):
            self.app.add_handler(
                CallbackQueryHandler(self._wrap(func), pattern=pattern)
            )
            return func
        return decorator

    async def send(self, chat_id: int, text: str, **kwargs):
        await self.app.bot.send_message(chat_id=chat_id, text=text, **kwargs)

    def load(self, folder: str):
        print(f"📂 Loading handlers from '{folder}':")
        load_handlers(self, folder)

    def run(self):
        print("🚀 Pycrafts bot running...")
        self.app.run_polling()