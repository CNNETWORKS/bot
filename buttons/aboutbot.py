from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes



async def guide_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message_text = (
        "🌟 ═══════════════════════════════════ 🌟\n"
        "                    ℹ️ 𝗛𝗢𝗪 𝗧𝗢 𝗨𝗦𝗘 𝗚𝗨𝗜𝗗𝗘\n"
        "🌟 ═══════════════════════════════════ 🌟\n\n"
        "🚀 𝗧𝗵𝗶𝘀 𝗶𝘀 𝗮 𝗣𝗼𝘄𝗲𝗿𝗳𝘂𝗹 𝗕𝗼𝘁! 𝗥𝗲𝗮𝗱 𝗧𝗵𝗶𝘀 𝗕𝗲𝗳𝗼𝗿𝗲 𝗬𝗼𝘂 𝗦𝘁𝗮𝗿𝘁 𝗨𝘀𝗶𝗻𝗴 𝗜𝘁\n\n"
        "📋 𝗛𝗲𝗿𝗲'𝘀 𝗲𝘃𝗲𝗿𝘆𝘁𝗵𝗶𝗻𝗴 𝘆𝗼𝘂 𝗻𝗲𝗲𝗱 𝘁𝗼 𝗸𝗻𝗼𝘄 𝘀𝘁𝗲𝗽-𝗯𝘆-𝘀𝘁𝗲𝗽:\n\n"
        "🔸 𝟭 📱 𝗠𝗼𝗯𝗶𝗹𝗲 𝗡𝘂𝗺𝗯𝗲𝗿 𝗟𝗼𝗼𝗸𝘂𝗽\n"
        "   ✨ Extract detailed information using just a mobile number\n\n"
        "🔸 𝟮 🆔 𝗔𝗮𝗱𝗵𝗮𝗮𝗿 𝗖𝗮𝗿𝗱 𝗟𝗼𝗼𝗸𝘂𝗽\n"
        "   ✨ Get comprehensive data using an Aadhaar card number\n\n"
        "🔸 𝟯 🚗 𝗩𝗲𝗵𝗶𝗰𝗹𝗲 𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻\n"
        "   ✨ Discover vehicle details and registration info\n\n"
        "🔸 𝟰 🔍 𝗕𝗿𝗲𝗮𝗰𝗵 𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻\n"
        "   ✨ Check if your data has been compromised in breaches\n\n"
        "🔸 𝟱 📋 𝗥𝗮𝘁𝗶𝗼𝗻 𝗖𝗮𝗿𝗱 𝗦𝗲𝗮𝗿𝗰𝗵\n"
        "   ✨ Access ration card and family member details\n\n"
        "🔸 𝟲 💳 𝗙𝗮𝗺𝗣𝗮𝘆 𝗜𝗻𝗳𝗼\n"
        "   ✨ FamPay info also available here\n\n"
        "⚠️ 𝗗𝗶𝘀𝗰𝗹𝗮𝗶𝗺𝗲𝗿\n"
        "🔒 This bot is designed for anonymous usage\n"
        "🛡️ Your identity remains private at all times\n"
        "✅ Safe and secure – absolutely nothing to worry about\n\n"
        "🌟 ═══════════════════════════════════ 🌟\n"
        "           𝗘𝗻𝗷𝗼𝘆 𝗨𝘀𝗶𝗻𝗴 𝗢𝘂𝗿 𝗦𝗲𝗿𝘃𝗶𝗰𝗲!\n"
        "🌟 ═══════════════════════════════════ 🌟"
    )

    if update.callback_query:  
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(message_text, reply_markup=reply_markup)


# Callback handler for Back button
async def guide_back_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # Replace with your main menu function
    await query.edit_message_text("🏠 Main Menu\nSelect an option to continue:")
