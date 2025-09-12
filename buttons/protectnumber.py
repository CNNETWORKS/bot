from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import ADMINS
from modules.protected import add_protected, remove_protected, list_protected, is_protected

# Show info when "🔏 Protect U Number" button is clicked
async def protectnumber_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    text = (
        "🔏 **Protect Your Number** 🔏\n\n"
        "\n\n"
        "📞 Contact Admin to request number protection."
    )

    buttons = [
        [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/PIYUSH_SUPPORT_BOT")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ]

    await q.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown"
    )

# Admin command to protect a number
async def protect_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return await update.message.reply_text("🚫 You are not authorized to use this command.")

    if not context.args:
        return await update.message.reply_text("❌ Usage: /protect <number>")

    number = context.args[0].strip()
    if add_protected(number):
        await update.message.reply_text(f"✅ Number {number} protected successfully.")
    else:
        await update.message.reply_text(f"⚠️ Number {number} is already protected.")

# Admin command to unprotect
async def unprotect_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return await update.message.reply_text("🚫 You are not authorized to use this command.")

    if not context.args:
        return await update.message.reply_text("❌ Usage: /unprotect <number>")

    number = context.args[0].strip()
    if remove_protected(number):
        await update.message.reply_text(f"✅ Number {number} removed from protection.")
    else:
        await update.message.reply_text(f"⚠️ Number {number} was not protected.")

# Admin command to list protected numbers
async def list_protected_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return await update.message.reply_text("🚫 You are not authorized to use this command.")

    numbers = list_protected()
    if not numbers:
        return await update.message.reply_text("ℹ️ No protected numbers yet.")

    text = "🔏 **Protected Numbers List** 🔏\n\n"
    text += "\n".join([f"📱 {num}" for num in numbers])
    await update.message.reply_text(text, parse_mode="Markdown")
