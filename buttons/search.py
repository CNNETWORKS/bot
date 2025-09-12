import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import API_URL,API_KEY, SUPPORT_CONTACT
from modules.user import get_user, save_user, is_banned
from modules.protected import is_protected

REQUIRED_CREDITS = 1  # 𝒄𝒓𝒆𝒅𝒊𝒕𝒔 𝒑𝒆𝒓 𝒏𝒖𝒎𝒃𝒆𝒓 𝒔𝒆𝒂𝒓𝒄𝒉


async def num_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """𝑹𝒖𝒏𝒔 𝒘𝒉𝒆𝒏 /num 𝑶𝑹 '𝑺𝒆𝒂𝒓𝒄𝒉' 𝒃𝒖𝒕𝒕𝒐𝒏 𝒊𝒔 𝒄𝒍𝒊𝒄𝒌𝒆𝒅"""
    uid = str(update.effective_user.id)

    if is_banned(uid):
        return await update.message.reply_text("🚫 𝒀𝒐𝒖 𝒂𝒓𝒆 𝒃𝒂𝒏𝒏𝒆𝒅 𝒇𝒓𝒐𝒎 𝒖𝒔𝒊𝒏𝒈 𝒕𝒉𝒊𝒔 𝒃𝒐𝒕.")

    # /num <number>
    if update.message and context.args:
        return await process_number(update, context, context.args[0].strip())

    # /num (without args) or button
    text = (
        "📱 𝗡𝗨𝗠𝗕𝗘𝗥 𝗜𝗡𝗙𝗢 𝗦𝗘𝗥𝗩𝗜𝗖𝗘 📱\n\n"
        "📞 𝑷𝒍𝒆𝒂𝒔𝒆 𝒔𝒆𝒏𝒅 𝒕𝒉𝒆 𝒑𝒉𝒐𝒏𝒆 𝒏𝒖𝒎𝒃𝒆𝒓 𝒚𝒐𝒖 𝒘𝒂𝒏𝒕 𝒕𝒐 𝒔𝒆𝒂𝒓𝒄𝒉.\n\n"
        f"📝 𝑭𝒐𝒓𝒎𝒂𝒕: <code>10-digit mobile number</code>\n"
        f"💰 𝑪𝒐𝒔𝒕: {REQUIRED_CREDITS} 𝑪𝒓𝒆𝒅𝒊𝒕\n\n"
        "👉 𝑬𝒙𝒂𝒎𝒑𝒍𝒆: <code>/num 6351516535</code>"
    )

    keyboard = [[InlineKeyboardButton("🔙 𝑩𝒂𝒄𝒌", callback_data="main_menu")]]

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
    else:
        await update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )

    context.user_data["waiting_for_number"] = True


async def number_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """𝑯𝒂𝒏𝒅𝒍𝒆𝒔 𝒇𝒓𝒆𝒆-𝒕𝒆𝒙𝒕 𝒊𝒏𝒑𝒖𝒕 𝒂𝒇𝒕𝒆𝒓 /num"""
    if context.user_data.get("waiting_for_number"):
        context.user_data["waiting_for_number"] = False
        number = update.message.text.strip()
        return await process_number(update, context, number)


