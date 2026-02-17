async def send_photo(update, photo, caption=None, **kwargs):
    if update.message:
        await update.message.reply_photo(
            photo = photo,
            caption = caption,
            **kwargs
            )
    elif update.effective_chat:
        await update.effective_chat.send_photo(
            photo = photo,
            caption = caption,
            **kwargs
        )

async def send_file(update, file, **kwargs):
    if update.message:
        await update.message.reply_document(
            document = file,
            **kwargs
        )
    elif update.effective_chat:
        await update.effective_chat.send_file(
            document = file,
            **kwargs
        )