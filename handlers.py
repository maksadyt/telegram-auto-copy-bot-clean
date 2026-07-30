from telegram import Update
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)

from config import ADMIN_IDS
from database import (
    add_pair,
    get_pairs,
    remove_pair,
    forwarding_enabled,
    set_forwarding,
)


def is_admin(user_id):
    return user_id in ADMIN_IDS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ You are not authorized.")
        return

    text = (
        "✅ Auto Copy Bot\n\n"
        "/addpair <source_id> <destination_id>\n"
        "/listpairs\n"
        "/removepair <pair_id>\n"
        "/startforwarding\n"
        "/stopforwarding"
    )

    await update.message.reply_text(text)


async def addpair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if len(context.args) != 2:
        await update.message.reply_text(
            "Usage:\n/addpair <source_chat_id> <destination_chat_id>"
        )
        return

    try:
        source = int(context.args[0])
        destination = int(context.args[1])

        add_pair(source, destination)

        await update.message.reply_text(
            "✅ Pair added successfully."
        )

    except Exception as e:
        await update.message.reply_text(str(e))
