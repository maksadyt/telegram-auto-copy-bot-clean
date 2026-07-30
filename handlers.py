from telegram import Update
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)

from config import ADMIN_USER_IDS
from database import (
    add_pair,
    remove_pair,
    get_pairs,
    forwarding_enabled,
    set_forwarding,
)


def is_admin(user_id):
    return str(user_id) in ADMIN_USER_IDS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Auto Copy Bot\n\n"
        "Commands:\n"
        "/addpair <source_id> <destination_id>\n"
        "/listpairs\n"
        "/removepair <pair_id>\n"
        "/startforwarding\n"
        "/stopforwarding"
    )


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


async def listpairs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    pairs = get_pairs()

    if not pairs:
        await update.message.reply_text("No pairs found.")
        return

    text = ""

    for pair in pairs:
        pair_id, source, destination = pair
        text += (
            f"ID: {pair_id}\n"
            f"Source: {source}\n"
            f"Destination: {destination}\n\n"
        )

    await update.message.reply_text(text)


async def removepair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if len(context.args) != 1:
        await update.message.reply_text(
            "Usage:\n/removepair <pair_id>"
        )
        return

    try:
        pair_id = int(context.args[0])

        remove_pair(pair_id)

        await update.message.reply_text(
            "✅ Pair removed successfully."
        )

    except Exception as e:
        await update.message.reply_text(str(e))


async def startforwarding(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    set_forwarding("on")

    await update.message.reply_text(
        "✅ Forwarding Started."
    )


async def stopforwarding(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    set_forwarding("off")

    await update.message.reply_text(
        "🛑 Forwarding Stopped."
    )
async def copy_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not forwarding_enabled():
        return

    if update.channel_post is None:
        return

    chat_id = update.channel_post.chat_id

    pairs = get_pairs()

    for pair in pairs:
        pair_id, source, destination = pair

        if source == chat_id:
            try:
                await context.bot.copy_message(
                    chat_id=destination,
                    from_chat_id=source,
                    message_id=update.channel_post.message_id,
                )
            except Exception as e:
                print(e)


message_handler = MessageHandler(
    filters.ALL & filters.ChatType.CHANNEL,
    copy_messages,
    )
