from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from src.utils.tools import safe_edit
from src.utils.text_loader import texts

history_router = Router()

@history_router.callback_query(lambda c: c.data == "history")
async def cart_handler(callback: CallbackQuery):
    title = texts.get("history.empty_title")
    body = texts.get("history.empty_body")

    await safe_edit(
        callback = callback,
        text = f"{title}{body}",
        reply_markup = InlineKeyboardMarkup(
            inline_keyboard = [
                [InlineKeyboardButton(
                    text = texts.get("back_button"),
                    callback_data = "back_to_menu"
                )]
            ]
        ),
    )

    await callback.answer()
