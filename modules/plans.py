from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def plans_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    text = (
        "💳 𝗥𝗲𝗰𝗵𝗮𝗿𝗴𝗲 & 𝗔𝗰𝗰𝗲𝘀𝘀 𝗣𝗹𝗮𝗻𝘀\n\n"
        "🔍 1 Credit = 1 Search\n\n"
        "⚡️ 𝗖𝗿𝗲𝗱𝗶𝘁-𝗕𝗮𝘀𝗲𝗱 𝗣𝗹𝗮𝗻𝘀\n"
        "New Rates 🚨 – Value Meets Performance\n"
        "💰 ₹100 = 35 Credits\n"
        "💰 ₹200 = 55 Credits\n"
        "💰 ₹300 = 80 Credits\n"
        "💰 ₹400 = 105 Credits\n"
        "💰 ₹500 = 200+ Credits\n"
        "💰 ₹700 = 300+ Credits\n"
        "💰 ₹1,000 = 450+ Credits\n"
        "💥 ₹1,500 = 500+ Credits\n"
        "📌 Need more credits? Just message the admin!\n"
        "────────────────────\n"
        "🔓 𝗨𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱 𝗣𝗹𝗮𝗻𝘀\n"
        "Unlimited Searches 🚀\n"
        "🗓 7 Days – ₹1,000\n"
        "🗓 15 Days – ₹2,000\n"
        "🗓 30 Days – ₹3,000\n"
        "🗓 1 Year – ₹10,000\n"
        "────────────────────\n"
        "🛠 𝗔𝗣𝗜 𝗔𝗰𝗰𝗲𝘀𝘀 𝗣𝗹𝗮𝗻𝘀\n"
        "For Developers & Bots 🧩\n"
        "🔹 Basic – ₹1,000 (7 Days)\n"
        "🔹 Standard – ₹1,400 (15 Days)\n"
        "🔹 Premium – ₹3,500 (30 Days)\n"
        "💥 Business – ₹8,000 (1 Year)\n"
        "────────────────────\n"
        "📞 𝗥𝗲𝗮𝗱𝘆 𝘁𝗼 𝗕𝘂𝘆?\n"
        "🧑‍💻 Want Bot Source Code or Full Setup?\n"
        "💬 Contact Admin\n"
        "💬 Message Support Bot\n"
        "👇"
    )

    buttons = [
        [InlineKeyboardButton("💬 Contact Support Bot", url="https://t.me/PIYUSH_SUPPORT_BOT")],
        [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
    ]

    await q.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
