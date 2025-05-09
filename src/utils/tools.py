from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InputMediaPhoto
from aiogram.exceptions import TelegramBadRequest


async def safe_edit(
    callback: CallbackQuery,
    text: str,
    reply_markup: InlineKeyboardMarkup,
    fallback_photo: str = "https://upload.wikimedia.org/wikipedia/commons/c/ce/Transparent.gif"
):
    """
    Универсальная замена для edit_text. Если сообщение — media, заменяет caption через edit_media.
    """
    try:
        await callback.message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
    except TelegramBadRequest as e:
        if "no text in the message to edit" in str(e):
            await callback.message.edit_media(
                media=InputMediaPhoto(media=fallback_photo, caption=text, parse_mode="HTML"),
                reply_markup=reply_markup
            )
        else:
            raise e  # пробрасываем, если ошибка не связана с edit_text
