import os
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
bot_token = os.environ["BOT_TOKEN"]

app = Client("clean_forward_forceadd_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Source and destination for media forwarder
SOURCE_CHAT_ID = -1002312779748  # Change as needed
DEST_CHAT_ID = -1002740358553    # Your group

# Force Add Unlock Setup
REQUIRED_ADDS = 5
user_add_count = {}

@app.on_message(filters.chat(SOURCE_CHAT_ID))
def media_forwarder(client, message: Message):
    try:
        if message.media:
            message.copy(DEST_CHAT_ID, caption="")
    except Exception as e:
        print("Media forward error:", e)

@app.on_message(filters.new_chat_members)
def welcome_new_users(client, message: Message):
    for new_member in message.new_chat_members:
        if new_member.is_bot:
            continue
        user_id = new_member.id
        user_add_count[user_id] = 0  # reset or initialize

        mention = f"[{new_member.first_name}](tg://user?id={user_id})"
        welcome_text = (
            f"🕉️ Ahem... Brahmāsmi.

"
            f"{mention},
"
            f"Jab tumne is mehfil mein kadam rakha,
"
            f"toh tumne ek daayra paar kiya.
"
            f"Yeh group nahi, yeh tapasya hai.
"
            f"Aur tapasya mein niyam todne wale ko shaanti nahi milti...
"
            f"sirf moksha milta hai — group se bahar ka moksha 🔕

"
            f"⚠️ To unlock the group, you must add **{REQUIRED_ADDS} members**.
"
            f"Jab tak sankhya poori nahi hoti, moksha nahi milega 🧿"
        )
        try:
            client.send_message(chat_id=user_id, text=welcome_text)
        except PeerIdInvalid:
            print("Failed to send DM to", user_id)

app.run()
