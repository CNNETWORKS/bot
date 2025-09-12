import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import SUPPORT_CONTACT
from modules.user import get_user, save_user, is_banned

BIN_REQUIRED_CREDITS = 1  # credits per BIN lookup


async def bin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Runs when /bin OR 'BIN Details' button is clicked"""
    uid = str(update.effective_user.id)

    if is_banned(uid):
        if update.message:
            return await update.message.reply_text("🚫 You are banned from using this bot.")
        elif update.callback_query:
            q = update.callback_query
            await q.answer()
            return await q.message.reply_text("🚫 You are banned from using this bot.")

    # Agar /bin <digits> diya gaya
    if update.message and context.args:
        return await process_bin(update, context, context.args[0].strip())

    # Agar argument nahi diya to guide karo
    text = (
        "💳 <b>BIN INFO SERVICE</b> 💳\n\n"
        "👉 Please send the first <code>6 digits</code> of your card (BIN) to get details.\n\n"
        f"📝 Format: <code>/bin 535522</code>\n"
        f"💰 Cost: {BIN_REQUIRED_CREDITS} Credit"
    )

    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="main_menu")]]

    if update.message:
        await update.message.reply_text(
            text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML"
        )
    elif update.callback_query:
        q = update.callback_query
        await q.answer()
        await q.message.reply_text(
            text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML"
        )


async def process_bin(update: Update, context: ContextTypes.DEFAULT_TYPE, bin_number: str):
    uid = str(update.effective_user.id)
    user = get_user(uid)

    if is_banned(uid):
        if update.message:
            return await update.message.reply_text("🚫 You are banned from using this bot.")
        elif update.callback_query:
            q = update.callback_query
            await q.answer()
            return await q.message.reply_text("🚫 You are banned from using this bot.")

    # Check credits
    current_credits = user.get("credits", 0)
    if current_credits < BIN_REQUIRED_CREDITS:
        keyboard = [
            [InlineKeyboardButton("📞 Contact Admin", url=SUPPORT_CONTACT)],
            [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
        ]
        if update.message:
            return await update.message.reply_text(
                f"❌ Insufficient Credits!\n\n"
                f"You need {BIN_REQUIRED_CREDITS} credit for BIN lookup.\n"
                f"Your balance: {current_credits}",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        elif update.callback_query:
            q = update.callback_query
            await q.answer()
            return await q.message.reply_text(
                f"❌ Insufficient Credits!\n\n"
                f"You need {BIN_REQUIRED_CREDITS} credit for BIN lookup.\n"
                f"Your balance: {current_credits}",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )

    # Searching message
    if update.message:
        searching_msg = await update.message.reply_text("⏳ Fetching BIN details...")
    else:
        q = update.callback_query
        await q.answer()
        searching_msg = await q.message.reply_text("⏳ Fetching BIN details...")

    try:
        resp = requests.get(f"https://lookup.binlist.net/{bin_number}", timeout=20)
        resp.raise_for_status()
        data = resp.json()

        # Deduct credits
        user["credits"] = max(0, current_credits - BIN_REQUIRED_CREDITS)
        save_user(uid)

        # Build result text
        result_text = (
            "💳 <b>BIN Lookup Results</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🔢 <b>BIN:</b> <code>{bin_number}</code>\n"
            f"🏦 <b>Bank:</b> {data.get('bank', {}).get('name', '-')}\n"
            f"💳 <b>Scheme:</b> {data.get('scheme', '-')}\n"
            f"💳 <b>Type:</b> {data.get('type', '-')}\n"
            f"💳 <b>Brand:</b> {data.get('brand', '-')}\n"
            f"🌍 <b>Country:</b> {data.get('country', {}).get('name', '-')} {data.get('country', {}).get('emoji', '')}\n"
            f"💱 <b>Currency:</b> {data.get('country', {}).get('currency', '-')}\n\n"
            f"✅ Credits Used: {BIN_REQUIRED_CREDITS}\n"
            f"💰 Remaining Credits: {user['credits']}"
        )

        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="main_menu")]]
        await searching_msg.edit_text(
            result_text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard)
        )

    except requests.RequestException:
        await searching_msg.edit_text("⚠️ Network error while fetching BIN info.")
    except ValueError:
        await searching_msg.edit_text("⚠️ Unexpected response format from BIN API.")
    except Exception as e:
        await searching_msg.edit_text(f"⚠️ Error: ")
