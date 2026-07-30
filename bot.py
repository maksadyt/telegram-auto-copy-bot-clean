from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
)

from config import BOT_TOKEN
from handlers import (
    start,
    addpair,
    listpairs,
    removepair,
    startforwarding,
    stopforwarding,
    message_handler,
)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addpair", addpair))
    app.add_handler(CommandHandler("listpairs", listpairs))
    app.add_handler(CommandHandler("removepair", removepair))
    app.add_handler(CommandHandler("startforwarding", startforwarding))
    app.add_handler(CommandHandler("stopforwarding", stopforwarding))

    app.add_handler(message_handler)

    print("Bot Started...")

    app.run_polling()

if __name__ == "__main__":
    main()
