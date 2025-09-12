from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def help_command(update, context):
    text = (
        "📌 ━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚫⚫⚫ <b>Cʏʙᴇʀ Iɴғᴏ 𝐁𝐨𝐭 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬</b> ⚫⚫⚫\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "👤 <b>𝐔𝐒𝐄𝐑 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬</b>\n"
        "• /start – 𝐎𝐩𝐞𝐧 𝐌𝐚𝐢𝐧 𝐌𝐞𝐧𝐮\n"
        "• /free – 𝐑𝐞𝐝𝐞𝐞𝐦 𝐂𝐫𝐞𝐝𝐢𝐭𝐬\n"
        "• /help – 𝐒𝐡𝐨𝐰 𝐇𝐞𝐥𝐩 𝐌𝐞𝐧𝐮\n"
        "• /num &lt;number&gt; – 𝐒𝐞𝐚𝐫𝐜𝐡 𝐍𝐮𝐦𝐛𝐞𝐫 𝐈𝐧𝐟𝐨\n"
        "• /insta &lt;username&gt; – 𝐒𝐞𝐚𝐫𝐜𝐡 𝐈𝐧𝐬𝐭𝐚𝐠𝐫𝐚𝐦 𝐈𝐧𝐟𝐨\n"
        "• /vehicle &lt;number&gt; – 𝐕𝐞𝐡𝐢𝐜𝐥𝐞 𝐈𝐧𝐟𝐨\n"
        "• /upiinfo &lt;upi&gt; – 𝐔𝐏𝐈 𝐈𝐧𝐟𝐨\n"
        "• /bin <code>6-digit BIN</code> – 𝐁𝐈𝐍 𝐃𝐞𝐭𝐚𝐢𝐥𝐬\n"
        "• /fampay &lt;id&gt; – 𝐅𝐚𝐦𝐩𝐚𝐲 𝐈𝐧𝐟𝐨\n"
        "• /breach &lt;email&gt; – 𝐁𝐫𝐞𝐚𝐜𝐡 𝐃𝐚𝐭𝐚 𝐂𝐡𝐞𝐜𝐤\n\n"
        "👑 <b>𝐀𝐃𝐌𝐈𝐍 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬</b>\n"
        "• /redeem &lt;credits&gt; – 𝐂𝐫𝐞𝐚𝐭𝐞 𝐑𝐞𝐝𝐞𝐞𝐦 𝐂𝐨𝐝𝐞\n"
        "• /redeemlist – 𝐒𝐡𝐨𝐰 𝐀𝐥𝐥 𝐑𝐞𝐝𝐞𝐞𝐦 𝐂𝐨𝐝𝐞𝐬\n"
        "• /addcredit &lt;chatid&gt; &lt;amount&gt; – 𝐀𝐝𝐝 𝐂𝐫𝐞𝐝𝐢𝐭𝐬\n"
        "• /ban &lt;chatid&gt; – 𝐁𝐚𝐧 𝐔𝐬𝐞𝐫\n"
        "• /unban &lt;chatid&gt; – 𝐔𝐧𝐛𝐚𝐧 𝐔𝐬𝐞𝐫\n"
        "• /total – 𝐒𝐡𝐨𝐰 𝐓𝐨𝐭𝐚𝐥 𝐔𝐬𝐞𝐫𝐬\n"
        "• /broadcast &lt;msg&gt; – 𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭 𝐌𝐞𝐬𝐬𝐚𝐠𝐞\n"
        "• /maintenance – 𝐓𝐨𝐠𝐠𝐥𝐞 𝐌𝐚𝐢𝐧𝐭𝐞𝐧𝐚𝐧𝐜𝐞\n"
        "• /protect &lt;number&gt; – 𝐏𝐫𝐨𝐭𝐞𝐜𝐭 𝐀 𝐍𝐮𝐦𝐛𝐞𝐫\n"
        "• /unprotect &lt;number&gt; – 𝐔𝐧𝐩𝐫𝐨𝐭𝐞𝐜𝐭 𝐀 𝐍𝐮𝐦𝐛𝐞𝐫\n"
        "• /listprotected – 𝐋𝐢𝐬𝐭 𝐀𝐥𝐥 𝐏𝐫𝐨𝐭𝐞𝐜𝐭𝐞𝐝 𝐍𝐮𝐦𝐛𝐞𝐫𝐬\n"
    )

    # Main menu buttons
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")],
        [InlineKeyboardButton("💳 Redeem Credits", callback_data="redeem")],
        [InlineKeyboardButton("🔍 Search Number", callback_data="search")],
        [InlineKeyboardButton("📸 Instagram Info", callback_data="insta")],
        [InlineKeyboardButton("🚗 Vehicle Info", callback_data="vehicle")],
        [InlineKeyboardButton("🏦 UPI Info", callback_data="upiinfo")],
        [InlineKeyboardButton("📄 Fampay", callback_data="fampay")],
        [InlineKeyboardButton("💥 Breach Data", callback_data="breach")],
        [InlineKeyboardButton("🛡️ Protect Numbers", callback_data="protectnumber")],
        [InlineKeyboardButton("📝 About Bot", callback_data="about")],
    ])

    if update.message:
        await update.message.reply_text(
            text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=buttons
        )
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.edit_text(
            text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=buttons
        )
