import os


# ⚠️ IMPORTANT: For production, use environment variables.
# These defaults are here so the sample runs out-of-the-box, but you should replace them.
BOT_TOKEN = os.getenv("BOT_TOKEN", "8343147024:AAEAFM8id0lJiwCCq6tjMyh10doViHRaVV8")
# API_KEY = os.getenv("API_KEY", "MK103020070811")
# API_URL = os.getenv("API_URL", "https://xwalletbot.shop/number.php")
API_KEY = os.getenv("API_KEY", "FROZEN")
API_URL = os.getenv("API_URL", "http://blackhatfrozen.store/lodalelobaby/api.php")

# API_URL = os.getenv("API_URL", "https://api-learnonix.onrender.com/numbers/")

# Channels users must join before using bot
FORCE_CHANNELS = os.getenv("FORCE_CHANNELS", "@cnnetworkofficial,@Babysojao").split(",")

# Admin chat IDs (comma-separated). Example: "12345,67890"
ADMINS = {int(x) for x in os.getenv("ADMINS", "7271198694,8406861406").split(",") if x.strip()}

# Data files
DATA_DIR = os.getenv("DATA_DIR", "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
REDEEMS_FILE = os.path.join(DATA_DIR, "redeems.json")

# UPI / Payment config (edit these as needed)
UPI_ID = os.getenv("UPI_ID", "name@upi")
PAYMENT_INSTRUCTIONS = os.getenv(
    "PAYMENT_INSTRUCTIONS",
    "Send payment to the UPI ID above, then tap 'Send Payment Proof' in the bot and upload the screenshot with your Telegram @username in the caption."
)
SUPPORT_CONTACT = os.getenv("SUPPORT_CONTACT", "https://t.me/jioxt")
