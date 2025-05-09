from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from src.utils.tools import safe_edit
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
    await message.answer(text=texts.get("start"), reply_markup=get_main_menu())


# return to menu handler
@menu_router.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await safe_edit(text=texts.get("menu_back"), reply_markup=get_main_menu())
    await callback.answer()
