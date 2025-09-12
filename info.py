import logging
import requests
import json
import os
import random
import string
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ConversationHandler, ContextTypes, filters
)

# ===== CONFIGURATION =====
BOT_TOKEN = "8245872361:AAFFOP814_N1VI6brkwbR58LCnRIq13RBhQ"
FORCE_CHANNELS = ["@free_info_gc", "@GODCYBER_INFO"]
API_KEY = "MK103020070811"
API_URL = "https://numlooking.rf.gd/index.php"
DATA_FILE = "users.json"
REDEEM_FILE = "redeem.json"

# ===== Logging =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== Utils: Data Persistence =====
def load_json(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

users = load_json(DATA_FILE)
redeems = load_json(REDEEM_FILE)

def get_user(uid):
    if str(uid) not in users:
        users[str(uid)] = {
            "credits": 1,
            "free_used": False,
            "banned": False,
            "is_admin": False
        }
        save_json(DATA_FILE, users)
    return users[str(uid)]

def save_user(uid):
    save_json(DATA_FILE, users)

def save_redeems():
    save_json(REDEEM_FILE, redeems)

# ===== ADMIN LIST =====
ADMINS = {7850839661}

# ===== GLOBAL MAINTENANCE FLAG =====
MAINTENANCE_MODE = False

# ===== FORCE JOIN CHECK =====
async def check_force_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    try:
        for channel in FORCE_CHANNELS:
            member = await context.bot.get_chat_member(channel, uid)
            if member.status not in ["member", "administrator", "creator"]:
                return True
    except:
        return True
    return True

# ===== Redeem System =====
def generate_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

async def redeem_create(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return await update.message.reply_text("🚫 You are not authorized.")
    if not context.args:
        return await update.message.reply_text("Usage: /redeem <credits>")
    try:
        credits = int(context.args[0])
    except:
        return await update.message.reply_text("Credits must be a number.")
    code = generate_code()
    redeems[code] = {"credits": credits, "used": False}
    save_redeems()
    await update.message.reply_text(f"✅ Redeem code created:\n\nCode: `{code}`\nCredits: {credits}", parse_mode="Markdown")

WAITING_CODE = 1

async def free_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if MAINTENANCE_MODE and update.effective_user.id not in ADMINS:
        return await update.message.reply_text("🚧 Bot is under maintenance. Please try again later.")
    await update.message.reply_text("🔑 Enter your redeem code:")
    return WAITING_CODE

async def free_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    code = update.message.text.strip().upper()
    if code not in redeems:
        await update.message.reply_text("❌ Invalid redeem code.")
        return ConversationHandler.END
    if redeems[code]["used"]:
        await update.message.reply_text("⚠️ This code has already been used.")
        return ConversationHandler.END
    credits = redeems[code]["credits"]
    redeems[code]["used"] = True
    users[uid]["credits"] += credits
    save_user(uid)
    save_redeems()
    await update.message.reply_text(f"🎉 Successfully redeemed {credits} credits!")
    return ConversationHandler.END

async def free_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Redeem process cancelled.")
    return ConversationHandler.END

# ===== Add Credit Command =====
async def addcredit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return await update.message.reply_text("🚫 You are not authorized.")
    if len(context.args) < 2:
        return await update.message.reply_text("Usage: /addcredit <chatid> <amount>")
    try:
        target = str(context.args[0])
        amount = int(context.args[1])
        if target not in users:
            get_user(target)
        users[target]["credits"] += amount
        save_user(target)
        await update.message.reply_text(f"✅ Added {amount} credits to user {target}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# ===== Ban & Unban =====
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return await update.message.reply_text("🚫 You are not authorized.")
    if not context.args:
        return await update.message.reply_text("Usage: /ban <chatid>")
    target = str(context.args[0])
    if target not in users:
        get_user(target)
    users[target]["banned"] = True
    save_user(target)
    await update.message.reply_text(f"🚫 User {target} has been banned.")

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return await update.message.reply_text("🚫 You are not authorized.")
    if not context.args:
        return await update.message.reply_text("Usage: /unban <chatid>")
    target = str(context.args[0])
    if target not in users:
        get_user(target)
    users[target]["banned"] = False
    save_user(target)
    await update.message.reply_text(f"✅ User {target} has been unbanned.")

# ===== Total Users =====
async def total(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return await update.message.reply_text("🚫 You are not authorized.")
    total_users = len(users)
    banned_users = sum(1 for u in users.values() if u["banned"])
    active_users = total_users - banned_users
    await update.message.reply_text(
        f"📊 Bot Stats:\n\n"
        f"👥 Total Users: {total_users}\n"
        f"✅ Active Users: {active_users}\n"
        f"🚫 Banned Users: {banned_users}"
    )

# ===== Broadcast =====
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return await update.message.reply_text("🚫 You are not authorized.")
    if not context.args:
        return await update.message.reply_text("Usage: /broadcast <message>")
    msg = " ".join(context.args)
    sent, failed = 0, 0
    for uid in users.keys():
        try:
            await context.bot.send_message(chat_id=int(uid), text=msg)
            sent += 1
        except:
            failed += 1
    await update.message.reply_text(f"📢 Broadcast done!\n✅ Sent: {sent}\n❌ Failed: {failed}")

# ===== Start Menu =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if MAINTENANCE_MODE and update.effective_user.id not in ADMINS:
        return await update.message.reply_text("🚧 Bot is under maintenance. Please try again later.")
    uid = update.effective_user.id
    user = get_user(uid)
    if user["banned"]:
        return await update.message.reply_text("🚫 You are banned from using this bot.")
    if not await check_force_join(update, context):
        buttons = [[InlineKeyboardButton(f"Join {ch}", url=f"https://t.me/{ch[1:]}")] for ch in FORCE_CHANNELS]
        buttons.append([InlineKeyboardButton("I am Joined ✅", callback_data="joined")])
        return await update.message.reply_text("Please join required channels to use this bot:", reply_markup=InlineKeyboardMarkup(buttons))
    menu = [
        [InlineKeyboardButton("🔍 Search Number", callback_data="search")],
        [InlineKeyboardButton("👤 My Account", callback_data="account")],
        [InlineKeyboardButton("💳 UPI Info", callback_data="upi")],
        [InlineKeyboardButton("💳 Recharge & Access Plans", callback_data="plans")],
        [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/PIYUSH_SUPPORT_BOT")],
    ]
    await update.message.reply_text(f"👋 Hello {update.effective_user.first_name}, welcome!", reply_markup=InlineKeyboardMarkup(menu))

# ===== Maintenance =====
async def maintenance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global MAINTENANCE_MODE
    if update.effective_user.id not in ADMINS:
        return await update.message.reply_text("🚫 You are not authorized.")
    MAINTENANCE_MODE = not MAINTENANCE_MODE
    await update.message.reply_text(f"⚙️ Maintenance mode: {'ON' if MAINTENANCE_MODE else 'OFF'}")

# ===== Search Number =====
async def search_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🔍 Please send the number you want to search:")
    context.user_data["waiting_for_number"] = True

# ===== Search Number =====
async def number_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    user = get_user(uid)

    if user["banned"]:
        return await update.message.reply_text("🚫 You are banned from using this bot.")

    if user["credits"] <= 0:
        return await update.message.reply_text("⚠️ You don’t have enough credits. Please recharge.")

    if context.user_data.get("waiting_for_number"):
        number = update.message.text.strip()
        context.user_data["waiting_for_number"] = False

        # New API URL
        params = {"key": API_KEY, "num": number}
        response = requests.get("https://numlooking.rf.gd/index.php", params=params, timeout=10)
        try:
            data_json = response.json()

            if data_json.get("status") != "success" or not data_json.get("data"):
                return await update.message.reply_text("❌ No data found for this number.")

            # Deduct 1 credit
            user["credits"] -= 1
            save_user(uid)

            # Avoid duplicate entries
            seen = set()
            for entry in data_json["data"]:
                mobile = entry.get("mobile", "-")
                if mobile in seen:
                    continue
                seen.add(mobile)

                text = (
                    f"📱 **Mobile:** `{mobile}`\n"
                    f"👤 **Name:** {entry.get('name', '-')}\n"
                    f"👨‍👦 **Father:** {entry.get('fname', '-')}\n"
                    f"🏠 **Address:** {entry.get('address', '-').replace('!', ' ').strip()}\n"
                    f"📞 **Alt:** {entry.get('alt', '-')}\n"
                    f"🌍 **Circle:** {entry.get('circle', '-')}\n"
                    f"🆔 **ID:** {entry.get('id', '-')}\n"
                    f"💳 Credit: {entry.get('credit', '-')}\n"
                    f"━━━━━━━━━━━━━━━"
                )
                await update.message.reply_text(text, parse_mode="Markdown")

        except Exception as e:
            await update.message.reply_text(f"⚠️ Error: {e}")



# ===== Handle "I am Joined" button =====
async def joined_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not await check_force_join(update, context):
        await query.edit_message_text("❌ You still need to join all required channels.")
        return
    
    menu = [
        [InlineKeyboardButton("🔍 Search Number", callback_data="search")],
        [InlineKeyboardButton("👤 My Account", callback_data="account")],
        [InlineKeyboardButton("💳 UPI Info", callback_data="upi")],
        [InlineKeyboardButton("💳 Recharge & Access Plans", callback_data="plans")],
        [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/LearnOnix")],
    ]
    await query.edit_message_text("✅ Thank you! Now you can use the bot:", reply_markup=InlineKeyboardMarkup(menu))




# ===== Help =====
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📌 Commands:\n\n"
        "👤 User:\n"
        "/start - Open menu\n"
        "/free - Redeem code\n"
        "/help - Help menu\n\n"
        "👑 Admin:\n"
        "/redeem <credits> - Create redeem code\n"
        "/addcredit <chatid> <amount> - Add credits\n"
        "/ban <chatid> - Ban user\n"
        "/unban <chatid> - Unban user\n"
        "/total - Show total users\n"
        "/broadcast <msg> - Send message to all users\n"
        "/maintenance - Toggle maintenance\n"
    )
    await update.message.reply_text(text)

# ===== Main =====
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("redeem", redeem_create))
    application.add_handler(CommandHandler("addcredit", addcredit))
    application.add_handler(CommandHandler("ban", ban))
    application.add_handler(CommandHandler("unban", unban))
    application.add_handler(CommandHandler("total", total))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("maintenance", maintenance))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(CallbackQueryHandler(joined_callback, pattern="joined"))

    application.add_handler(CallbackQueryHandler(search_callback, pattern="search"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, number_handler))


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("free", free_start)],
        states={WAITING_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, free_process)]},
        fallbacks=[CommandHandler("cancel", free_cancel)],
    )
    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == "__main__":
    main()
