from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Breach Info Dummy Callback
async def breach_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    text = (
        "🔍 𝗕𝗥𝗘𝗔𝗖𝗛 𝗜𝗡𝗙𝗢𝗥𝗠𝗔𝗧𝗜𝗢𝗡 𝗦𝗘𝗥𝗩𝗜𝗖𝗘 🔍\n\n"
        "🚨 /breach 𝗦𝗲𝗻𝗱 𝗮𝗻𝘆 𝗼𝗳 𝘁𝗵𝗲 𝗳𝗼𝗹𝗹𝗼𝘄𝗶𝗻𝗴 𝘁𝗼 𝗰𝗵𝗲𝗰𝗸 𝗳𝗼𝗿 𝗱𝗮𝘁𝗮 𝗯𝗿𝗲𝗮𝗰𝗵𝗲𝘀:\n\n"
        "📧 𝗘𝗺𝗮𝗶𝗹: example@gmail.com\n"
        "🌐 𝗜𝗣 𝗔𝗱𝗱𝗿𝗲𝘀𝘀: 192.168.1.1\n"
        "👤 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: johndoe123\n"
        "📱 𝗣𝗵𝗼𝗻𝗲: 9876543210\n"
        "🌐 𝗗𝗼𝗺𝗮𝗶𝗻: example.com\n\n"
        "💰 𝗖𝗼𝘀𝘁: 𝟣 𝗰𝗿𝗲𝗱𝗶𝘁 𝗽𝗲𝗿 𝘀𝗲𝗮𝗿𝗰𝗵\n"
        "📄 𝗡𝗼𝘁𝗲: 𝗟𝗼𝗻𝗴 𝗿𝗲𝘀𝘂𝗹𝘁𝘀 𝘄𝗶𝗹𝗹 𝗵𝗮𝘃𝗲 𝗽𝗮𝗴𝗶𝗻𝗮𝘁𝗶𝗼𝗻\n\n"
        "⚠️ 𝗧𝗵𝗶𝘀 𝘀𝗲𝗿𝘃𝗶𝗰𝗲 𝗶𝘀 𝘂𝗻𝗱𝗲𝗿 𝗺𝗮𝗶𝗻𝘁𝗲𝗻𝗮𝗻𝗰𝗲.\n"
        "📌 𝗣𝗹𝗲𝗮𝘀𝗲 𝘁𝗿𝘆 𝗮𝗴𝗮𝗶𝗻 𝗹𝗮𝘁𝗲𝗿."
    )

    buttons = [
        [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
    ]

    await q.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# Agar user breach input bhejta hai
async def breach_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    if len(user_input) >= 3:  # Basic validation (email/username/domain/IP/phone min 3 chars)
        await update.message.reply_text(
            f"🔍 𝗖𝗵𝗲𝗰𝗸𝗶𝗻𝗴: `{user_input}`\n\n"
            "⚠️ 𝗧𝗵𝗶𝘀 𝘀𝗲𝗿𝘃𝗶𝗰𝗲 𝗶𝘀 𝗰𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝘂𝗻𝗱𝗲𝗿 𝗺𝗮𝗶𝗻𝘁𝗲𝗻𝗮𝗻𝗰𝗲.\n"
            "📌 𝗣𝗹𝗲𝗮𝘀𝗲 𝘁𝗿𝘆 𝗮𝗴𝗮𝗶𝗻 𝗹𝗮𝘁𝗲𝗿.",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗶𝗻𝗽𝘂𝘁!\n"
            "👉 𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗲𝗻𝗱 𝗮 𝘃𝗮𝗹𝗶𝗱 𝗲𝗺𝗮𝗶𝗹, 𝗶𝗽, 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲, 𝗽𝗵𝗼𝗻𝗲 𝗼𝗿 𝗱𝗼𝗺𝗮𝗶𝗻.",
            parse_mode="Markdown"
        )
