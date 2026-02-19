from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def inline_buttons(buttons):
    keyboard = [
        [
            InlineKeyboardButton(text, url=value)
            if value.startswith("http")
            else InlineKeyboardButton(text, callback_data=value)
        ]
        for text, value in buttons
    ]
    return InlineKeyboardMarkup(keyboard)