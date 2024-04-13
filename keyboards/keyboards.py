from aiogram.utils.keyboard import (KeyboardBuilder, KeyboardButton,
                                    InlineKeyboardBuilder, InlineKeyboardButton,
                                    InlineKeyboardMarkup)

async def create_game_ikb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Join in",
                                callback_data="joined_in"))

    return kb.as_markup(resize_keyboard=True)
