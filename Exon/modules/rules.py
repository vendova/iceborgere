"""
MIT License

Copyright (c) 2022 ABISHNOI69

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1m
#     UPDATE   :- Abishnoi_bots
#     GITHUB :- ABISHNOI69 ""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, Filters
from telegram.utils.helpers import escape_markdown

import Exon.modules.sql.rules_sql as sql
from Exon import dispatcher
from Exon.modules.helper_funcs.anonymous import AdminPerms, user_admin
from Exon.modules.helper_funcs.decorators import Exoncmd
from Exon.modules.helper_funcs.string_handling import markdown_parser


@Exoncmd(command="rules", filters=Filters.chat_type.groups)
def get_rules(update: Update, _: CallbackContext):
    chat_id = update.effective_chat.id
    send_rules(update, chat_id)


# Do not async - not from a handler
def send_rules(update, chat_id, from_pm=False):
    bot = dispatcher.bot
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message
    reply_msg = update.message.reply_to_message
    try:
        chat = bot.get_chat(chat_id)
    except BadRequest as excp:
        if excp.message == "Chat not found" and from_pm:
            bot.send_message(
                user.id,
                "THE RULES SHoRTcUT FoR THIS cHAT HASN'T BEEN SET PRoPERLY! ASK ADMINS To "
                "FIx THIS.\nMAY BE THEY FoRGoT THE HYPHEN IN ID",
            )
            return
        raise

    rules = sql.get_rules(chat_id)
    text = f"THE RULES FoR *{escape_markdown(chat.title)}* ARE:\n\n{rules}"

    if from_pm and rules:
        bot.send_message(
            user.id,
            text,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    elif from_pm:
        bot.send_message(
            user.id,
            "THE GRoUP ADMINS HAvEN'T SET ANY RULES FoR THIS cHAT YET. "
            "THIS PRoBEBLY DoES'T MEAN IT'S LAWLESS THoUGH...!",
        )
    elif rules and reply_msg:
        reply_msg.reply_text(
            "PLEASE cLIcK THE BUTToN BELoW To SEE THE RULES.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="📝 READ RULES",
                            url=f"t.me/{bot.username}?start={chat_id}",
                        ),
                        InlineKeyboardButton(text="❌ DELETE", callback_data="close2"),
                    ]
                ]
            ),
        )
    elif rules:
        btn = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="📝 READ RULES",
                        url=f"t.me/{bot.username}?start={chat_id}",
                    ),
                    InlineKeyboardButton(text="❌ DELETE", callback_data="close2"),
                ]
            ]
        )
        txt = "Please click the button below to see the rules."
        if not message.reply_to_message:
            message.reply_text(txt, reply_markup=btn)

        if message.reply_to_message:
            message.reply_to_message.reply_text(txt, reply_markup=btn)
    else:
        update.effective_message.reply_text(
            "THE GRoUP ADMINS HAvEN'T SET ANY RULES FoR THIS cHAT YET. "
            "THIS PRoBABLY DoES'T MEAN ITS LAWLESS THoUGH...!",
        )


close_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("❌ DELETE", callback_data="close2")]]
)


@Exoncmd(command="setrules", filters=Filters.chat_type.groups)
@user_admin(AdminPerms.CAN_CHANGE_INFO)
def set_rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    msg = update.effective_message  # type: Optional[Message]
    raw_text = msg.text
    args = raw_text.split(None, 1)  # use python's maxsplit to separate cmd and args
    if len(args) == 2:
        txt = args[1]
        offset = len(txt) - len(raw_text)  # set correct offset relative to command
        markdown_rules = markdown_parser(
            txt,
            entities=msg.parse_entities(),
            offset=offset,
        )

        sql.set_rules(chat_id, markdown_rules)
        update.effective_message.reply_text("SUcESSFULLY SET RULES FoR THIS GRoUP.")


@Exoncmd(command="clearrules", filters=Filters.chat_type.groups)
@user_admin(AdminPerms.CAN_CHANGE_INFO)
def clear_rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    sql.set_rules(chat_id, "")
    update.effective_message.reply_text("SUccESSFULLY cLEARED RULES!")


def __stats__():
    return f"x {sql.num_chats()} chats have rules set."


def __import_data__(chat_id, data):
    # set chat rules
    rules = data.get("info", {}).get("rules", "")
    sql.set_rules(chat_id, rules)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    return f"This chat has had it's rules set: `{bool(sql.get_rules(chat_id))}`"


__mod_name__ = "Rules"


# foR HELP MENU


# """
from Exon.modules.language import gs


def get_help(chat):
    return gs(chat, "rules_help")


# """
