import aiohttp
from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from src.utils.text_loader import texts
from src.config import API_GET_BRANDS, API_GET_FLAVORS_BY_BRAND, API_GET_FLAVOR_DETAILS, IMG_URLS

catalog_router = Router()

# step one: select brand with flavors [not empty]
@catalog_router.callback_query(lambda c: c.data == "catalog")
async def catalog_brands(callback: CallbackQuery):
    photo = FSInputFile(f'{IMG_URLS}menu_catalog.png')

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
                text=f"{flavor["name"]} {flavor["weight"]}г {flavor["price"]}zł",
                callback_data=f"flavor_{flavor['flavor_id']}|{brand_id}|{brand_name}")]
            for flavor in flavors
        ] + [[InlineKeyboardButton(text=texts.get("back_button"), callback_data="catalog")]]
    )

    photo = FSInputFile(f'{IMG_URLS}brand_{brand_name}.png')

    await callback.message.answer_photo(
        photo=photo,
        caption=texts.get("flavors.select_flavor"),
        parse_mode="HTML",
        reply_markup=keyboard
    )

    await callback.answer()


# step three: show flavor (product) details
@catalog_router.callback_query(lambda c: c.data.startswith("flavor_"))
async def flavor_details(callback: CallbackQuery):
    raw_data = callback.data.removeprefix("flavor_")
    flavor_id, brand_id, brand_name = raw_data.split("|", 2)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_GET_FLAVOR_DETAILS}{flavor_id}") as response:
                response.raise_for_status()
                data = await response.json()
                flavor = data.get("flavor")
                if not flavor:
                    raise ValueError("Flavor not found")
    except Exception as e:
        await callback.message.answer(f"Error Message: {e}")
        await callback.answer()
        return

    text = (
        f"▶️ <b>{flavor['name']} {flavor['weight']}г</b>\n"
        f"▶️ <b>💵 Цена: {flavor['price']} zł 💵</b>\n"
        f"▶️ <b>⏳ Доступно: {flavor['available_qty']} ⏳</b>\n\n"
        f"{flavor['description']}"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=texts.get("back_button"), callback_data=f"brand_{brand_id}|{brand_name}")],
            [InlineKeyboardButton(text=texts.get("to_menu_button"), callback_data="back_to_menu")]
        ]
    )

    photo_url = flavor.get("image_url")
    if photo_url:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(photo_url) as img_response:
                    img_response.raise_for_status()
                    img_bytes = await img_response.read()

            from aiogram.types import BufferedInputFile
            photo = BufferedInputFile(img_bytes, filename="flavor.jpg")

            await callback.message.answer_photo(
                photo=photo,
                caption=text,
                parse_mode="HTML",
                reply_markup=keyboard
            )
        except Exception as e:
            await callback.message.answer(f"{text}\n\n(Не удалось загрузить изображение)", parse_mode="HTML", reply_markup=keyboard)
    else:
        await callback.message.answer(text, parse_mode="HTML", reply_markup=keyboard)

    await callback.answer()