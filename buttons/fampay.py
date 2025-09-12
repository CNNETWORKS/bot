from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# FAMPAY Info Dummy Callback
async def fampay_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    text = (
        "💳 𝗙𝗔𝗠𝗣𝗔𝗬 𝗜𝗻𝗳𝗼 𝗦𝗲𝗿𝘃𝗶𝗰𝗲\n\n"
        "𝗣𝗹𝗲𝗮𝘀𝗲 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝘁𝗵𝗲 𝗙𝗔𝗠𝗣𝗔𝗬 𝗱𝗲𝘁𝗮𝗶𝗹𝘀. /fampay\n\n"
        "💰 𝗖𝗼𝘀𝘁: 𝟤 𝗖𝗿𝗲𝗱𝗶𝘁𝘀\n\n"
        "⚠️ 𝗧𝗵𝗶𝘀 𝘀𝗲𝗿𝘃𝗶𝗰𝗲 𝗶𝘀 𝗰𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝘂𝗻𝗱𝗲𝗿 𝗺𝗮𝗶𝗻𝘁𝗲𝗻𝗮𝗻𝗰𝗲.\n"
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


# Agar user FAMPAY ID ya number bhejta hai
async def fampay_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    # Basic validation (at least 5 characters)
    if len(user_input) >= 5:
        await update.message.reply_text(
            f"💳 𝗙𝗔𝗠𝗣𝗔𝗬 𝗗𝗲𝘁𝗮𝗶𝗹: `{user_input}`\n\n"
            "⚠️ 𝗧𝗵𝗶𝘀 𝘀𝗲𝗿𝘃𝗶𝗰𝗲 𝗶𝘀 𝗰𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝘂𝗻𝗱𝗲𝗿 𝗺𝗮𝗶𝗻𝘁𝗲𝗻𝗮𝗻𝗰𝗲.\n"
            "📌 𝗣𝗹𝗲𝗮𝘀𝗲 𝘁𝗿𝘆 𝗮𝗴𝗮𝗶𝗻 𝗹𝗮𝘁𝗲𝗿.",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗙𝗔𝗠𝗣𝗔𝗬 𝗱𝗲𝘁𝗮𝗶𝗹!\n"
            "👉 𝗣𝗹𝗲𝗮𝘀𝗲 𝗲𝗻𝘁𝗲𝗿 𝗮 𝘃𝗮𝗹𝗶𝗱 𝗙𝗔𝗠𝗣𝗔𝗬 𝗜𝗗/𝗻𝘂𝗺𝗯𝗲𝗿.",
            parse_mode="Markdown"
        )
