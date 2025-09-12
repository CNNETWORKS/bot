import requests
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from modules.user import get_user, save_user, is_banned

REQUIRED_CREDITS = 1  # credits per Instagram search


async def insta_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Runs when /insta command OR 'Instagram' button is clicked"""
    uid = str(update.effective_user.id)

    if is_banned(uid):
        return await update.message.reply_text(
            "🚫 𝒀𝒐𝒖 𝒂𝒓𝒆 𝒃𝒂𝒏𝒏𝒆𝒅 𝒇𝒓𝒐𝒎 𝒖𝒔𝒊𝒏𝒈 𝒕𝒉𝒊𝒔 𝒃𝒐𝒕."
        )

    # Case 1: /insta <username>
    if update.message and context.args:
        username = " ".join(context.args).strip().lstrip("@")
        return await process_insta(update, context, username)

    # Case 2: /insta (without args) or button
    text = (
        "📸 <b>𝑰𝒏𝒔𝒕𝒂𝒈𝒓𝒂𝒎 𝑺𝒆𝒂𝒓𝒄𝒉 𝑺𝒆𝒓𝒗𝒊𝒄𝒆</b> 📸\n\n"
        "👤 <b>Please send the Instagram username</b> you want to search.\n\n"
        "📝 <b>Format:</b> <code>@username</code>\n"
        f"💰 <b>Cost:</b> {REQUIRED_CREDITS} Credit\n\n"
        "👉 Example: <code>/insta virat.kohli</code>"
    )

    keyboard = [[InlineKeyboardButton("🔙 𝑩𝒂𝒄𝒌", callback_data="main_menu")]]

    # Set waiting flag
    context.user_data["waiting_for_insta"] = True

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        return await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
    else:
        return await update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )


async def insta_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles free-text input after /insta"""
    if context.user_data.get("waiting_for_insta"):
        context.user_data["waiting_for_insta"] = False
        username = update.message.text.strip().lstrip("@")
        return await process_insta(update, context, username)


async def process_insta(update: Update, context: ContextTypes.DEFAULT_TYPE, username: str):
    """Fetch and display Instagram profile info"""
    uid = str(update.effective_user.id)
    user = get_user(uid)

    if is_banned(uid):
        return await update.message.reply_text(
            "🚫 𝒀𝒐𝒖 𝒂𝒓𝒆 𝒃𝒂𝒏𝒏𝒆𝒅 𝒇𝒓𝒐𝒎 𝒖𝒔𝒊𝒏𝒈 𝒕𝒉𝒊𝒔 𝒃𝒐𝒕."
        )

    current_credits = user.get("credits", 0)
    if current_credits < REQUIRED_CREDITS:
        keyboard = [[InlineKeyboardButton("🔙 𝑩𝒂𝒄𝒌", callback_data="main_menu")]]
        return await update.message.reply_text(
            f"❌ 𝑰𝒏𝒔𝒖𝒇𝒇𝒊𝒄𝒊𝒆𝒏𝒕 𝑪𝒓𝒆𝒅𝒊𝒕𝒔!\n\n"
            f"𝒀𝒐𝒖 𝒏𝒆𝒆𝒅 {REQUIRED_CREDITS} 𝒄𝒓𝒆𝒅𝒊𝒕 𝒕𝒐 𝒔𝒆𝒂𝒓𝒄𝒉 𝑰𝒏𝒔𝒕𝒂 𝒑𝒓𝒐𝒇𝒊𝒍𝒆.\n"
            f"𝒀𝒐𝒖𝒓 𝒃𝒂𝒍𝒂𝒏𝒄𝒆: {current_credits}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # Encode username for URL safety
    safe_username = urllib.parse.quote(username)
    url = f"https://instagram-api-ashy.vercel.app/api/ig-profile.php?username={safe_username}"

    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        if data.get("status") != "ok":
            return await update.message.reply_text(
                "❌ 𝑵𝒐 𝒅𝒂𝒕𝒂 𝒇𝒐𝒖𝒏𝒅 𝒇𝒐𝒓 𝒕𝒉𝒊𝒔 𝒖𝒔𝒆𝒓𝒏𝒂𝒎𝒆."
            )

        profile = data["profile"]

        # Deduct credit
        user["credits"] = max(0, current_credits - REQUIRED_CREDITS)
        save_user(uid)

        # Direct Instagram link
        insta_link = f"https://instagram.com/{profile.get('username', '')}"

        text = (
            "✨ 𝑰𝒏𝒔𝒕𝒂𝒈𝒓𝒂𝒎 𝑷𝒓𝒐𝒇𝒊𝒍𝒆 𝑰𝒏𝒇𝒐 ✨\n\n"
            f"👤 𝑵𝒂𝒎𝒆: {profile.get('full_name', '-')}\n"
            f"🔗 𝑼𝒔𝒆𝒓𝒏𝒂𝒎𝒆: @{profile.get('username', '-')}\n"
            f"📝 𝑩𝒊𝒐: {profile.get('biography', '-')}\n"
            f"✅ 𝑽𝒆𝒓𝒊𝒇𝒊𝒆𝒅: {'✔️ Yes' if profile.get('is_verified') else '❌ No'}\n"
            f"🔒 𝑷𝒓𝒊𝒗𝒂𝒕𝒆: {'🔐 Yes' if profile.get('is_private') else '🌍 No'}\n\n"
            f"📊 𝑭𝒐𝒍𝒍𝒐𝒘𝒆𝒓𝒔: {profile['edge_counts'].get('followers', 0):,}\n"
            f"📊 𝑭𝒐𝒍𝒍𝒐𝒘𝒊𝒏𝒈: {profile['edge_counts'].get('following', 0):,}\n"
            f"📸 𝑷𝒐𝒔𝒕𝒔: {profile['edge_counts'].get('posts', 0):,}\n"
            "━━━━━━━━━━━━━━━\n"
            f"🔗 <a href='{insta_link}'>𝑶𝒑𝒆𝒏 𝑷𝒓𝒐𝒇𝒊𝒍𝒆</a>"
        )

        keyboard = [[InlineKeyboardButton("🔙 𝑩𝒂𝒄𝒌", callback_data="main_menu")]]
        await update.message.reply_photo(
            photo=profile.get("profile_pic_url_hd"),
            caption=text,
            parse_mode="HTML",  # HTML needed for clickable link
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    except requests.RequestException:
        await update.message.reply_text("⚠️ 𝑵𝒆𝒕𝒘𝒐𝒓𝒌 𝒆𝒓𝒓𝒐𝒓.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ 𝑬𝒓𝒓𝒐𝒓 𝒐𝒄𝒄𝒖𝒓𝒆𝒅: {e}")
