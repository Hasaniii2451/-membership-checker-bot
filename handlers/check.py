from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database import get_channels
from config import ADMIN_ID

router = Router()


@router.message(Command("check"))
async def check_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    args = message.text.split()

    if len(args) != 2:
        await message.answer(
            "فرمت صحیح:\n/check USER_ID"
        )
        return

    user_id = int(args[1])

    channels = await get_channels()

    if not channels:
        await message.answer(
            "هیچ کانالی برای بررسی ثبت نشده است."
        )
        return

    result = f"🔍 بررسی کاربر: {user_id}\n\n"

    from aiogram import Bot
    bot: Bot = message.bot

    for channel_id, channel_name in channels:
        try:
            member = await bot.get_chat_member(
                chat_id=channel_id,
                user_id=user_id
            )

            if member.status in [
                "member",
                "administrator",
                "creator"
            ]:
                result += f"✅ {channel_name}\n"
            else:
                result += f"❌ {channel_name}\n"

        except Exception:
            result += f"⚠️ {channel_name} (خطا)\n"

    await message.answer(result)
