from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Vehicle Info Dummy Callback
async def vehicle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    text = (
        "🚗 𝗩𝗲𝗵𝗶𝗰𝗹𝗲 𝗜𝗻𝗳𝗼\n\n"
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


# Agar user vehicle number bhejta hai
async def vehicle_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip().upper()

    # Simple vehicle number check (alphanumeric, 6-10 chars)
    if user_input.isalnum() and 6 <= len(user_input) <= 10:
        await update.message.reply_text(
            f"🚗 Vehicle Number: {user_input}\n\n"
            "⚠️ Service is under maintenance. Please try later."
        )
    else:
        await update.message.reply_text(
            "❌ Invalid Vehicle Number!\n"
            "👉 Please enter a valid number (e.g., KA01AB1234)."
        )
