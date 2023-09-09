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

    return "{} hour(s)".format(t[0]) if time >= 3600 else "{} minutes".format(t[1]) 

  

  

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

        context.bot.sendMessage(chat.id, "This command is not available in pms.") 

        return 

    stat, time, acttime = sql.getDefenseStatus(chat.id) 

    readable_time = get_readable_time(time) 

    if len(args) == 0: 

        if stat: 

            text = "Raid mode is currently <code>enabled</code>\nwould you like to <code>disable</code> raid?" 

            keyboard = [ 

                [ 

                    InlineKeyboardButton( 

                        "Disable raid", 

                        callback_data="disable_raid={}={}".format(chat.id, time), 

                    ), 

                    InlineKeyboardButton("cancel", callback_data="cancel_raid=1"), 

                ] 

            ] 

        else: 

            text = f"Raid mode is currently <code>disabled</code>\nwould you like to <code>enable</code> raid for {readable_time}?" 

            keyboard = [ 

                [ 

                    InlineKeyboardButton( 

                        "Enable raid", 

                        callback_data="enable_raid={}={}".format(chat.id, time), 

                    ), 

                    InlineKeyboardButton("cancel", callback_data="cancel_raid=0"), 

                ] 

            ] 

        reply_markup = InlineKeyboardMarkup(keyboard) 

        msg.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup) 

  

    elif args[0] == "off": 

        if stat: 

            sql.setDefenseStatus(chat.id, False, time, acttime) 

            text = "Raid mode has been <code>disabled</code>, members that join will no longer be kicked." 

            msg.reply_text(text, parse_mode=ParseMode.HTML) 

            logmsg = ( 

                f"<b>{html.escape(chat.title)}:</b>\n" 

                f"#RAID\n" 

                f"Disabled\n" 

                f"<b>ADMIN:</b> {mention_html(user.id, user.first_name)}\n" 

            ) 

            return logmsg 

  

    else: 

        args_time = args[0].lower() 

        time = get_time(args_time) 

        if time: 

            readable_time = get_readable_time(time) 

            if time >= 300 and time < 86400: 

                text = f"Raid mode is currently <code>disabled</code>\nwould you like to <code>enable</code> raid for {readable_time}?" 

                keyboard = [ 

                    [ 

                        InlineKeyboardButton( 

                            "ENABLE RAID", 

                            callback_data="enable_raid={}={}".format(chat.id, time), 

                        ), 

                        InlineKeyboardButton("cancel", callback_data="cancel_raid=0"), 

                    ] 

                ] 

                reply_markup = InlineKeyboardMarkup(keyboard) 

                msg.reply_text( 

                    text, parse_mode=ParseMode.HTML, reply_markup=reply_markup 

                ) 

            else: 

                msg.reply_text( 

                    "You can only set time between 5 minutes and 1 day.", 

                    parse_mode=ParseMode.HTML, 

                ) 

  

        else: 

            msg.reply_text( 

                "Unknown time given, give me something like 5m or 1h.", 

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

        f"Raid mode has been <code>enabled</code> for {readable_time}.", 

        parse_mode=ParseMode.HTML, 

    ) 

    log.info("Enabled raid mode in {} for {}!".format(chat_id, readable_time)) 

  

    def disable_raid(_): 

        sql.setDefenseStatus(chat_id, False, t, acttime) 

        log.info("Disbled raid mode in {}!".format(chat_id)) 

        logmsg = ( 

            f"<b>{html.escape(chat.title)}:</b>\n" 

            f"#RAID\n" 

            f"Automatically disabled\n" 

        ) 

        return logmsg 

  

    j.run_once(disable_raid, time) 

    logmsg = ( 

        f"<b>{html.escape(chat.title)}:</b>\n" 

        f"#RAID\n" 

        f"Enablbed for {readable_time}\n" 

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

        "Raid mode has been <code>disabled</code>, joinig members will no longer be kicked.", 

        parse_mode=ParseMode.HTML, 

    ) 

    logmsg = ( 

        f"<b>{html.escape(chat.title)}:</b>\n" 

        f"#RAID\n" 

        f"Disabled\n" 

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

        f"Action cancelled, raid mode will stay <code>{'enabled' if what ==1 else 'disabled'}</code>.", 

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

            f"Raid mode is currently set to {get_readable_time(time)}\nwhen toggled, the raid mode will last for {get_readable_time(time)} then turn off automatically.", 

            parse_mode=ParseMode.HTML, 

        ) 

        return 

    args_time = args[0].lower() 

    time = get_time(args_time) 

    if time: 

        readable_time = get_readable_time(time) 

        if time >= 300 and time < 86400: 

            text = f"Raid mode is currently set to {readable_time}\nwhen toggled, the raid mode will last for {readable_time} then turn off automatically." 

            msg.reply_text(text, parse_mode=ParseMode.HTML) 

            sql.setDefenseStatus(chat.id, what, time, acttime) 

            logmsg = ( 

                f"<b>{html.escape(chat.title)}:</b>\n" 

                f"#RAID\n" 

                f"set raid mode time to {readable_time}\n" 

                f"<b>ADMIN:</b> {mention_html(user.id, user.first_name)}\n" 

            ) 

            return logmsg 

        else: 

            msg.reply_text( 

                "You can only set time between 5 minutes and 1 day!", 

                parse_mode=ParseMode.HTML, 

            ) 

    else: 

        msg.reply_text( 

            "Unknown time given, give me something like 5m or 1h!", 

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

            f"Raid actoin time is currently set to {get_readable_time(time)}\nwhen toggled, the members that join will be temp banned for {get_readable_time(time)}!", 

            parse_mode=ParseMode.HTML, 

        ) 

        return 

    args_time = args[0].lower() 

    time = get_time(args_time) 

    if time: 

        readable_time = get_readable_time(time) 

        if time >= 300 and time < 86400: 

            text = f"Raid actoin time is currently set to {get_readable_time(time)}\nwhen toggled, the members that join will be temp banned for {readable_time}!" 

            msg.reply_text(text, parse_mode=ParseMode.HTML) 

            sql.setDefenseStatus(chat.id, what, t, time) 

            logmsg = ( 

                f"<b>{html.escape(chat.title)}:</b>\n" 

                f"#RAID\n" 

                f"set raid mode action time to {readable_time}\n" 

                f"<b>ADMIN:</b> {mention_html(user.id, user.first_name)}\n" 

            ) 

            return logmsg 

        else: 

            msg.reply_text( 

                "You can only set time between 5 minutes and 1 day!", 

                parse_mode=ParseMode.HTML, 

            ) 

    else: 

        msg.reply_text( 

            "Unknown time given, give me something like 5m or 1h!", 

            parse_mode=ParseMode.HTML, 

        )

 
