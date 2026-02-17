from telegram import Update

async def safe_reply(update : Update, text : str, **kwargs):
    if update.message:
        await update.message.reply_text(
            text, 
            **kwargs
            )
    else:
        await update.effective_chat.send_message(
            text,
            **kwargs
            )

def html(text : str) -> dict:
    return{
        "text" : text,
        "parse_mode" : "HTML"
        }