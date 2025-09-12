# from telegram import Update
# from telegram.ext import ContextTypes, ConversationHandler
# from modules.user import get_user, save_user
# from modules.utils import load_json, save_json
# from config import REDEEMS_FILE

# WAITING_CODE = 1

# # Load redeem codes
# _redeems = load_json(REDEEMS_FILE)

# # Step 1: User starts redeem
# async def redeem_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(
#         "🎟️ 𝗥𝗲𝗱𝗲𝗲𝗺 𝗖𝗼𝘂𝗽𝗼𝗻 🎟️\n\n"
#         "📝 𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗲𝗻𝗱 𝘆𝗼𝘂𝗿 𝗰𝗼𝘂𝗽𝗼𝗻 𝗰𝗼𝗱𝗲 𝘁𝗼 𝗿𝗲𝗱𝗲𝗲𝗺 𝗰𝗿𝗲𝗱𝗶𝘁𝘀.\n\n"
#         "💡 𝗧𝗶𝗽: 𝗖𝗼𝘂𝗽𝗼𝗻 𝗰𝗼𝗱𝗲𝘀 𝗮𝗿𝗲 𝘂𝘀𝘂𝗮𝗹𝗹𝘆 𝟴 𝗰𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿𝘀 𝗹𝗼𝗻𝗴\n"
#         "📋 𝗘𝘅𝗮𝗺𝗽𝗹𝗲: ABC12345\n\n"
#         "👇 𝗦𝗲𝗻𝗱 𝘁𝗵𝗲 𝗰𝗼𝘂𝗽𝗼𝗻 𝗰𝗼𝗱𝗲 𝗻𝗼𝘄:"
#     )
#     return WAITING_CODE

# # Step 2: Process redeem code
# async def redeem_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     uid = str(update.effective_user.id)
#     code = update.message.text.strip().upper()

#     data = _redeems.get(code)
#     if not data:
#         await update.message.reply_text("❌ Invalid redeem code.")
#         return ConversationHandler.END

#     if data.get("used"):
#         await update.message.reply_text("⚠️ This code has already been used.")
#         return ConversationHandler.END

#     # Add credits to user
#     credits = int(data.get("credits", 0))
#     user = get_user(uid)
#     old_credits = user.get("credits", 0)
#     user["credits"] = old_credits + credits
#     save_user(uid)

#     # Mark code as used
#     data["used"] = True
#     save_json(REDEEMS_FILE, _redeems)

#     await update.message.reply_text(
#         f"🎉 𝗦𝘂𝗰𝗰𝗲𝘀𝗳𝘂𝗹𝗹𝘆 𝗿𝗲𝗱𝗲𝗲𝗺𝗲𝗱!\n\n"
#         f"💳 𝗖𝗿𝗲𝗱𝗶𝘁𝘀 𝗔𝗱𝗱𝗲𝗱: {credits}\n"
#         f"💰 𝗧𝗼𝘁𝗮𝗹 𝗖𝗿𝗲𝗱𝗶𝘁𝘀: {user['credits']}"
#     )
#     return ConversationHandler.END

# # Step 3: Cancel redeem
# async def redeem_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("❌ Redeem process cancelled.")
#     return ConversationHandler.END
