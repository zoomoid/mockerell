import hashlib
import logging
import os
import re
from functools import reduce
from typing import Callable
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    InlineQueryHandler,
    MessageHandler,
    filters,
)

import pymocklib
import bot

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

token = os.environ.get("MOCK_BOT_TOKEN")
if not token:
    logging.error("MOCK_BOT_TOKEN is required")
    exit(1)

HELP_MESSAGE = f"""
*Mockerell Bot {bot.__version__}*
A Telegram bot that lets you express your true feelings
Developed by @zoomoid at https://github.com/zoomoid/mockerell
Inspired by Nicolas Lenz' work (https://git.eisfunke.com/software/mock-bot-telegram)

*Inline usage:* Just type `@mockerellbot` and the text you want to stylize in any chat.
Telegram will show you a selection of the styles available.

*Usage:* \\[STYLE] \\[TEXT]
*Example:* `random Cool Text`

Multiple styles can be concatenated with '|'s.
*Example:* `random|double Cool Text`

*Available Styles:*
""" + "\n".join(
    [f"  *{name}*: {pymocklib.style_doc(name)}" for (name, _) in pymocklib.styles]
)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Composes the response to the /help and /start commands of the bot
    """
    if not update.message:
        return

    await update.message.reply_text(HELP_MESSAGE, parse_mode=ParseMode.MARKDOWN)


async def reply_to_inline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Replies to inline querys, i.e., "@bot_name text" with results for all available styles and
    a preview of how each style is going to look with the provided text
    """
    if not update.inline_query:
        return

    query = update.inline_query.query

    if not query:
        return

    regional_indicator_code_points = list(query.strip()[0:2].encode("unicode-escape").decode("ascii").split("\\U"))[1:]

    flag_intersperse_funcs = []

    if len(regional_indicator_code_points) == 2 and all(
        [c >= int("0x1F1E6", 16) and c <= int("0x1F1FF", 16)
        for c in [int(i, 16) for i in regional_indicator_code_points]]
    ):
        # flag emojis are composed of two regional indicators from inbetween U+1F1E6 and U+1F1FF
        # convert flag back to characters
        flag = "".join([chr(int(cp, 16)) for cp in regional_indicator_code_points])
        flag_intersperse_funcs = [(flag * 3, pymocklib.to_interspersed_flag(flag))]
        # chop the flag from the query
        query = query[2:]

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=name,
            description=f(query),
            input_message_content=InputTextMessageContent(f(query)),
        )
        for (name, f) in pymocklib.styles + flag_intersperse_funcs
    ]

    await update.inline_query.answer(results)


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Replies to any message with a valid command+text combo, i.e., when a user
    requests a style, e.g. "random" and any text followed by that.

    Commands can be composed using "|" from all the available styles
    """
    if not update.message:
        return

    if not update.message.text:
        return

    message = update.message.text
    words = message.split()
    command = words.pop(0)
    style_names = re.sub("^/", "", command).split("@")[0].lower().split("|")
    words = " ".join(words)
    funcs = [f for (name, f) in pymocklib.styles if name in style_names]
    if not funcs:
        msg = "Invalid mocking."
        if update.effective_chat and update.effective_chat.type == "private":
            msg += " See /help"
        await update.message.reply_text(msg)

        return

    def apply(p: str, f: Callable[[str], str]) -> str:
        """
        somewhat functional way of composing the transformer functions onto a base string
        """
        return f(p)

    msg = reduce(apply, funcs, words)
    await update.message.reply_text(msg)


def main() -> None:
    application = Application.builder().token(str(token)).build()

    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("start", help_command))
    application.add_handler(InlineQueryHandler(reply_to_inline))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply))

    application.run_polling()


if __name__ == "__main__":
    main()
