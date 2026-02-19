import asyncio

class Ctx:
    def __init__(self, update, context):
        self.update = update
        self.context = context
        self.message = update.message
        self.chat = update.effective_chat
        self.user = update.effective_user
        self.data = {}

    async def reply(self, text, **kwargs):
        if self.message:
            await self.message.reply_text(text, **kwargs)
        else:
            await self.chat.send_message(text, **kwargs)

    async def reply_html(self, text, **kwargs):
        await self.reply(text, parse_mode="HTML", **kwargs)

    async def reply_buttons(self, text, buttons, **kwargs):
        from .buttons import inline_buttons
        markup = inline_buttons(buttons)
        await self.reply(text, reply_markup=markup, **kwargs)

    async def edit(self, text, **kwargs):
        if self.update.callback_query:
            await self.update.callback_query.edit_message_text(text, **kwargs)
        elif self.message:
            await self.message.edit_text(text, **kwargs)

    async def photo(self, photo, caption=None, **kwargs):
        if self.message:
            await self.message.reply_photo(photo, caption=caption, **kwargs)
        else:
            await self.chat.send_photo(photo, caption=caption, **kwargs)

    async def file(self, file, **kwargs):
        if self.message:
            await self.message.reply_document(file, **kwargs)
        else:
            await self.chat.send_document(file, **kwargs)

    async def typing(self):
        await self.chat.send_action("typing")

    async def ask(self, question: str = None):
        if question:
            await self.reply(question)
        key = f"ask_{self.user.id}_{self.chat.id}"
        futures = self.context.application.bot_data.setdefault("__futures__", {})
        loop = asyncio.get_event_loop()
        f = loop.create_future()
        futures[key] = f
        try:
            return await asyncio.wait_for(asyncio.shield(f), timeout=60)
        except asyncio.TimeoutError:
            futures.pop(key, None)
            return None