from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from modules.user import get_user

async def refer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    user_id = update.effective_user.id
    user = get_user(user_id)

    # Referral link
    refer_link = f"https://t.me/CYBER_infoo_bot?start={user_id}"

    # Stylish Text (Mathematical Bold)
    text = (
        "👥 𝗥𝗲𝗳𝗲𝗿 & 𝗘𝗮𝗿𝗻 👥\n\n"
        "🎯 𝗦𝗵𝗮𝗿𝗲 𝘆𝗼𝘂𝗿 𝗿𝗲𝗳𝗲𝗿𝗿𝗮𝗹 𝗹𝗶𝗻𝗸 𝗮𝗻𝗱 𝗲𝗮𝗿𝗻 𝗰𝗿𝗲𝗱𝗶𝘁𝘀!\n\n"
        f"🔗 𝗬𝗼𝘂𝗿 𝗿𝗲𝗳𝗲𝗿𝗿𝗮𝗹 𝗹𝗶𝗻𝗸:\n`{refer_link}`\n\n"
        f"💰 𝗥𝗲𝘄𝗮𝗿𝗱: 1 𝗰𝗿𝗲𝗱𝗶𝘁 𝗽𝗲𝗿 𝗿𝗲𝗳𝗲𝗿𝗿𝗮𝗹\n"
        f"👥 𝗧𝗼𝘁𝗮𝗹 𝗿𝗲𝗳𝗲𝗿𝗿𝗮𝗹𝘀: `{len(user.get('referrals', []))}`\n\n"
        "📋 𝗛𝗼𝘄 𝗶𝘁 𝘄𝗼𝗿𝗸𝘀:\n"
        "• 𝗦𝗵𝗮𝗿𝗲 𝘆𝗼𝘂𝗿 𝗹𝗶𝗻𝗸 𝘄𝗶𝘁𝗵 𝗳𝗿𝗶𝗲𝗻𝗱𝘀\n"
        "• 𝗧𝗵𝗲𝘆 𝗷𝗼𝗶𝗻 𝘂𝘀𝗶𝗻𝗴 𝘆𝗼𝘂𝗿 𝗹𝗶𝗻𝗸\n"
        "• 𝗬𝗼𝘂 𝗯𝗼𝘁𝗵 𝗴𝗲𝘁 𝗿𝗲𝘄𝗮𝗿𝗱𝗲𝗱!\n\n"
        "✨ 𝗦𝘁𝗮𝗿𝘁 𝘀𝗵𝗮𝗿𝗶𝗻𝗴 𝗮𝗻𝗱 𝗲𝗮𝗿𝗻𝗶𝗻𝗴 𝗻𝗼𝘄! ✨"
    )

    # Buttons
    buttons = [
        [InlineKeyboardButton("💬 Contact Admin", url="https://t.me/PIYUSH_SUPPORT_BOT")],
        [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
    ]

    await q.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
