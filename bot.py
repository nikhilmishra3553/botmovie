from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config

bot = Client(
    "MovieBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)


@bot.on_message(filters.command("start"))
async def start(client, message):

    try:
        member = await client.get_chat_member(config.CHANNEL_ID, message.from_user.id)

        if member.status in ["member","administrator","creator"]:
            await message.reply_text(
                "🎬 Welcome To Ultra Movie Bot\n\nMovie name bhejo."
            )
        else:
            await message.reply_text(
                f"⚠️ Pehle channel join karo\n{config.FORCE_JOIN}"
            )

    except:
        await message.reply_text(
            f"⚠️ Pehle channel join karo\n{config.FORCE_JOIN}"
        )


@bot.on_message(filters.private & filters.text)
async def search(client, message):

    query = message.text
    buttons = []
    count = 0

    async for msg in client.search_messages(config.CHANNEL_ID, query):

        if msg.video or msg.document:

            name = msg.video.file_name if msg.video else msg.document.file_name

            buttons.append(
                [InlineKeyboardButton(name, callback_data=str(msg.id))]
            )

            count += 1

        if count == 10:
            break

    if buttons:

        await message.reply_text(
            "🎬 Select Movie",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    else:
        await message.reply_text("❌ Movie nahi mili")


@bot.on_callback_query()
async def send_movie(client, callback_query):

    msg_id = int(callback_query.data)

    msg = await client.get_messages(config.CHANNEL_ID, msg_id)

    await msg.copy(callback_query.message.chat.id)

    await callback_query.answer()


print("🔥 Ultra Movie Bot Running")
bot.run()
