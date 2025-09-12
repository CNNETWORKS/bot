from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# UPI Info Dummy Callback
async def upi_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    text = (
        "💰 𝗨𝗣𝗜 𝗜𝗡𝗙𝗢𝗥𝗠𝗔𝗧𝗜𝗢𝗡 𝗟𝗢𝗢𝗞𝗨𝗣\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🔍 𝗘𝗻𝘁𝗲𝗿 𝗨𝗣𝗜 𝗜𝗗 𝘁𝗼 𝘀𝗲𝗮𝗿𝗰𝗵:\n\n"
        "💡 𝗘𝘅𝗮𝗺𝗽𝗹𝗲: `/upiinfo user@upi`\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "💳 𝗖𝗼𝘀𝘁: 𝟣 𝗖𝗿𝗲𝗱𝗶𝘁\n\n"
        "👇 𝗦𝗲𝗻𝗱 𝘁𝗵𝗲 𝗨𝗣𝗜 𝗜𝗗 𝗻𝗼𝘄:"
    )

    buttons = [
        [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
    ]

    await q.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# Agar user UPI ID bhejta hai
async def upi_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip().lower()

    # Basic UPI check (contains @ and at least 3 chars before it)
    if "@" in user_input and len(user_input.split("@")[0]) >= 3:
        await update.message.reply_text(
            f"💰 𝗨𝗣𝗜 𝗜𝗗: `{user_input}`\n\n"
            "⚠️ 𝗧𝗵𝗶𝘀 𝘀𝗲𝗿𝘃𝗶𝗰𝗲 𝗶𝘀 𝗰𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝘂𝗻𝗱𝗲𝗿 𝗺𝗮𝗶𝗻𝘁𝗲𝗻𝗮𝗻𝗰𝗲.\n"
            "📌 𝗣𝗹𝗲𝗮𝘀𝗲 𝘁𝗿𝘆 𝗮𝗴𝗮𝗶𝗻 𝗹𝗮𝘁𝗲𝗿."
        , parse_mode="Markdown")
    else:
        await update.message.reply_text(
            "❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗨𝗣𝗜 𝗜𝗗!\n"
            "👉 𝗘𝘅𝗮𝗺𝗽𝗹𝗲: `rohit@upi`",
            parse_mode="Markdown"
        )
