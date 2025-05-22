from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from src.utils.text_loader import texts

cart_router = Router()

@cart_router.callback_query(lambda c: c.data == "cart")
async def cart_handler(callback: CallbackQuery):
    title = texts.get("cart.empty_title")
    body = texts.get("cart.empty_body")
    photo = FSInputFile('/Users/Dzmitry_Mashkala/fox_tobacco/fox_tobacco_bot/src/img/menu_cart.png')

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
