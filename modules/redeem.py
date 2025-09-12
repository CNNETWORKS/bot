# modules/redeem.py
import random
import string
import datetime
from typing import Dict, Any

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from config import REDEEMS_FILE, ADMINS
from modules.utils import load_json, save_json
from modules.user import get_user, save_user

# Load or initialize redeems store
try:
    _redeems: Dict[str, Dict[str, Any]] = load_json(REDEEMS_FILE) or {}
except Exception:
    _redeems = {}

WAITING_CODE = 1  # conversation state


def _generate_code(length: int = 8) -> str:
    """Generate an uppercase alnum redeem code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


async def redeem_create(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command: /redeem <credits> [count]  -> create 1 or multiple redeem codes"""
    uid = update.effective_user.id
    if uid not in ADMINS:
        return await update.message.reply_text("🚫 You are not authorized.")

    if not context.args:
        return await update.message.reply_text("Usage: /redeem <credits> [count]")

    # parse credits and optional count
    try:
        credits = int(context.args[0])
    except ValueError:
        return await update.message.reply_text("Credits must be a number.")

    count = 1
    if len(context.args) > 1:
        try:
            count = int(context.args[1])
            count = max(1, min(count, 50))  # safety cap
        except ValueError:
            count = 1

    created_codes = []
    for _ in range(count):
        code = _generate_code()
        # ensure unique
        while code in _redeems:
            code = _generate_code()
        _redeems[code] = {
            "credits": credits,
            "used": False,
            "created_by": uid,
            "created_at": datetime.datetime.utcnow().isoformat()
        }
        created_codes.append(code)

    save_json(REDEEMS_FILE, _redeems)

    if count == 1:
        await update.message.reply_text(
            f"✅ Redeem code created:\n\nCode: `{created_codes[0]}`\nCredits: {credits}",
            parse_mode="Markdown"
        )
    else:
        # send multiple codes (keep message size reasonable)
        codes_text = "\n".join(created_codes)
        await update.message.reply_text(
            f"✅ {len(created_codes)} redeem codes created for {credits} credits each:\n\n{codes_text}"
        )


async def redeem_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin helper: list redeem codes (limited). Command: /redeemlist"""
    uid = update.effective_user.id
    if uid not in ADMINS:
        return await update.message.reply_text("🚫 𝙔𝙤𝙪 𝙖𝙧𝙚 𝙣𝙤𝙩 𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙.")

    if not _redeems:
        return await update.message.reply_text("📭 𝙉𝙤 𝙧𝙚𝙙𝙚𝙚𝙢 𝙘𝙤𝙙𝙚𝙨 𝙛𝙤𝙪𝙣𝙙.")

    lines = []
    limit = 30  # show only first 30 for readability

    for i, (code, data) in enumerate(_redeems.items()):
        if i >= limit:
            break

        used = "✅ 𝚈𝙴𝚂" if data.get("used") else "❌ 𝙽𝙾"
        credits = data.get("credits", 0)
        created_at = data.get("created_at", "unknown").split("T")[0]
        used_by = data.get("used_by", "—")

        lines.append(
            f"🎟️ 𝙲𝚘𝚍𝚎: `{code}`\n"
            f"   ➤ 𝙲𝚛𝚎𝚍𝚒𝚝𝚜: 𝟣 {credits}\n"
            f"   ➤ 𝚄𝚜𝚎𝚍: {used}\n"
            f"   ➤ 𝚄𝚜𝚎𝚍 𝚋𝚢: {used_by}\n"
            f"   ➤ 𝙲𝚛𝚎𝚊𝚝𝚎𝚍: {created_at}\n"
        )

    text = "\n".join(lines)
    if len(_redeems) > limit:
        text += f"\n\n… and {len(_redeems)-limit} more codes."

    await update.message.reply_text(
        f"📜 𝚁𝚎𝚍𝚎𝚎𝚖 𝙲𝚘𝚍𝚎𝚜 (showing {min(limit, len(_redeems))}):\n\n{text}",
        parse_mode="Markdown"
    )



async def redeem_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Entry point for redeem conversation.
    This handles both /free command and callback_query from inline menu (pattern '^redeem$').
    """
    # if callback button pressed
    if update.callback_query:
        q = update.callback_query
        await q.answer()
        # send a fresh message prompting for code
        await q.message.reply_text(
            "🎟️ 𝗥𝗲𝗱𝗲𝗲𝗺 𝗖𝗼𝘂𝗽𝗼𝗻 🎟️\n\n"
            "Please send your coupon code to redeem credits.\n\n"
            "Example: `ABC12345`",
            parse_mode="Markdown"
        )
    else:
        # plain command
        await update.message.reply_text(
            "🔑 Enter your redeem code (example: ABC12345):"
        )
    return WAITING_CODE


async def redeem_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process the redeem code (user message)."""
    uid = update.effective_user.id
    code = update.message.text.strip().upper()

    data = _redeems.get(code)
    if not data:
        await update.message.reply_text("❌ Invalid redeem code.")
        return ConversationHandler.END

    if data.get("used"):
        await update.message.reply_text("⚠️ This code has already been used.")
        return ConversationHandler.END

    # Add credits to user
    credits = int(data.get("credits", 0))
    user = get_user(uid)
    old_credits = user.get("credits", 0)
    user["credits"] = old_credits + credits

    # optional metadata
    data["used"] = True
    data["used_by"] = uid
    data["used_at"] = datetime.datetime.utcnow().isoformat()

    # persist
    save_user(uid)
    save_json(REDEEMS_FILE, _redeems)

    # ✅ Notify user
    await update.message.reply_text(
        f"🎉 Successfully redeemed {credits} credits!\n"
        f"💳 Total Credits: {user.get('credits', 0)}"
    )

    # ✅ Notify Admin(s)
    for admin_id in ADMINS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=(
                    f"📢 <b>Redeem Used</b>\n\n"
                    f"👤 User: <a href='tg://user?id={uid}'>{update.effective_user.first_name}</a> ({uid})\n"
                    f"🎟️ Code: <code>{code}</code>\n"
                    f"💳 Credits: {credits}\n"
                    f"⏰ Time: {data['used_at']}"
                ),
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Failed to notify admin {admin_id}: {e}")

    return ConversationHandler.END



async def redeem_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation"""
    if update.callback_query:
        await update.callback_query.answer()
    if update.message:
        await update.message.reply_text("❌ Redeem process cancelled.")
    return ConversationHandler.END
