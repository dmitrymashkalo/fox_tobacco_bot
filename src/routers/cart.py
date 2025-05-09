from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from src.utils.tools import safe_edit
from src.utils.text_loader import texts

cart_router = Router()

@cart_router.callback_query(lambda c: c.data == "cart")
async def cart_handler(callback: CallbackQuery):
    title = texts.get("cart.empty_title")
    body = texts.get("cart.empty_body")

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
