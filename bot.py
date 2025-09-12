import logging
import os
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ConversationHandler, ContextTypes, filters
)

from config import BOT_TOKEN
from modules.menu import start, joined_callback, account_callback, back_to_menu
from modules.redeem import (
    redeem_create, redeem_list,
    redeem_start, redeem_process, redeem_cancel, WAITING_CODE
)
from modules.admin import addcredit, ban, unban, total, broadcast, maintenance
from modules.help import help_command
from modules.utils import ensure_data_folder
from modules.plans import plans_callback
from buttons.refer import refer_callback
from buttons.adhar import adhar_info
from buttons.instagram import insta_callback
from buttons.vehicle import vehicle_callback, vehicle_handler
from buttons.upiinfo import upi_callback, upi_handler
from buttons.aboutbot import guide_message
from buttons.fampay import fampay_callback, fampay_handler
from buttons.breachdata import breach_callback, breach_handler
from buttons.bininfo import bin_command, process_bin
from buttons.search import  num_command
from buttons.protectnumber import (
    protectnumber_callback, protect_command,
    unprotect_command, list_protected_command
)
from handlers.conversation import forward_to_admin



# ===== Logging =====
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    ensure_data_folder()

    application = Application.builder().token(BOT_TOKEN).build()

    # User commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("num", num_command))
    application.add_handler(CommandHandler("insta", insta_callback))
    application.add_handler(CommandHandler("upiinfo",upi_handler ))
    application.add_handler(CommandHandler("vehicle", vehicle_handler))
    application.add_handler(CommandHandler("fampay", fampay_handler))
    application.add_handler(CommandHandler("breach", breach_handler))
    application.add_handler(CommandHandler("bin", bin_command))

    # Admin commands
    application.add_handler(CommandHandler("redeem", redeem_create))
    application.add_handler(CommandHandler("redeemlist", redeem_list))
    application.add_handler(CommandHandler("addcredit", addcredit))
    application.add_handler(CommandHandler("ban", ban))
    application.add_handler(CommandHandler("unban", unban))
    application.add_handler(CommandHandler("total", total))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("maintenance", maintenance))
    application.add_handler(CommandHandler("protect", protect_command))
    application.add_handler(CommandHandler("unprotect", unprotect_command))
    application.add_handler(CommandHandler("listprotected", list_protected_command))

    # Callback buttons
    application.add_handler(CallbackQueryHandler(joined_callback, pattern="^joined$"))
    application.add_handler(CallbackQueryHandler(num_command, pattern="^search$"))
    application.add_handler(CallbackQueryHandler(account_callback, pattern="^account$"))
    application.add_handler(CallbackQueryHandler(upi_callback, pattern="^upiinfo$"))
    application.add_handler(CallbackQueryHandler(plans_callback, pattern="^plans$"))
    application.add_handler(CallbackQueryHandler(back_to_menu, pattern="^main_menu$"))
    application.add_handler(CallbackQueryHandler(refer_callback, pattern="^refer$"))
    application.add_handler(CallbackQueryHandler(adhar_info, pattern="^adhar$"))
    application.add_handler(CallbackQueryHandler(insta_callback, pattern="^insta$"))
    application.add_handler(CallbackQueryHandler(vehicle_callback, pattern="^vehicle$"))
    application.add_handler(CallbackQueryHandler(guide_message, pattern="^about$"))
    application.add_handler(CallbackQueryHandler(protectnumber_callback, pattern="^protectnumber$"))
    application.add_handler(CallbackQueryHandler(fampay_callback, pattern="^fampay$"))
    application.add_handler(CallbackQueryHandler(breach_callback, pattern="^breach$"))
    application.add_handler(CallbackQueryHandler(help_command, pattern="^help$"))
    application.add_handler(CallbackQueryHandler(bin_command, pattern="^bininfo$"))


    # Redeem conversation: allow both /free and inline menu button (pattern '^redeem$') to start
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("free", redeem_start),
            CallbackQueryHandler(redeem_start, pattern="^redeem$")   # when user presses Redeem button in menu
        ],
        states={
            WAITING_CODE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, redeem_process)
            ]
        },
        fallbacks=[CommandHandler("cancel", redeem_cancel)],
        allow_reentry=True
    )
    application.add_handler(conv_handler)


    # Catch-all message handler (forward user messages to admins)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))


    logger.info("Bot starting...")
    application.run_polling(allowed_updates=["message", "callback_query"])



if __name__ == "__main__":
    main()
