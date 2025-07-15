import os
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

SOURCE_CHAT_ID = -1002312779748
DESTINATION_CHAT_ID = -1002740358553
GROUP_ID = -1002740358553
REQUIRED_ADDS = 5

user_data = {}

app = Client("force_forward_combined_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.chat(SOURCE_CHAT_ID))
def forward_media_only(client, message: Message):
    try:
        if message.media:
            message.copy(DESTINATION_CHAT_ID, caption="")
    except Exception as e:
        print("Error forwarding message:", e)

@app.on_message(filters.new_chat_members & filters.chat(GROUP_ID))
def welcome(client, message: Message):
    for new_member in message.new_chat_members:
        if not new_member.is_bot:
            user_data[new_member.id] = {"added": set()}
            client.restrict_chat_member(GROUP_ID, new_member.id, ChatPermissions())
            client.send_message(
                GROUP_ID,
                f"🕉️ Ahem... Brahmāsmi.\n"
                f"Welcome, [{new_member.first_name}](tg://user?id={new_member.id})!\n"
                f"🔒 Tapasya tabhi safal hogi jab aap {REQUIRED_ADDS} yogi laayenge.\n"
                f"Add friends & unlock chat.",
                parse_mode="markdown"
            )

@app.on_message(filters.chat(GROUP_ID) & filters.new_chat_members)
def track_invites(client, message: Message):
    inviter = message.from_user
    if inviter and not inviter.is_bot:
        if inviter.id not in user_data:
            user_data[inviter.id] = {"added": set()}
        for new_user in message.new_chat_members:
            user_data[inviter.id]["added"].add(new_user.id)

        added_count = len(user_data[inviter.id]["added"])
        if added_count >= REQUIRED_ADDS:
            client.restrict_chat_member(
                GROUP_ID,
                inviter.id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                )
            )
            client.send_message(
                GROUP_ID,
                f"🔓 Moksha prapt!\n"
                f"[{inviter.first_name}](tg://user?id={inviter.id}) ne {added_count} yogi laaye.\n"
                f"Chat ab khula hai!",
                parse_mode="markdown"
            )
        else:
            remain = REQUIRED_ADDS - added_count
            client.send_message(
                GROUP_ID,
                f"⏳ Abhi tak {added_count} yogi aaye hain.\n"
                f"{remain} aur laao moksha ke liye!",
                reply_to_message_id=message.message_id
            )

app.run()
