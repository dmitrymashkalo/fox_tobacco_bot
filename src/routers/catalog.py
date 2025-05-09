import aiohttp
from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from src.utils.tools import safe_edit
from src.utils.text_loader import texts
from src.config import API_GET_BRANDS

catalog_router = Router()
API_URL = API_GET_BRANDS

# step one: select brand with flavors [not empty]
@catalog_router.callback_query(lambda c: c.data == "catalog")
async def catalog_brands(callback: CallbackQuery):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_GET_BRANDS) as response:
                response.raise_for_status()
                data = await response.json()
                brands = data.get("brands", [])
    except Exception as e:
        await callback.message.answer(f"Error Message: {e}")
        await callback.answer()
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=brand["name"], callback_data=f"brand_{brand['brand_id']}")]
            for brand in brands
        ] + [[InlineKeyboardButton(text=texts.get("back_button"), callback_data="back_to_menu")]]
    )

    await safe_edit(
        callback=callback,
        text=texts.get("brands.select_brand"),
        reply_markup=keyboard
    )

    await callback.answer()