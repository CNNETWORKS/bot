from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Aadhaar Info Dummy Callback
async def adhar_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    text = (
        "🆔 𝗔𝗮𝗱𝗵𝗮𝗮𝗿 𝗜𝗻𝗳𝗼\n\n"
        "⚠️ This service is currently under maintenance.\n"
        "📌 Please try again later!"
    )

    buttons = [
        [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
    ]

    await q.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# Agar user Aadhaar number bhejta hai
async def adhar_number_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    # Simple Aadhaar check (12 digit number)
    if user_input.isdigit() and len(user_input) == 12:
        await update.message.reply_text(
            f"🆔 Aadhaar Number: {user_input}\n\n"
            "⚠️ Service is under maintenance. Please try later."
        )
    else:
        await update.message.reply_text(
            "❌ Invalid Aadhaar Number!\n"
            "👉 Please enter a valid 12-digit Aadhaar Number."
        )
