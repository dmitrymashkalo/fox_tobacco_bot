from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from src.utils.text_loader import texts
from src.config import IMG_URLS

history_router = Router()

@history_router.callback_query(lambda c: c.data == "history")
async def cart_handler(callback: CallbackQuery):
    await callback.message.delete()

    title = texts.get("history.empty_title")
    body = texts.get("history.empty_body")
    photo = FSInputFile(f'{IMG_URLS}menu_history.png')

    await callback.message.answer_photo(
        photo=photo,
        caption=f"{title}{body}",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=texts.get("back_button"),
                    callback_data="back_to_menu"
                )]
            ]
        ),
    )

    await callback.answer()
