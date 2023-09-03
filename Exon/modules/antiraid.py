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
import html
from datetime import timedelta
from typing import Optional

from pytimeparse.timeparse import timeparse
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext
from telegram.utils.helpers import mention_html

import Exon.modules.sql.welcome_sql as sql
from Exon import LOGGER as log
from Exon.modules.cron_jobs import j
from Exon.modules.helper_funcs.anonymous import AdminPerms
from Exon.modules.helper_funcs.anonymous import resolve_user as res_user
from Exon.modules.helper_funcs.anonymous import user_admin as u_admin
from Exon.modules.helper_funcs.chat_status import connection_status, user_admin_no_reply
from Exon.modules.helper_funcs.decorators import Exoncallback, Exoncmd
from Exon.modules.log_channel import loggable


def get_time(time: str) -> int:
    try:
        return timeparse(time)
    except:
        return 0


def get_readable_time(time: int) -> str:
    t = f"{timedelta(seconds=time)}".split(":")
    if time == 86400:
        return "1 day"
    return "{} HoUR(s)".format(t[0]) if time >= 3600 else "{} MINUTEs".format(t[1])


@Exoncmd(command="raid", pass_args=True)
@connection_status
@loggable
@u_admin(AdminPerms.CAN_CHANGE_INFO)
def setRaid(update: Update, context: CallbackContext) -> Optional[str]:
    args = context.args
    chat = update.effective_chat
    msg = update.effective_message
    u = update.effective_user
    user = res_user(u, msg.message_id, chat)
    if chat.type == "private":
        context.bot.sendMessage(chat.id, "THIs coMMAND Is NoT AvAILABLE IN PMs.")
        return
    stat, time, acttime = sql.getDefenseStatus(chat.id)
    readable_time = get_readable_time(time)
    if len(args) == 0:
        if stat:
            text = "RAID MoDE Is cURRENTLY <code>ENABLED</code>\nWoULD YoU LIKE To <code>DIsABLE</code> RAID?"
            keyboard = [
                [
                    InlineKeyboardButton(
                        "DIsABLE RAID",
                        callback_data="disable_raid={}={}".format(chat.id, time),
                    ),
                    InlineKeyboardButton("cANcEL", callback_data="cancel_raid=1"),
                ]
            ]
        else:
            text = f"RAID MoDE Is cURRENTLY <code>DIsABLED</code>\nWoULD YoU LIKE To <code>ENABLE</code> RAID foR {readable_time}?"
            keyboard = [
                [
                    InlineKeyboardButton(
                        "ENABLE RAID",
                        callback_data="enable_raid={}={}".format(chat.id, time),
                    ),
                    InlineKeyboardButton("cANcEL", callback_data="cancel_raid=0"),
                ]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)

    elif args[0] == "off":
        if stat:
            sql.setDefenseStatus(chat.id, False, time, acttime)
            text = "RAID MoDE HAs BEEN <code>DIsABLED</code>, MEMBERs THAT JoIN WILL No LoNGER BE KIcKED."
            msg.reply_text(text, parse_mode=ParseMode.HTML)
            logmsg = (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#RAID\n"
                f"DIsABLED\n"
                f"<b>ADMIN:</b> {mention_html(user.id, user.first_name)}\n"
            )
            return logmsg

    else:
        args_time = args[0].lower()
        time = get_time(args_time)
        if time:
            readable_time = get_readable_time(time)
            if time >= 300 and time < 86400:
                text = f"RAID MoDE Is cURRENTLY <code>DIsABLED</code>\nWoULD YoU LIKE To <code>ENABLE</code> RAID foR {readable_time}?"
                keyboard = [
                    [
                        InlineKeyboardButton(
                            "ENABLE RAID",
                            callback_data="enable_raid={}={}".format(chat.id, time),
                        ),
                        InlineKeyboardButton("cANcEL", callback_data="cancel_raid=0"),
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                msg.reply_text(
                    text, parse_mode=ParseMode.HTML, reply_markup=reply_markup
                )
            else:
                msg.reply_text(
                    "YoU cAN oNLY sET TIME BETWEEN 5 MINUTEs AND 1 DAY",
                    parse_mode=ParseMode.HTML,
                )

        else:
            msg.reply_text(
                "UNKNoWN TIME GIvEN, GIvE ME soMETHING LIKE 5m oR 1h",
                parse_mode=ParseMode.HTML,
            )


@Exoncallback(pattern="enable_raid=")
@connection_status
@user_admin_no_reply
@loggable
def enable_raid_cb(update: Update, _: CallbackContext) -> Optional[str]:
    args = update.callback_query.data.replace("enable_raid=", "").split("=")
    chat = update.effective_chat
    user = update.effective_user
    chat_id = args[0]
    time = int(args[1])
    readable_time = get_readable_time(time)
    _, t, acttime = sql.getDefenseStatus(chat_id)
    sql.setDefenseStatus(chat_id, True, time, acttime)
    update.effective_message.edit_text(
        f"RAID MoDE HAs BEEN <code>ENABLED</code> foR {readable_time}.",
        parse_mode=ParseMode.HTML,
    )
    log.info("ENABLED RAID MoDE IN {} foR {}".format(chat_id, readable_time))

    def disable_raid(_):
        sql.setDefenseStatus(chat_id, False, t, acttime)
        log.info("DIsBLED RAID MoDE IN {}".format(chat_id))
        logmsg = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#RAID\n"
            f"AUToMATIcALLY DIsABLED\n"
        )
        return logmsg

    j.run_once(disable_raid, time)
    logmsg = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#RAID\n"
        f"ENABLBED foR {readable_time}\n"
        f"<b>ADMIN:</b> {mention_html(user.id, user.first_name)}\n"
    )
    return logmsg


