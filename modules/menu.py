from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import FORCE_CHANNELS, SUPPORT_CONTACT
from .admin import MAINTENANCE_MODE
from .user import get_user,save_user, is_banned



async def _check_force_join(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    uid = update.effective_user.id
    try:
        for channel in FORCE_CHANNELS:
            member = await context.bot.get_chat_member(channel, uid)
            if member.status not in ["member", "administrator", "creator"]:
                return False
    except Exception:
        # If check fails (e.g., bot not admin in channel), block usage to be safe
        return False
    return True

def _main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📱 𝐍𝐮𝐦𝐛𝐞𝐫 𝐈𝐧𝐟𝐨", callback_data="search")],

        [InlineKeyboardButton("🆔 𝐀𝐝𝐡𝐚𝐫 𝐈𝐧𝐟𝐨", callback_data="adhar"),
         InlineKeyboardButton("💳 𝐁𝐈𝐍 𝐃𝐞𝐭𝐚𝐢𝐥𝐬", callback_data="bininfo")],
        
        [InlineKeyboardButton("🚗 𝐕𝐞𝐡𝐢𝐜𝐥𝐞 𝐈𝐧𝐟𝐨", callback_data="vehicle"),
         InlineKeyboardButton("💳 𝐅𝐀𝐌𝐏𝐀𝐘 𝐈𝐧𝐟𝐨", callback_data="fampay")],

        [InlineKeyboardButton("🔍 𝐁𝐑𝐄𝐀𝐂𝐇 𝐃𝐀𝐓𝐀", callback_data="breach"),
         InlineKeyboardButton("📷 𝐈𝐧𝐬𝐭𝐚 𝐈𝐧𝐟𝐨", callback_data="insta")],

        
        [InlineKeyboardButton("💰 𝐔𝐏𝐈 𝐈𝐧𝐟𝐨", callback_data="upiinfo"),
         InlineKeyboardButton("🎟️ 𝐑𝐞𝐝𝐞𝐞𝐦 𝐂𝐨𝐝𝐞", callback_data="redeem")],
        
        [InlineKeyboardButton("👥 𝐑𝐞𝐟𝐞𝐫 & 𝐄𝐚𝐫𝐧", callback_data="refer"),
         InlineKeyboardButton("💴 𝐑𝐞𝐜𝐡𝐚𝐫𝐠𝐞 & 𝐏𝐥𝐚𝐧𝐬", callback_data="plans")],
             
        [InlineKeyboardButton("📞 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐀𝐝𝐦𝐢𝐧", url=SUPPORT_CONTACT),
         InlineKeyboardButton("ℹ️ A𝐛𝐨𝐮𝐭 𝐁𝐨𝐭", callback_data="about")
         ],
         [InlineKeyboardButton("🆘 Help", callback_data="help")],
         [InlineKeyboardButton("🔏 𝐏𝐫𝐨𝐭𝐞𝐜𝐭 𝐔 𝐍𝐮𝐦𝐛𝐞𝐫", callback_data="protectnumber")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if MAINTENANCE_MODE["on"] and not get_user(update.effective_user.id).get("is_admin", False):
        return await update.message.reply_text("🚧 Bot is under maintenance. Please try again later.")

    user_id = update.effective_user.id
    args = context.args  

    user = get_user(user_id)

    if user.get("referred_by") is None and args:
        try:
            ref_id = int(args[0])
            if ref_id != user_id: 
                user["referred_by"] = ref_id
                referrer = get_user(ref_id)
                referrer["credits"] = referrer.get("credits", 0) + 1
                referrer.setdefault("referrals", []).append(user_id)
                save_user(ref_id)
                save_user(user_id)
        except Exception:
            pass

        if user.get("banned"):
          buttons = InlineKeyboardMarkup([
          [InlineKeyboardButton("📞 Contact Admin", url=SUPPORT_CONTACT)]
          ])
        return await update.message.reply_text(
           "🚫 You are banned from using this bot.\n\n"
           "👉 Tap below to contact admin for support.",
            reply_markup=buttons
      )

    if not await _check_force_join(update, context):
        buttons = [[InlineKeyboardButton(f"Join {ch}", url=f"https://t.me/{ch[1:]}")] for ch in FORCE_CHANNELS]
        buttons.append([InlineKeyboardButton("I am Joined ✅", callback_data="joined")])
        return await update.message.reply_text(
            "Please join required channels to use this bot:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    await update.message.reply_text(
    f"  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    f"  ⚫️⚫️⚫️ <b>Cʏʙᴇʀ Iɴғᴏ Osɪɴᴛ</b> ⚫️⚫️⚫️   \n"
    f"  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    f"  👤 <b>𝐔𝐬𝐞𝐫:</b> <code>{update.effective_user.first_name}</code>\n"
    f"  🆔 <b>𝐈𝐃:</b> <code>{user_id}</code>\n"
    f"  💰 <b>𝐂𝐫𝐞𝐝𝐢𝐭𝐬:</b> <code>{user.get('credits', 0)}</code>\n"
    f"  👥 <b>𝐑𝐞𝐟𝐞𝐫𝐫𝐚𝐥𝐬:</b> <code>{len(user.get('referrals', []))}</code>\n\n"
    f"  ✅ <b>𝐒𝐭𝐚𝐭𝐮𝐬:</b> <span class='tg-spoiler'>𝐀𝐂𝐓𝐈𝐕𝐄</span>\n"
    f"  ━━━━━━━━━━━━━━",
    reply_markup=_main_menu(),
    parse_mode="HTML"
)



async def joined_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not await _check_force_join(update, context):
        return await query.edit_message_text("❌ You still need to join all required channels.")

    await query.edit_message_text("✅ Thank you! Now you can use the bot:", reply_markup=_main_menu())

async def account_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    user = get_user(update.effective_user.id)
    text = (
        "👤 **My Account**\n\n"
        f"🆔 ID: `{update.effective_user.id}`\n"
        f"💰 Credits: `{user.get('credits', 3)}`\n"
        f"🚫 Banned: `{user.get('banned', False)}`"
    )
    await q.edit_message_text(text, parse_mode="Markdown", reply_markup=_main_menu())



async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    user_id = update.effective_user.id
    user = get_user(user_id)

    await q.edit_message_text(
        f"  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"  ⚫️⚫️⚫️ <b>Cʏʙᴇʀ Iɴғᴏ Osɪɴᴛ</b> ⚫️⚫️⚫️   \n"
        f"  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  👤 <b>𝐔𝐬𝐞𝐫:</b> <code>{update.effective_user.first_name}</code>\n"
        f"  🆔 <b>𝐈𝐃:</b> <code>{user_id}</code>\n"
        f"  💰 <b>𝐂𝐫𝐞𝐝𝐢𝐭𝐬:</b> <code>{user.get('credits', 0)}</code>\n"
        f"  👥 <b>𝐑𝐞𝐟𝐞𝐫𝐫𝐚𝐥𝐬:</b> <code>{len(user.get('referrals', []))}</code>\n\n"
        f"  ✅ <b>𝐒𝐭𝐚𝐭𝐮𝐬:</b> <span class='tg-spoiler'>𝐀𝐂𝐓𝐈𝐕𝐄</span>\n"
        f"  ━━━━━━━━━━━━━━",
        reply_markup=_main_menu(),
        parse_mode="HTML"
    )
