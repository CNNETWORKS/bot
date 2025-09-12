from telegram import Update
from telegram.ext import ContextTypes
from config import ADMINS
from .user import add_credits, set_ban, all_users, totals

MAINTENANCE_MODE = {"on": False}  # tiny mutable flag shared within module

async def addcredit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return await update.message.reply_text("🚫 You are not authorized.")
    if len(context.args) < 2:
        return await update.message.reply_text("Usage: /addcredit <chatid> <amount>")
    try:
        target = int(context.args[0])
        amount = int(context.args[1])
        add_credits(target, amount)
        await update.message.reply_text(f"✅ Added {amount} credits to user {target}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return await update.message.reply_text("🚫 You are not authorized.")
    if not context.args:
        return await update.message.reply_text("Usage: /ban <chatid>")
    target = int(context.args[0])
    set_ban(target, True)
    await update.message.reply_text(f"🚫 User {target} has been banned.")

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return await update.message.reply_text("🚫 You are not authorized.")
    if not context.args:
        return await update.message.reply_text("Usage: /unban <chatid>")
    target = int(context.args[0])
    set_ban(target, False)
    await update.message.reply_text(f"✅ User {target} has been unbanned.")

async def total(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return await update.message.reply_text("🚫 You are not authorized.")
    total_users, banned_users, active_users = totals()
    await update.message.reply_text(
        f"📊 Bot Stats:\n\n"
        f"👥 Total Users: {total_users}\n"
        f"✅ Active Users: {active_users}\n"
        f"🚫 Banned Users: {banned_users}"
    )

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return await update.message.reply_text("🚫 You are not authorized.")
    if not context.args:
        return await update.message.reply_text("Usage: /broadcast <message>")
    msg = " ".join(context.args)
    sent, failed = 0, 0
    for uid in list(all_users().keys()):
        try:
            await context.bot.send_message(chat_id=int(uid), text=msg)
            sent += 1
        except Exception:
            failed += 1
    await update.message.reply_text(f"📢 Broadcast done!\n✅ Sent: {sent}\n❌ Failed: {failed}")

async def maintenance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return await update.message.reply_text("🚫 You are not authorized.")
    MAINTENANCE_MODE["on"] = not MAINTENANCE_MODE["on"]
    await update.message.reply_text(f"⚙️ Maintenance mode: {'ON' if MAINTENANCE_MODE['on'] else 'OFF'}")
