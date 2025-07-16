import os
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
import asyncio

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

# Filled IDs
SOURCE_CHAT_ID = -1002312779748
DEST_CHAT_ID = -1002740358553
GROUP_ID = -1002740358553
MIN_MEMBERS_REQUIRED = 5

app = Client("clean_forward_force_add_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ Forward Media-Only
@app.on_message(filters.chat(SOURCE_CHAT_ID))
async def forward_media_only(client: Client, message: Message):
    try:
        if message.media:
            await message.copy(DEST_CHAT_ID, caption="")
            print(f"Forwarded media: {message.message_id}")
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        print("Forward Error:", e)

# ✅ Force Add Unlock Logic
user_data = {}

@app.on_message(filters.new_chat_members)
async def new_member(client, message: Message):
    for user in message.new_chat_members:
        if user.is_bot:
            continue

        user_data[user.id] = set()
        await message.reply_text(
            f"🕉️ Ahem... Brahmāsmi.\n\n"
            f"{user.first_name}, is daayre mein pravesh ke liye tumhe 5 sadasya laane honge.\n"
            f"Jab tak tum yeh tapasya poori nahi karte, tum mukh bandh raho. 🔕\n\n"
            f"➤ Add 5 members to unlock full access."
        )
        await app.restrict_chat_member(
            chat_id=GROUP_ID,
            user_id=user.id,
            permissions={"can_send_messages": False}
        )

@app.on_message(filters.chat(GROUP_ID))
async def track_adds(client, message: Message):
    user = message.from_user
    if not user or user.id not in user_data:
        return

    if message.new_chat_members:
        for member in message.new_chat_members:
            if not member.is_bot and member.id != user.id:
                user_data[user.id].add(member.id)

        if len(user_data[user.id]) >= MIN_MEMBERS_REQUIRED:
            await app.restrict_chat_member(
                chat_id=GROUP_ID,
                user_id=user.id,
                permissions={
                    "can_send_messages": True,
                    "can_send_media_messages": True,
                    "can_send_other_messages": True,
                    "can_add_web_page_previews": True,
                }
            )
            await message.reply_text(
                f"🔓 Tapasya poori hui!\n"
                f"{user.first_name}, ab tum mukh khol sakte ho.\n"
                f"Swagat hai Guruji ke daayre mein."
            )

app.run()
