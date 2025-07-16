import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, RPCError

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

SOURCE_CHAT_ID = -1002312779748
DESTINATION_CHAT_ID = -1002740358553
REQUIRED_ADDS = 5

user_adds = {}

app = Client("combined_forward_forceadd_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.chat(SOURCE_CHAT_ID))
async def forward_media_only(client, message):
    try:
        if message.media:
            await message.copy(DESTINATION_CHAT_ID, caption="")
            await asyncio.sleep(1.5)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await message.copy(DESTINATION_CHAT_ID, caption="")
    except RPCError as e:
        print(f"Error forwarding message {message.message_id}: {e}")

@app.on_message(filters.new_chat_members)
async def handle_new_user(client, message):
    new_user = message.new_chat_members[0].id
    user_adds[new_user] = 0
    await message.reply_text(
        f"🕉️ Ahem... Brahmāsmi.

Welcome, {message.new_chat_members[0].mention}!

"
        f"To unlock this sacred space, invite {REQUIRED_ADDS} members to this group.
"
        f"Once done, your path to enlightenment (and chatting) shall be opened. 🧘‍♂️"
    )

@app.on_message(filters.command("addcheck"))
async def check_adds(client, message):
    user_id = message.from_user.id
    added = user_adds.get(user_id, 0)
    remain = REQUIRED_ADDS - added
    await message.reply_text(
        f"🧮 You have added {added}/{REQUIRED_ADDS} members.
"
        f"{'✅ Access Granted!' if remain <= 0 else f'⏳ Add {remain} more to unlock group.'}"
    )

app.run()