@Exoncallback(pattern="disable_raid=")
@connection_status
@user_admin_no_reply
@loggable
def disable_raid_cb(update: Update, _: CallbackContext) -> Optional[str]:
    args = update.callback_query.data.replace("disable_raid=", "").split("=")
    chat = update.effective_chat
    user = update.effective_user
    chat_id = args[0]
    time = args[1]
    _, t, acttime = sql.getDefenseStatus(chat_id)
    sql.setDefenseStatus(chat_id, False, time, acttime)
    update.effective_message.edit_text(
        "RAID MoDE HAs BEEN <code>Disabled</code>, JoINIG MEMBERs WILL No LoNGER BE KIcKED.",
        parse_mode=ParseMode.HTML,
    )
    logmsg = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#RAID\n"
        f"DIsABLED\n"
        f"<b>ADMIN:</b> {mention_html(user.id, user.first_name)}\n"
    )
    return logmsg


@Exoncallback(pattern="cancel_raid=")
@connection_status
@user_admin_no_reply
def disable_raid_cb(update: Update, context: CallbackContext):
    args = update.callback_query.data.split("=")
    what = args[0]
    update.effective_message.edit_text(
        f"AcTIoN cANcELLED, RAID MoDE WILL sTAY <code>{'Enabled' if what ==1 else 'Disabled'}</code>.",
        parse_mode=ParseMode.HTML,
    )


@Exoncmd(command="raidtime")
@connection_status
@loggable
@u_admin(AdminPerms.CAN_CHANGE_INFO)
def raidtime(update: Update, context: CallbackContext) -> Optional[str]:
    what, time, acttime = sql.getDefenseStatus(update.effective_chat.id)
    args = context.args
    msg = update.effective_message
    u = update.effective_user
    chat = update.effective_chat
    user = res_user(u, msg.message_id, chat)
    if not args:
        msg.reply_text(
            f"RAID MoDE Is cURRENTLY sET To {get_readable_time(time)}\nWHEN ToGGLED, THE RAID MoDE WILL LAsT foR {get_readable_time(time)} THEN TURN off AUToMATIcALLY",
            parse_mode=ParseMode.HTML,
        )
        return
    args_time = args[0].lower()
    time = get_time(args_time)
    if time:
        readable_time = get_readable_time(time)
        if time >= 300 and time < 86400:
            text = f"RAID MoDE Is cURRENTLY sET To {readable_time}\nWHEN ToGGLED, THE RAID MoDE WILL LAsT foR {readable_time} THEN TURN off AUToMATIcALLY"
            msg.reply_text(text, parse_mode=ParseMode.HTML)
            sql.setDefenseStatus(chat.id, what, time, acttime)
            logmsg = (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#RAID\n"
                f"sET RAID MoDE TIME To {readable_time}\n"
                f"<b>ADMIN:</b> {mention_html(user.id, user.first_name)}\n"
            )
            return logmsg
        else:
            msg.reply_text(
                "YoU cAN oNLY sET TIME BETWEEN 5 MINUTEs AND 1 DAY",
                parse_mode=ParseMode.HTML,
            )
    else:
        msg.reply_text(
            "UNKNoWN TIME GIvEN, give ME soMETHING LIKE 5M oR 1H",
            parse_mode=ParseMode.HTML,
        )


@Exoncmd(command="raidactiontime", pass_args=True)
@connection_status
@u_admin(AdminPerms.CAN_CHANGE_INFO)
@loggable
def raidtime(update: Update, context: CallbackContext) -> Optional[str]:
    what, t, time = sql.getDefenseStatus(update.effective_chat.id)
    args = context.args
    msg = update.effective_message
    u = update.effective_user
    chat = update.effective_chat
    user = res_user(u, msg.message_id, chat)
    if not args:
        msg.reply_text(
            f"RAID AcToIN TIME Is cURRENTLY sET To {get_readable_time(time)}\nWHEN ToGGLED, THE MEMBERs THAT JoIN WILL BE TEMP BANNED foR {get_readable_time(time)}",
            parse_mode=ParseMode.HTML,
        )
        return
    args_time = args[0].lower()
    time = get_time(args_time)
    if time:
        readable_time = get_readable_time(time)
        if time >= 300 and time < 86400:
            text = f"RAID AcToIN TIME Is cURRENTLY sET To {get_readable_time(time)}\nWHEN ToGGLED, THE MEMBERs THAT JoIN WILL BE TEMP BANNED foR {readable_time}"
            msg.reply_text(text, parse_mode=ParseMode.HTML)
            sql.setDefenseStatus(chat.id, what, t, time)
            logmsg = (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#RAID\n"
                f"sET RAID MoDE AcTIoN TIME To {readable_time}\n"
                f"<b>ADMIN:</b> {mention_html(user.id, user.first_name)}\n"
            )
            return logmsg
        else:
            msg.reply_text(
                "YoU cAN oNLY sET TIME BETWEEN 5 MINUTEs AND 1 DAY",
                parse_mode=ParseMode.HTML,
            )
    else:
        msg.reply_text(
            "UNKNoWN TIME GIvEN, GIvE ME soMETHING LIKE 5m oR 1h",
            parse_mode=ParseMode.HTML,
        )


# foR HELP MENU
# """
from Exon.modules.language import gs


def get_help(chat):
    return gs(chat, "raid_help")


# """

__mod_name__ = "A-Raid"