async def process_number(update: Update, context: ContextTypes.DEFAULT_TYPE, number: str):
    uid = str(update.effective_user.id)
    user = get_user(uid)

    if is_banned(uid):
        return await update.message.reply_text("🚫 𝒀𝒐𝒖 𝒂𝒓𝒆 𝒃𝒂𝒏𝒏𝒆𝒅 𝒇𝒓𝒐𝒎 𝒖𝒔𝒊𝒏𝒈 𝒕𝒉𝒊𝒔 𝒃𝒐𝒕.")


    if is_protected(number):
        return await update.message.reply_text(
            f"🔏 Number {number} is **Protected**.\n❌ No information available."
        )


    current_credits = user.get("credits", 0)
    if current_credits < REQUIRED_CREDITS:
        keyboard = [
            [InlineKeyboardButton("📞 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐀𝐝𝐦𝐢𝐧", url=SUPPORT_CONTACT)],
            [InlineKeyboardButton("🔙 𝑩𝒂𝒄𝒌", callback_data="main_menu")]
        ]
        return await update.message.reply_text(
            f"❌ 𝑰𝒏𝒔𝒖𝒇𝒇𝒊𝒄𝒊𝒆𝒏𝒕 𝑪𝒓𝒆𝒅𝒊𝒕𝒔!\n\n"
            f"𝒀𝒐𝒖 𝒏𝒆𝒆𝒅 {REQUIRED_CREDITS} 𝒄𝒓𝒆𝒅𝒊𝒕𝒔 𝒇𝒐𝒓 𝑵𝒖𝒎𝒃𝒆𝒓 𝑰𝒏𝒇𝒐 𝒔𝒆𝒓𝒗𝒊𝒄𝒆.\n"
            f"𝒀𝒐𝒖𝒓 𝒃𝒂𝒍𝒂𝒏𝒄𝒆: {current_credits}\n\n"
            "💰 𝑼𝒔𝒆 /start 𝒕𝒐 𝒃𝒖𝒚 𝒎𝒐𝒓𝒆 𝒄𝒓𝒆𝒅𝒊𝒕𝒔.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # Step 1: Send searching message
    searching_msg = await update.message.reply_text("⏳ 𝗦𝗲𝗮𝗿𝗰𝗵𝗶𝗻𝗴 𝗻𝘂𝗺𝗯𝗲𝗿 𝗶𝗻𝗳𝗼...")

    # API call
    # url = f"{API_URL}{number}"
    url = f"{API_URL}?key={API_KEY}&type=mobile&term={number}"
    try:
        resp = requests.get(url, timeout=30)  # ज्यादा timeout रखा
        resp.raise_for_status()
        data = resp.json()

        if not data:
            return await searching_msg.edit_text("❌ 𝑵𝒐 𝒅𝒂𝒕𝒂 𝒇𝒐𝒖𝒏𝒅 𝒇𝒐𝒓 𝒕𝒉𝒊𝒔 𝒏𝒖𝒎𝒃𝒆𝒓.")

        # Deduct credits
        user["credits"] = max(0, current_credits - REQUIRED_CREDITS)
        save_user(uid)

        # Build results text
        results_text = (
            "📱 𝗡𝘂𝗺𝗯𝗲𝗿 𝗜𝗻𝗳𝗼 𝗥𝗲𝘀𝘂𝗹𝘁𝘀\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ 𝗦𝗵𝗼𝘄𝗶𝗻𝗴 {len(data)} 𝗼𝗳 {len(data)} 𝗿𝗲𝘀𝘂𝗹𝘁(𝘀) 𝗳𝗼𝘂𝗻𝗱\n\n"
        )

        data = resp.json().get("data", [])


        for i, entry in enumerate(data, start=1):
            address_clean = str(entry.get('address', '-') or '-').replace("!", " ").strip()
            results_text += (
                f"🔸 𝗥𝗲𝘀𝘂𝗹𝘁 {i}:\n"
                f"📱 𝗠𝗼𝗯𝗶𝗹𝗲: {entry.get('mobile', '-')}\n"
                f"👤 𝗡𝗮𝗺𝗲: {entry.get('name', '-')}\n"
                f"👨‍👦 𝗙𝗮𝘁𝗵𝗲𝗿: {entry.get('fname', '-')}\n"
                f"🏠 𝗔𝗱𝗱𝗿𝗲𝘀𝘀: {address_clean}\n"
                f"📞 𝗔𝗹𝘁: {entry.get('alt', '-')}\n"
                f"🌐 𝗖𝗶𝗿𝗰𝗹𝗲: {entry.get('circle', '-')}\n"
                f"🆔 𝗜𝗗: {entry.get('id', '-')}\n"
                f"📧 𝗘𝗺𝗮𝗶𝗹: {entry.get('email', '-')}\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            )

        results_text += (
            f"🔍 𝗖𝗬𝗕𝗘𝗥 𝗜𝗡𝗙𝗢𝗢 𝗢𝗦𝗜𝗡𝗧 | ✅ 𝗦𝘂𝗰𝗰𝗲𝘀𝘀\n\n"
            f"💰 Credits Used: {REQUIRED_CREDITS}\n"
            f"💰 Remaining Credits: {user['credits']}"
        )

        keyboard = [[InlineKeyboardButton("🔙 𝑩𝒂𝒄𝒌", callback_data="main_menu")]]

        # Step 2: Edit searching message to results
        await searching_msg.edit_text(
            results_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    except requests.RequestException:
        await searching_msg.edit_text("⚠️ 𝐔𝐧𝐚𝐛𝐥𝐞 𝐭𝐨 𝐜𝐨𝐧𝐧𝐞𝐜𝐭 𝐭𝐨 𝐬𝐞𝐫𝐯𝐞𝐫.\n\n⏳ 𝑷𝒍𝒆𝒂𝒔𝒆 𝒕𝒓𝒚 𝒂𝒈𝒂𝒊𝒏 𝒍𝒂𝒕𝒆𝒓.")
    
    except ValueError:
        await searching_msg.edit_text("⚠️ 𝑰𝒏𝒗𝒂𝒍𝒊𝒅 𝒓𝒆𝒔𝒑𝒐𝒏𝒔𝒆 𝒓𝒆𝒄𝒆𝒊𝒗𝒆𝒅.\n\n📱 𝑷𝒍𝒆𝒂𝒔𝒆 𝒕𝒓𝒚 𝒘𝒊𝒕𝒉 𝒂 𝒅𝒊𝒇𝒇𝒆𝒓𝒆𝒏𝒕 𝐁𝐈𝐍.")
    
    except Exception:
        await searching_msg.edit_text("⚠️ 𝑵𝒐 𝒅𝒆𝒕𝒂𝒊𝒍𝒔 𝒇𝒐𝒖𝒏𝒅 𝒇𝒐𝒓 𝐭𝐡𝐢𝐬 𝑵𝑼𝑴𝑩𝑬𝑹.\n\n🔁 𝑷𝒍𝒆𝒂𝒔𝒆 𝒅𝒐𝒖𝒃𝒍𝒆-𝒄𝒉𝒆𝒄𝒌 𝒂𝒏𝒅 𝒕𝒓𝒚 𝒂𝒈𝒂𝒊𝒏.")






# import asyncio
# import requests
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import ContextTypes
# from config import API_URL, SUPPORT_CONTACT
# from modules.user import get_user, save_user, is_banned
# from modules.protected import is_protected

# REQUIRED_CREDITS = 1  # credits per number search

# # --------------------
# # Unicode helpers
# # --------------------
# def to_math_bold(s: str) -> str:
#     """Map ASCII letters & digits to Mathematical Bold Unicode where available."""
#     out = []
#     for ch in s:
#         if 'A' <= ch <= 'Z':
#             out.append(chr(0x1D400 + (ord(ch) - ord('A'))))
#         elif 'a' <= ch <= 'z':
#             out.append(chr(0x1D41A + (ord(ch) - ord('a'))))
#         elif '0' <= ch <= '9':
#             out.append(chr(0x1D7CE + (ord(ch) - ord('0'))))
#         else:
#             out.append(ch)
#     return ''.join(out)


# def to_math_italic(s: str) -> str:
#     """Map ASCII letters to Mathematical Italic (leaves digits & others unchanged)."""
#     out = []
#     for ch in s:
#         if 'A' <= ch <= 'Z':
#             out.append(chr(0x1D434 + (ord(ch) - ord('A'))))
#         elif 'a' <= ch <= 'z':
#             out.append(chr(0x1D44E + (ord(ch) - ord('a'))))
#         else:
#             out.append(ch)
#     return ''.join(out)


# def safe_fmt(value):
#     """Return a safe string for display (fallback '-' for empty/None)."""
#     if value is None:
#         return '-'
#     v = str(value).strip()
#     return v if v else '-'


# # --------------------
# # Bot handlers
# # --------------------
# async def num_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Runs when /num OR 'Search' button is clicked"""
#     uid = str(update.effective_user.id)

#     if is_banned(uid):
#         return await update.message.reply_text("🚫 You are banned from using this bot.")

#     # /num <number>
#     if update.message and context.args:
#         return await process_number(update, context, context.args[0].strip())

#     # /num (without args) or button
#     text = (
#         "📱 𝗡𝗨𝗠𝗕𝗘𝗥 𝗜𝗡𝗙𝗢 𝗦𝗘𝗥𝗩𝗜𝗖𝗘 📱\n\n"
#         "📞 Please send the phone number you want to search.\n\n"
#         f"📝 Format: <code>10-digit mobile number</code>\n"
#         f"💰 Cost: {REQUIRED_CREDITS} Credit\n\n"
#         "👉 Example: <code>/num 6351516535</code>"
#     )

#     keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="main_menu")]]

#     if update.callback_query:
#         query = update.callback_query
#         await query.answer()
#         await query.edit_message_text(
#             text,
#             reply_markup=InlineKeyboardMarkup(keyboard),
#             parse_mode="HTML",
#         )
#     else:
#         await update.message.reply_text(
#             text,
#             reply_markup=InlineKeyboardMarkup(keyboard),
#             parse_mode="HTML",
#         )

#     context.user_data["waiting_for_number"] = True


# async def number_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Handles free-text input after /num"""
#     if context.user_data.get("waiting_for_number"):
#         context.user_data["waiting_for_number"] = False
#         number = update.message.text.strip()
#         return await process_number(update, context, number)


# async def process_number(update: Update, context: ContextTypes.DEFAULT_TYPE, number: str):
#     uid = str(update.effective_user.id)
#     user = get_user(uid)

#     if is_banned(uid):
#         return await update.message.reply_text("🚫 You are banned from using this bot.")

#     if is_protected(number):
#         return await update.message.reply_text(
#             f"🔏 Number {number} is **Protected**.\n❌ No information available."
#         )

#     current_credits = user.get("credits", 0)
#     if current_credits < REQUIRED_CREDITS:
#         keyboard = [
#             [InlineKeyboardButton("📞 Contact Admin", url=SUPPORT_CONTACT)],
#             [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
#         ]
#         return await update.message.reply_text(
#             f"❌ Insufficient Credits!\n\n"
#             f"You need {REQUIRED_CREDITS} credits for Number Info service.\n"
#             f"Your balance: {current_credits}\n\n"
#             "💰 Use /start to buy more credits.",
#             reply_markup=InlineKeyboardMarkup(keyboard),
#         )

#     # Step 1: Send initial searching message (we'll animate it)
#     searching_msg = await update.message.reply_text("⏳ Preparing search...")

#     url = f"{API_URL}{number}"

#     # Spinner task (animated "ball" / spinner)
#     async def _spinner(msg, stop_event: asyncio.Event):
#         spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
#         idx = 0
#         try:
#             while not stop_event.is_set():
#                 text = f"🔎 {to_math_italic('Searching')} {spinner[idx % len(spinner)]}  {to_math_italic('please wait')}"
#                 # attempt to edit; ignore errors (rate limits or message deleted)
#                 try:
#                     await msg.edit_text(text)
#                 except Exception:
#                     pass
#                 idx += 1
#                 await asyncio.sleep(0.35)
#         except asyncio.CancelledError:
#             return

#     stop_evt = asyncio.Event()
#     spinner_task = asyncio.create_task(_spinner(searching_msg, stop_evt))

#     try:
#         # Run blocking requests.get in thread so spinner can animate
#         resp = await asyncio.to_thread(requests.get, url, {"timeout": 30})
#         # If we used the dict accidentally above (requests.get(url, {"timeout":30})), ensure correct signature:
#         # But Python's requests.get accepts timeout as keyword arg, so fix:
#     except TypeError:
#         # fallback in case above to_thread call passed dict incorrectly; call properly
#         try:
#             resp = await asyncio.to_thread(requests.get, url, timeout=30)
#         except Exception as e:
#             stop_evt.set()
#             await spinner_task
#             return await searching_msg.edit_text("⚠️ Unable to connect to server.\n\n⏳ Please try again later.")
#     except requests.RequestException:
#         stop_evt.set()
#         await spinner_task
#         return await searching_msg.edit_text("⚠️ Unable to connect to server.\n\n⏳ Please try again later.")
#     except Exception:
#         stop_evt.set()
#         await spinner_task
#         return await searching_msg.edit_text("⚠️ Unable to connect to server.\n\n⏳ Please try again later.")

#     # Got a response (stop spinner while we parse)
#     stop_evt.set()
#     await spinner_task  # wait spinner to finish cleanly

#     try:
#         resp.raise_for_status()
#         data = resp.json()
#     except requests.RequestException:
#         return await searching_msg.edit_text("⚠️ Server returned an error.\n\n⏳ Please try again later.")
#     except ValueError:
#         return await searching_msg.edit_text("⚠️ Invalid response received.\n\n📱 Please try with a different number.")

#     # Normalize results: API sometimes returns dict with "data" list
#     if isinstance(data, dict):
#         results = data.get("data", [])
#     elif isinstance(data, list):
#         results = data
#     else:
#         results = []

#     if not results:
#         return await searching_msg.edit_text("❌ No data found for this number.\n\n🔁 Please double-check and try again.")

#     # Deduct credits (save after successful retrieval)
#     user["credits"] = max(0, current_credits - REQUIRED_CREDITS)
#     save_user(uid)

#     # Build results text with Unicode math fonts
#     header = to_math_bold("NUMBER INFO RESULTS")
#     sub = to_math_italic(f"Showing {len(results)} result(s)")

#     results_text = []
#     results_text.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
#     results_text.append(f"🔍 {header}")
#     results_text.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
#     results_text.append(sub)
#     results_text.append("")

#     for i, entry in enumerate(results, start=1):
#         name = safe_fmt(entry.get("name"))
#         father = safe_fmt(entry.get("fname"))
#         mobile = safe_fmt(entry.get("mobile"))
#         alt = safe_fmt(entry.get("alt"))
#         cid = safe_fmt(entry.get("id"))
#         circle = safe_fmt(entry.get("circle"))
#         email = safe_fmt(entry.get("email"))
#         address_raw = safe_fmt(entry.get("address"))
#         # cleanup address: replace '!' with space, collapse whitespace
#         address_clean = " ".join(address_raw.replace("!", " ").split())
#         address_clean = address_clean if address_clean != "" else "-"

#         block = (
#             f"✦ {to_math_bold('Result')} ⟮{to_math_bold(str(i))}⟯\n"
#             f"{to_math_italic('Name')}: {to_math_bold(name)}\n"
#             f"{to_math_italic('Father')}: {to_math_bold(father)}\n"
#             f"{to_math_italic('Mobile')}: {to_math_bold(mobile)}\n"
#             f"{to_math_italic('Alt')}: {to_math_bold(alt)}\n"
#             f"{to_math_italic('Circle')}: {to_math_bold(circle)}\n"
#             f"{to_math_italic('ID')}: {to_math_bold(cid)}\n"
#             f"{to_math_italic('Email')}: {to_math_bold(email)}\n"
#             f"{to_math_italic('Address')}: {address_clean}\n"
#             "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
#         )
#         results_text.append(block)

#     footer = (
#         f"{to_math_italic('CYBER INFOO OSINT')}  |  {to_math_bold('Success')}\n\n"
#         f"{to_math_italic('Credits Used')}: {to_math_bold(str(REQUIRED_CREDITS))}\n"
#         f"{to_math_italic('Remaining')}: {to_math_bold(str(user['credits']))}"
#     )

#     results_text.append(footer)

#     final_text = "\n".join(results_text)

#     # Telegram message length limit safety (keep some margin)
#     MAX_LEN = 4000
#     if len(final_text) > MAX_LEN:
#         final_text = final_text[: MAX_LEN - 120]
#         final_text += "\n\n… (output truncated)"

#     keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="main_menu")]]

#     # Final edit: show results (no parse_mode to avoid accidental markup)
#     await searching_msg.edit_text(final_text, reply_markup=InlineKeyboardMarkup(keyboard))
