import hashlib
import logging
import os
import re
from functools import reduce
from typing import Callable

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Updater
from telegram.ext.filters import Filters
from telegram.ext.inlinequeryhandler import InlineQueryHandler

import pymocklib
import bot

token = os.environ.get("MOCK_BOT_TOKEN")
bot_name = os.environ.get("MOCK_BOT_NAME", "mockerell")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def help_command(update: Update, context: CallbackContext):
    """
    Composes the response to the /help and /start commands of the bot
    """
    help_lines = [
        f"*Mockerell Bot {bot.__version__}*",
        "A Telegram bot that lets you express your true feelings",
        "Developed by @zoomoid at https://github.com/zoomoid/mockerell"
        "Inspired by Nicolas Lenz' work (https://git.eisfunke.com/software/mock-bot-telegram)",
        "",
        f"*Inline usage:* Just type `@{bot_name}` and the text you want to stylize in any chat. Telegram will show you a selection of the styles available.",
        "",
        "*Usage:* \\[STYLE] \\[TEXT]",
        "*Example:* `random Cool Text`",
        "",
        "Multiple styles can be concatenated with '|'s.",
        "*Example:* `random|double Cool Text`",
        "",
        "*Available Styles:*",
    ] + [f"  *{name}*: {pymocklib.style_doc(name)}" for (name, _) in pymocklib.styles]
    update.message.reply_text("\n".join(help_lines), parse_mode=ParseMode.MARKDOWN)


def reply_to_inline(update: Update, context: CallbackContext):
    """
    Replies to inline querys, i.e., "@bot_name text" with results for all available styles and
    a preview of how each style is going to look with the provided text
    """
    query = update.inline_query.query
    if not query:
        return
    results = [
        InlineQueryResultArticle(
            id=hashlib.sha256(f"{name}{query}".encode("utf-8")).hexdigest(),
            title=name,
            description=f(query),
            input_message_content=InputTextMessageContent(message_text=f(query)),
        )
        for (name, f) in pymocklib.styles
    ]
    context.bot.answer_inline_query(update.inline_query.id, results)


def reply(update: Update, context: CallbackContext):
    """
    Replies to any message with a valid command+text combo, i.e., when a user
    requests a style, e.g. "random" and any text followed by that.

    Commands can be composed using "|" from all the available styles
    """
    message = update.message.text
    words = message.split()
    command = words.pop(0)
    style_names = re.sub("^/", "", command).split("@")[0].lower().split("|")
    words = " ".join(words)
    funcs = [f for (name, f) in pymocklib.styles if name in style_names]
    if not funcs:
        msg = "Invalid mocking."
        if update.effective_chat.type == "private":
            msg += " See /help"
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=msg,
            reply_to_message_id=update.message.message_id,
        )
        return

    def apply(p: str, f: Callable[[str], str]) -> str:
        """
        somewhat functional way of composing the transformer functions onto a base string
        """
        return f(p)

    msg = reduce(apply, funcs, words)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg,
        reply_to_message_id=update.message.message_id,
    )


def main() -> None:
    bot = Updater(token=token, use_context=True)
    dispatcher = bot.dispatcher

    help_handler = CommandHandler("help", help_command)
    start_handler = CommandHandler("start", help_command)
    inline_handler = InlineQueryHandler(reply_to_inline)
    reply_handler = MessageHandler(Filters.text & (~Filters.command), reply)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(inline_handler)
    dispatcher.add_handler(reply_handler)

    bot.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    bot.idle()


if __name__ == "__main__":
    main()
