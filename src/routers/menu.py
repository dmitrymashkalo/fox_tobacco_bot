from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile, InputMediaPhoto
from src.utils.text_loader import texts

menu_router = Router()


# main menu
def get_main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=texts.get("menu_buttons.catalog"), callback_data="catalog")],
            [InlineKeyboardButton(text=texts.get("menu_buttons.cart"), callback_data="cart")],
            [InlineKeyboardButton(text=texts.get("menu_buttons.history"), callback_data="history")],
            [InlineKeyboardButton(text=texts.get("menu_buttons.support"), callback_data="support")]
        ]
    )


# start handler
@menu_router.message(lambda msg: msg.text == "/start")
async def start_handler(message: Message):
    photo = FSInputFile('/Users/Dzmitry_Mashkala/fox_tobacco/fox_tobacco_bot/src/img/logo_two.jpeg')
    await message.answer_photo(
        photo=photo,
        caption=texts.get("start"),
        parse_mode="HTML",
        reply_markup=get_main_menu()
    )


# return to menu handler
@menu_router.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    photo = FSInputFile('/Users/Dzmitry_Mashkala/fox_tobacco/fox_tobacco_bot/src/img/logo_two.jpeg')
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=texts.get("start"),
            parse_mode="HTML"
        ),
        reply_markup=get_main_menu()
    )
    await callback.answer()
