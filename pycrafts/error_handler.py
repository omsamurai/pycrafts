import logging
import traceback

logger = logging.getLogger("pycrafts")


async def handle_error(update, context):
    tb = "".join(traceback.format_exception(type(context.error), context.error, context.error.__traceback__))
    logger.error(f"Exception:\n{tb}")
    if update and update.effective_message:
        await update.effective_message.reply_text("⚠️ Something went wrong. Please try again.")