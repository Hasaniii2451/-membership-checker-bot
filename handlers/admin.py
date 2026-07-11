from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config import ADMIN_ID
from database import (
    add_channel,
    remove_channel,
    get_channels
)

router = Router()


def is_admin(message: Message):
    return message.from_user.id == ADMIN_ID


@router.message(Command("addchannel"))
async def add_channel_handler(message: Message):
    if not is_admin(message):
        return

    args = message.text.split(maxsplit=2)

    if len(args) < 3:
        await message.answer(
            "فرمت صحیح:\n"
            "/addchannel ChannelID Name"
        )
        return

    channel_id = args[1]
    channel_name = args[2]

    await add_channel(channel_id, channel_name)

    await message.answer(
        f"✅ کانال اضافه شد:\n{channel_name}"
    )


@router.message(Command("removechannel"))
async def remove_channel_handler(message: Message):
    if not is_admin(message):
        return

    args = message.text.split()

    if len(args) != 2:
        await message.answer(
            "فرمت صحیح:\n"
            "/removechannel ChannelID"
        )
        return

    await remove_channel(args[1])

    await message.answer(
        "✅ کانال حذف شد."
    )


@router.message(Command("channels"))
async def list_channels_handler(message: Message):
    if not is_admin(message):
        return

    channels = await get_channels()

    if not channels:
        await message.answer(
            "هیچ کانالی ثبت نشده."
        )
        return

    text = "📋 لیست کانال‌ها:\n\n"

    for channel_id, name in channels:
        text += f"🔹 {name}\n"

    await message.answer(text)
