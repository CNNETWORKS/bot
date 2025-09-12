from telegram import Update
from telegram.ext import ContextTypes

ADMINS = [6321361862, 7850839661]  # List of admin user IDs


async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message.text

    for admin_id in ADMINS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=(
                    "📩 𝑵𝒆𝒘 𝑴𝒆𝒔𝒔𝒂𝒈𝒆 𝒇𝒓𝒐𝒎 𝑼𝒔𝒆𝒓\n\n"
                    f"👤 𝑵𝒂𝒎𝒆: {user.first_name} {user.last_name or ''}\n"
                    f"🆔 𝑰𝑫: `{user.id}`\n"
                    f"🔗 𝑷𝒓𝒐𝒇𝒊𝒍𝒆: [𝑶𝒑𝒆𝒏 𝑼𝒔𝒆𝒓](tg://user?id={user.id})\n\n"
                    f"💬 𝑴𝒆𝒔𝒔𝒂𝒈𝒆:\n『{message}』"
                ),
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Failed to forward to {admin_id}: {e}")
