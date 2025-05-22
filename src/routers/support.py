from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from src.utils.tools import safe_edit
from src.utils.text_loader import texts
from src.config import ADMIN_USER

support_router = Router()

@support_router.callback_query(lambda c: c.data == "support")
async def support_handler(callback: CallbackQuery):
    title = texts.get("support.title")
    body = texts.get("support.body")
    photo = FSInputFile('/Users/Dzmitry_Mashkala/fox_tobacco/fox_tobacco_bot/src/img/menu_support.png')

    await callback.message.answer_photo(
        photo=photo,
        caption=f"{title}{body}",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=texts.get("support.msg_button"),
                    url=ADMIN_USER
                )],
                [InlineKeyboardButton(
                    text=texts.get("back_button"),
                    callback_data="back_to_menu"
                )]
            ]
        )
    )
    """
    await safe_edit(
        callback,
        f"{title}{body}",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=texts.get("support.msg_button"),
                    url=ADMIN_USER
                )],
                [InlineKeyboardButton(
                    text=texts.get("back_button"),
                    callback_data="back_to_menu"
                )]
            ]
        )
    )"""

    await callback.answer()
