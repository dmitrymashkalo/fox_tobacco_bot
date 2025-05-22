import aiohttp
from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from src.utils.tools import safe_edit
from src.utils.text_loader import texts
from src.config import API_GET_BRANDS, API_GET_FLAVORS_BY_BRAND

catalog_router = Router()

# step one: select brand with flavors [not empty]
@catalog_router.callback_query(lambda c: c.data == "catalog")
async def catalog_brands(callback: CallbackQuery):
    photo = FSInputFile('/Users/Dzmitry_Mashkala/fox_tobacco/fox_tobacco_bot/src/img/menu_catalog.png')

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
            [InlineKeyboardButton(
                text=brand["name"],
                callback_data=f"brand_{brand['brand_id']}|{brand['name']}")]
            for brand in brands
        ] + [[InlineKeyboardButton(text=texts.get("back_button"), callback_data="back_to_menu")]]
    )

    await callback.message.answer_photo(
        photo=photo,
        caption=texts.get("brands.select_brand"),
        parse_mode="HTML",
        reply_markup=keyboard
    )

    await callback.answer()


#step two: get all flavors for selected brand [not empty]
@catalog_router.callback_query(lambda c: c.data.startswith("brand_"))
async def brand_flavors(callback: CallbackQuery):
    raw_data = callback.data.removeprefix("brand_")
    brand_id, brand_name = raw_data.split("|", 1)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_GET_FLAVORS_BY_BRAND}{brand_id}") as response:
                response.raise_for_status()
                data = await response.json()
                flavors = data.get("flavors", [])
    except Exception as e:
        await callback.message.answer(f"Error Message: {e}")
        await callback.answer()
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=f"{flavor["name"]} — {flavor["weight"]}г — {flavor["price"]}zł",
                callback_data=f"flavor_{flavor['flavor_id']}")]
            for flavor in flavors
        ] + [[InlineKeyboardButton(text=texts.get("back_button"), callback_data="catalog")]]
    )

    await safe_edit(
        callback=callback,
        text=texts.get("flavors.select_flavor") + f"{brand_name}:",
        reply_markup=keyboard
    )

    await callback.answer()
