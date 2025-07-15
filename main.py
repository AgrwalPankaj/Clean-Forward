import os
from pyrogram import Client, filters

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
bot_token = os.environ["BOT_TOKEN"]

source_chat_id = -1002312779748  # your source group
destination_chat_id = -1002740358553  # your destination group

app = Client("media_forwarder_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.chat(source_chat_id))
def media_only_forwarder(client, message):
    try:
        if message.media:
            message.copy(destination_chat_id, caption="")  # Remove caption
            print(f"✅ Media forwarded: {message.message_id}")
    except Exception as e:
        print(f"❌ Error: {e}")

app.run()
