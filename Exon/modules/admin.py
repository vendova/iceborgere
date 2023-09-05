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

import asyncio 

import html 

import os 

from typing import Optional 

  

from pyrogram import enums, filters 

from pyrogram.enums import ChatMemberStatus 

from pyrogram.errors import FloodWait 

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update, User 

from telegram.error import BadRequest 

from telegram.ext import CallbackContext, CommandHandler, Filters 

from telegram.utils.helpers import mention_html 

from telethon import * 

from telethon import events 

from telethon.tl import * 

from telethon.tl import functions, types 

  

from Exon import Abishnoi, dispatcher 

from Exon import telethn as bot 

from Exon.modules.connection import connected 

from Exon.modules.disable import DisableAbleCommandHandler 

from Exon.modules.helper_funcs.alternate import typing_action 

from Exon.modules.helper_funcs.chat_status import ( 

    ADMIN_CACHE, 

    bot_admin, 

    can_pin, 

    can_promote, 

    connection_status, 

    user_admin, 

    user_can_changeinfo, 

    user_can_promote, 

) 

from Exon.modules.helper_funcs.extraction import extract_user, extract_user_and_text 

from Exon.modules.log_channel import loggable 

  

  

async def is_register_admin(chat, user): 

    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)): 

        return isinstance( 

            ( 

                await bot(functions.channels.GetParticipantRequest(chat, user)) 

            ).participant, 

            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator), 

        ) 

    if isinstance(chat, types.InputPeerUser): 

        return True 

  

  

async def can_promote_users(message): 

    result = await bot( 

        functions.channels.GetParticipantRequest( 

            channel=message.chat_id, 

            user_id=message.sender_id, 

        ) 

    ) 

    p = result.participant 

    return isinstance(p, types.ChannelParticipantCreator) or ( 

        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.ban_users 

    ) 

  

  

async def can_ban_users(message): 

    result = await bot( 

        functions.channels.GetParticipantRequest( 

            channel=message.chat_id, 

            user_id=message.sender_id, 

        ) 

    ) 

    p = result.participant 

    return isinstance(p, types.ChannelParticipantCreator) or ( 

        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.ban_users 

    ) 

  

  

@bot.on(events.NewMessage(pattern="/users$")) 

async def get_users(show): 

    if not show.is_group: 

        return 

    if show.is_group and not await is_register_admin(show.input_chat, show.sender_id): 

        return 

    info = await bot.get_entity(show.chat_id) 

    title = info.title if info.title else "this chat" 

    mentions = "Users in {}: \n".format(title) 

    async for user in bot.iter_participants(show.chat_id): 

        if not user.deleted: 

            mentions += f"\n[{user.first_name}](tg://user?id={user.id}) {user.id}" 

        else: 

            mentions += f"\nDeleted account {user.id}" 

    file = open("userslist.txt", "w+") 

    file.write(mentions) 

    file.close() 

    await bot.send_file( 

        show.chat_id, 

        "userslist.txt", 

        caption="Users in {}".format(title), 

        reply_to=show.id, 

    ) 

    os.remove("userslist.txt") 

  

  

@bot_admin 

@user_admin 

def set_sticker(update: Update, context: CallbackContext): 

    msg = update.effective_message 

    chat = update.effective_chat 

    user = update.effective_user 

  

    if user_can_changeinfo(chat, user, context.bot.id) is False: 

        return msg.reply_text("You're missing rights to change chat info!") 

  

    if msg.reply_to_message: 

        if not msg.reply_to_message.sticker: 

            return msg.reply_text( 

                "You need to reply to some sticker to set chat sticker set!" 

            ) 

        stkr = msg.reply_to_message.sticker.set_name 

        try: 

            context.bot.set_chat_sticker_set(chat.id, stkr) 

            msg.reply_text(f"successfully set new group stickers in {chat.title}!") 

        except BadRequest as excp: 

            if excp.message == "Participants_too_few": 

                return msg.reply_text( 

                    "sorry, due to telegram restrictions chat needs to have minimum 100 members before they can have group stickers!" 

                ) 

            msg.reply_text(f"Error! {excp.message}.") 

    else: 

        msg.reply_text("You need to reply to some sticker to set chat sticker set!") 

  

  

@bot_admin 

@user_admin 

def setchatpic(update: Update, context: CallbackContext): 

    chat = update.effective_chat 

    msg = update.effective_message 

    user = update.effective_user 

  

    if user_can_changeinfo(chat, user, context.bot.id) is False: 

        msg.reply_text("You are missing right to change group info!") 

        RETURN 

  

    if msg.reply_to_message: 

        if msg.reply_to_message.photo: 

            pic_id = msg.reply_to_message.photo[-1].file_id 

        elif msg.reply_to_message.document: 

            pic_id = msg.reply_to_message.document.file_id 

        else: 

            msg.reply_text("You can only set some photo as chat pic!") 

            return 

        dlmsg = msg.reply_text("Just a sec......") 

        tpic = context.bot.get_file(pic_id) 

        tpic.download("gpic.png") 

        try: 

            with open("gpic.png", "rb") as chatp: 

                context.bot.set_chat_photo(int(chat.id), photo=chatp) 

                msg.reply_text("successfully set new chatpic!") 

        except BadRequest as excp: 

            msg.reply_text(f"error! {excp.message}") 

        finally: 

            dlmsg.delete() 

            if os.path.isfile("gpic.png"): 

                os.remove("gpic.png") 

    else: 

        msg.reply_text("Reply to some photo or file to set new chat pic!") 

  

  

@bot_admin 

@user_admin 

def rmchatpic(update: Update, context: CallbackContext): 

    chat = update.effective_chat 

    msg = update.effective_message 

    user = update.effective_user 

  

    if user_can_changeinfo(chat, user, context.bot.id) is False: 

        msg.reply_text("You don't have enough rights to delete group photo") 

        return 

    try: 

        context.bot.delete_chat_photo(int(chat.id)) 

        msg.reply_text("successfully deleted chat's profile photo!") 

    except BadRequest as excp: 

        msg.reply_text(f"Error! {excp.message}.") 

        return 

  

  

@bot_admin 

@user_admin 

def set_desc(update: Update, context: CallbackContext): 

    msg = update.effective_message 

    chat = update.effective_chat 

    user = update.effective_user 

  

    if user_can_changeinfo(chat, user, context.bot.id) is False: 

        return msg.reply_text("You're missing rights to change chat info!") 

  

    tesc = msg.text.split(None, 1) 

    if len(tesc) >= 2: 

        desc = tesc[1] 

    else: 

        return msg.reply_text("setting empty description won't do anything!") 

    try: 

        if len(desc) > 255: 

            return msg.reply_text("Description must needs to be under 255 characters!") 

        context.bot.set_chat_description(chat.id, desc) 

        msg.reply_text(f"successfully updated chat description in {chat.title}!") 

    except BadRequest as excp: 

        msg.reply_text(f"Error! {excp.message}.") 

  

  

@bot_admin 

@user_admin 

def setchat_title(update: Update, context: CallbackContext): 

    chat = update.effective_chat 

    msg = update.effective_message 

    user = update.effective_user 

    args = context.args 

  

    if user_can_changeinfo(chat, user, context.bot.id) is False: 

        msg.reply_text("You don't have enough rights to change chat info!") 

        RETURN 

  

    title = " ".join(args) 

    if not title: 

        msg.reply_text("Enter some text to set new title in your chat!") 

        return 

  

    try: 

        context.bot.set_chat_title(int(chat.id), str(title)) 

        msg.reply_text( 

            f"successfully set <b>{title}</b> as new chat title!", 

            parse_mode=ParseMode.HTML, 

        ) 

    except BadRequest as excp: 

        msg.reply_text(f"Error! {excp.message}.") 

        return 

  

  

@bot_admin 

@can_promote 

@user_admin 

@loggable 

@typing_action 

def promote(update: Update, context: CallbackContext) -> Optional[str]: 

    chat_id = update.effective_chat.id 

    message = update.effective_message 

    chat = update.effective_chat 

    user = update.effective_user 

    bot, args = context.bot, context.args 

  

    if user_can_promote(chat, user, bot.id) is False: 

        message.reply_text("You don't have enough rights to promote someone!") 

        return "" 

  

    user_id = extract_user(message, args) 

    if not user_id: 

        message.reply_text("Mention one.... 🤷🏻‍♂.") 

        return "" 

  

    user_member = chat.get_member(user_id) 

    if user_member.status in ["administrator", "creator"]: 

        message.reply_text("This person is already an admin...!") 

        return "" 

  

    if user_id == bot.id: 

        message.reply_text("I hope, if i could promote myself!") 

        return "" 

  

    # set same perms as bot - bot can't assign higher perms than itself! 

    bot_member = chat.get_member(bot.id) 

  

    bot.promoteChatMember( 

        chat_id, 

        user_id, 

        can_change_info=bot_member.can_change_info, 

        can_post_messages=bot_member.can_post_messages, 

        can_edit_messages=bot_member.can_edit_messages, 

        can_delete_messages=bot_member.can_delete_messages, 

        can_invite_users=bot_member.can_invite_users, 

        can_restrict_members=bot_member.can_restrict_members, 

        can_pin_messages=bot_member.can_pin_messages, 

    ) 

  

    title = "admin" 

    if " " in message.text: 

        title = message.text.split(" ", 1)[1] 

        if len(title) > 16: 

            message.reply_text( 

                "The title length is longer than 16 characters.\ntruncating it to 16 characters." 

            ) 

  

        try: 

            bot.setChatAdministratorCustomTitle(chat.id, user_id, title) 

  

        except BadRequest: 

            message.reply_text( 

                "I can't set custom title for admins that i didn't promote!" 

            ) 

  

    keyboard = InlineKeyboardMarkup( 

        [ 

            [ 

                InlineKeyboardButton( 

                    text="⏬ Demote", 

                    callback_data="demote_({})".format(user_member.user.id), 

                ), 

                InlineKeyboardButton(text="close ⛔", callback_data="close2"), 

            ] 

        ] 

    ) 

    message.reply_text( 

        f"{chat.title} Event!\n" 

        f"• A new admin has been appointed!\n" 

        f"• Let's all welcome {mention_html(user_member.user.id, user_member.user.first_name)}", 

        reply_markup=keyboard, 

        parse_mode=ParseMode.HTML, 

    ) 

    # REfREsH ADMIN cAcHE 

    try: 

        ADMIN_CACHE.pop(update.effective_chat.id) 

    except KeyError: 

        pass 

    return ( 

        "<b>{}:</b>" 

        "\n#PROMOTED" 

        "\n<b>ADMIN:</b> {}" 

        "\n<b>User:</b> {}".format( 

            html.escape(chat.title), 

            mention_html(user.id, user.first_name), 

            mention_html(user_member.user.id, user_member.user.first_name), 

        ) 

    ) 

  

  

close_keyboard = InlineKeyboardMarkup( 

    [[InlineKeyboardButton("🔄 cache", callback_data="close2")]] 

) 

  

  

@bot_admin 

@can_promote 

@user_admin 

@loggable 

@typing_action 

def fullpromote(update, context): 

    message = update.effective_message 

    chat = update.effective_chat 

    user = update.effective_user 

    bot, args = context.bot, context.args 

  

    if user_can_promote(chat, user, bot.id) is False: 

        message.reply_text("You don't have enough rights to promote someone!") 

        return "" 

  

    user_id = extract_user(message, args) 

    if not user_id: 

        message.reply_text("Mention one.... 🤷🏻‍♂.") 

        return "" 

  

    user_member = chat.get_member(user_id) 

    if user_member.status in ["administrator", "creator"]: 

        message.reply_text("This person is already an admin...!") 

        return "" 

  

    if user_id == bot.id: 

        message.reply_text("I hope, if i could promote myself!") 

        return "" 

  

    # set same perms as bot - bot can't assign higher perms than itself! 

    bot_member = chat.get_member(bot.id) 

  

    bot.promoteChatMember( 

        chat.id, 

        user_id, 

        can_change_info=bot_member.can_change_info, 

        can_post_messages=bot_member.can_post_messages, 

        can_edit_messages=bot_member.can_edit_messages, 

        can_delete_messages=bot_member.can_delete_messages, 

        can_invite_users=bot_member.can_invite_users, 

        can_promote_members=bot_member.can_promote_members, 

        can_restrict_members=bot_member.can_restrict_members, 

        can_pin_messages=bot_member.can_pin_messages, 

        can_manage_voice_chats=bot_member.can_manage_voice_chats, 

    ) 

  

    title = "admin" 

    if " " in message.text: 

        title = message.text.split(" ", 1)[1] 

        if len(title) > 16: 

            message.reply_text( 

                "The title length is longer than 16 characters.\ntruncating it to 16 characters." 

            ) 

  

        try: 

            bot.setChatAdministratorCustomTitle(chat.id, user_id, title) 

  

        except BadRequest: 

            message.reply_text( 

                "I can't set custom title for admins that i didn't promote!" 

            ) 

  

    keyboard = InlineKeyboardMarkup( 

        [ 

            [ 

                InlineKeyboardButton( 

                    text="⏬ Demote", 

                    callback_data="demote_({})".format(user_member.user.id), 

                ), 

                InlineKeyboardButton(text="🔄 close", callback_data="close2"), 

            ] 

        ] 

    ) 

    message.reply_text( 

        f" {chat.title} Event!\n" 

        f"• A new admin has been appointed as fully promoted!\n" 

        f"• Let's all welcome {mention_html(user_member.user.id, user_member.user.first_name)}", 

        reply_markup=keyboard, 

        parse_mode=ParseMode.HTML, 

    ) 

  

    log_message = ( 

        f"<b>{html.escape(chat.title)}:</b>\n" 

        f"#fullpromoted\n" 

        f"<b>ADMIN:</b> {mention_html(user.id, user.first_name)}\n" 

        f"<b>User:</b> {mention_html(user_member.user.id, user_member.user.first_name)}" 

    ) 

  

  

close_keyboard = InlineKeyboardMarkup( 

    [[InlineKeyboardButton("🔄 cache", callback_data="close2")]] 

) 

  

  

@bot_admin 

@can_promote 

@user_admin 

@loggable 

@typing_action 

def demote(update: Update, context: CallbackContext) -> Optional[str]: 

    chat = update.effective_chat 

    message = update.effective_message 

    user = update.effective_user 

    bot, args = context.bot, context.args 

  

    if user_can_promote(chat, user, bot.id) is False: 

        message.reply_text("You don't have enough rights to demote someone!") 

        return "" 

  

    user_id = extract_user(message, args) 

    if not user_id: 

        message.reply_text( 

            "You don't seem to be referring to a user or the id specified is incorrect.." 

        ) 

        return "" 

  

    user_member = chat.get_member(user_id) 

    if user_member.status == "creator": 

        message.reply_text("This person created the chat, how would i demote them?") 

        return "" 

  

    if user_member.status != "administrator": 

        message.reply_text( 

            "How i'm supposed to demote someone who is not even an admin!" 

        ) 

        return "" 

  

    if user_id == bot.id: 

        message.reply_text("Yeahhh... i'm not gonna demote myself!") 

        return "" 

  

    try: 

        bot.promoteChatMember( 

            int(chat.id), 

            int(user_id), 

            can_change_info=False, 

            can_post_messages=False, 

            can_edit_messages=False, 

            can_delete_messages=False, 

            can_invite_users=False, 

            can_restrict_members=False, 

            can_pin_messages=False, 

            can_manage_voice_chats=False, 

        ) 

        message.reply_text( 

            f"successfully demoted <b>{user_member.user.first_name or user_id}</b>!", 

            parse_mode=ParseMode.HTML, 

        ) 

        return ( 

            "<b>{}:</b>" 

            "\n#Demoted" 

            "\n<b>ADMIN:</b> {}" 

            "\n<b>User:</b> {}".format( 

                html.escape(chat.title), 

                mention_html(user.id, user.first_name), 

                mention_html(user_member.user.id, user_member.user.first_name), 

            ) 

        ) 

  

    except BadRequest: 

        message.reply_text( 

            "failed to demote. i might not be admin, or the admin status was appointed by another " 

            "User, so i can't act upon them!" 

        ) 

        return "" 

  

  

@user_admin 

def refresh_admin(update, _): 

    try: 

        ADMIN_CACHE.pop(update.effective_chat.id) 

    except KeyError: 

        pass 

  

    update.effective_message.reply_text("Admins cache refreshed!") 

  

  

@connection_status 

@bot_admin 

@can_promote 

@user_admin 

def set_title(update: Update, context: CallbackContext): 

    bot = context.bot 

    args = context.args 

  

    chat = update.effective_chat 

    message = update.effective_message 

  

    user_id, title = extract_user_and_text(message, args) 

    try: 

        user_member = chat.get_member(user_id) 

    except: 

        return 

  

    if not user_id: 

        message.reply_text( 

            "You don't seem to be referring to a user or the id specified is incorrect..", 

        ) 

        return 

  

    if user_member.status == "creator": 

        message.reply_text( 

            "This person created the chat, how can i set custom title for him?", 

        ) 

        return 

  

    if user_member.status != "administrator": 

        message.reply_text( 

            "can't set title for non-admins!\npromote them first to set custom title!", 

        ) 

        return 

  

    if user_id == bot.id: 

        message.reply_text( 

            "I can't set my own title myself! get the one who made me admin to do it for me.", 

        ) 

        return 

  

    if not title: 

        message.reply_text("setting blank title doesn't do anything!") 

        return 

  

    if len(title) > 16: 

        message.reply_text( 

            "The title length is longer than 16 characters.\ntruncating it to 16 characters.", 

        ) 

  

    try: 

        bot.setChatAdministratorCustomTitle(chat.id, user_id, title) 

    except BadRequest: 

        message.reply_text( 

            "Either they aren't promoted by me or you set a title text that is impossible to set." 

        ) 

        return 

  

    bot.sendMessage( 

        chat.id, 

        f"sucessfully set title for <code>{user_member.user.first_name or user_id}</code> " 

        f"To <code>{html.escape(title[:16])}</code>!", 

        parse_mode=ParseMode.HTML, 

    ) 

  

  

@bot_admin 

@can_pin 

@user_admin 

@loggable 

def pin(update: Update, context: CallbackContext) -> str: 

    bot, args = context.bot, context.args 

    user = update.effective_user 

    chat = update.effective_chat 

    msg = update.effective_message 

    msg_id = msg.reply_to_message.message_id if msg.reply_to_message else msg.message_id 

  

    if msg.chat.username: 

        # If chat has a username, use this format 

        link_chat_id = msg.chat.username 

        message_link = f"https://t.me/{link_chat_id}/{msg_id}" 

    elif (str(msg.chat.id)).startswith("-100"): 

        # If chat does not have a username, use this 

        link_chat_id = (str(msg.chat.id)).replace("-100", "") 

        message_link = f"https://t.me/c/{link_chat_id}/{msg_id}" 

  

    is_group = chat.type not in ("private", "channel") 

    prev_message = update.effective_message.reply_to_message 

  

    if prev_message is None: 

        msg.reply_text("Reply a message to pin it!") 

        return 

  

    is_silent = True 

    if len(args) >= 1: 

        is_silent = ( 

            args[0].lower() != "notify" 

            or args[0].lower() == "loud" 

            or args[0].lower() == "violent" 

        ) 

  

    if prev_message and is_group: 

        try: 

            bot.pinChatMessage( 

                chat.id, prev_message.message_id, disable_notification=is_silent 

            ) 

            msg.reply_text( 

                "success! pinned this message on this group", 

                reply_markup=InlineKeyboardMarkup( 

                    [ 

                        [ 

                            InlineKeyboardButton( 

                                text="📝 view messages", url=f"{message_link}" 

                            ), 

                            InlineKeyboardButton( 

                                text="❌ Delete", callback_data="close2" 

                            ), 

                        ] 

                    ] 

                ), 

                parse_mode=ParseMode.HTML, 

                disable_web_page_preview=True, 

            ) 

        except BadRequest as excp: 

            if excp.message != "Chat_not_modified": 

                raise 

  

        log_message = ( 

            f"<b>{html.escape(chat.title)}:</b>\n" 

            f"PINNED\n" 

            f"<b>ADMIN:</b> {mention_html(user.id, html.escape(user.first_name))}" 

        ) 

  

        return log_message 

  

  

close_keyboard = InlineKeyboardMarkup( 

    [[InlineKeyboardButton("❌ Delete", callback_data="close2")]] 

) 

  

  

@bot_admin 

@can_pin 

@user_admin 

@loggable 

def unpin(update: Update, context: CallbackContext): 

    chat = update.effective_chat 

    user = update.effective_user 

    msg = update.effective_message 

    msg_id = msg.reply_to_message.message_id if msg.reply_to_message else msg.message_id 

    unpinner = chat.get_member(user.id) 

  

    if ( 

        not (unpinner.can_pin_messages or unpinner.status == "creator") 

        and user.id not in DRAGONS 

    ): 

        message.reply_text("You don have the necessary rights to do that!") 

        return 

  

    if msg.chat.username: 

        # If chat has a username, use this format 

        link_chat_id = msg.chat.username 

        message_link = f"https://t.me/{link_chat_id}/{msg_id}" 

    elif (str(msg.chat.id)).startswith("-100"): 

        # If chat does not have a username, use this 

        link_chat_id = (str(msg.chat.id)).replace("-100", "") 

        message_link = f"https://t.me/c/{link_chat_id}/{msg_id}" 

  

    is_group = chat.type not in ("private", "channel") 

    prev_message = update.effective_message.reply_to_message 

  

    if prev_message and is_group: 

        try: 

            context.bot.unpinChatMessage(chat.id, prev_message.message_id) 

            msg.reply_text( 

                f"UNPINNED <a href='{message_link}'>this message</a>.", 

                parse_mode=ParseMode.HTML, 

                disable_web_page_preview=True, 

            ) 

        except BadRequest as excp: 

            if excp.message != "Chat_not_modified": 

                raise 

  

    if not prev_message and is_group: 

        try: 

            context.bot.unpinChatMessage(chat.id) 

            msg.reply_text("🔽 Unpinned the last message on this group.") 

        except BadRequest as excp: 

            if excp.message == "Message to unpin not found": 

                msg.reply_text( 

                    "I can't see pinned message, maybe already unpined, or pin message to old 🙂" 

                ) 

            else: 

                raise 

  

    log_message = ( 

        f"<b>{html.escape(chat.title)}:</b>\n" 

        f"Message-unpinned-successfully\n" 

        f"<b>ADMIN:</b> {mention_html(user.id, html.escape(user.first_name))}" 

    ) 

  

    return log_message 

  

  

@bot_admin 

def pinned(update: Update, context: CallbackContext) -> str: 

    bot = context.bot 

    msg = update.effective_message 

    msg_id = ( 

        update.effective_message.reply_to_message.message_id 

        if update.effective_message.reply_to_message 

        else update.effective_message.message_id 

    ) 

  

    chat = bot.getChat(chat_id=msg.chat.id) 

    if chat.pinned_message: 

        pinned_id = chat.pinned_message.message_id 

        if msg.chat.username: 

            link_chat_id = msg.chat.username 

            message_link = f"https://t.me/{link_chat_id}/{pinned_id}" 

        elif (str(msg.chat.id)).startswith("-100"): 

            link_chat_id = (str(msg.chat.id)).replace("-100", "") 

            message_link = f"https://t.me/c/{link_chat_id}/{pinned_id}" 

  

        msg.reply_text( 

            f"📌 Pinned the message on {html.escape(chat.title)}.", 

            reply_to_message_id=msg_id, 

            parse_mode=ParseMode.HTML, 

            disable_web_page_preview=True, 

            reply_markup=InlineKeyboardMarkup( 

                [ 

                    [ 

                        InlineKeyboardButton( 

                            text="Pinned messages", 

                            url=f"https://t.me/{link_chat_id}/{pinned_id}", 

                        ) 

                    ] 

                ] 

            ), 

        ) 

  

    else: 

        msg.reply_text( 

            f"There is no pinned message on <b>{html.escape(chat.title)}!</b>", 

            parse_mode=ParseMode.HTML, 

        ) 

  

  

@bot_admin 

@user_admin 

@typing_action 

def invite(update, context): 

    bot = context.bot 

    user = update.effective_user 

    msg = update.effective_message 

    chat = update.effective_chat 

  

    conn = connected(bot, update, chat, user.id, need_admin=True) 

    if conn: 

        chat = dispatcher.bot.getChat(conn) 

    else: 

        if msg.chat.type == "private": 

            msg.reply_text("This command is meant to use in chat not in pm") 

            return "" 

        chat = update.effective_chat 

  

    if chat.username: 

        msg.reply_text(chat.username) 

    elif chat.type in [chat.SUPERGROUP, chat.CHANNEL]: 

        bot_member = chat.get_member(bot.id) 

        if bot_member.can_invite_users: 

            invitelink = context.bot.exportChatInviteLink(chat.id) 

            msg.reply_text(invitelink) 

        else: 

            msg.reply_text( 

                "I don't have access to the invite link, try changing my permissions!" 

            ) 

    else: 

        msg.reply_text( 

            "I can only give you invite links for supergroups and channels, sorry!" 

        ) 

  

  

"""         

@Abishnoi.on_message(filters.command(["staff", "admins", "adminlist"]) & filters.group) 

    uname = f"ADMINs IN {message.chat.title} :\n\n" 

    async for gey in app.iter_chat_members(message.chat.id, filter="administrators"): 

        try: 

            uname += f"@{(await app.get_users(int(gey.user.id))).username}\n" 

        except: 

            uname += "" 

    await message.reply_text(uname) 

""" 

  

  

@Abishnoi.on_message(filters.command(["adminlist", "staff", "admins"])) 

async def admins(client, message): 

    try: 

        adminList = [] 

        ownerList = [] 

        async for admin in Abishnoi.get_chat_members( 

            message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS 

        ): 

            if admin.privileges.is_anonymous == False: 

                if admin.user.is_bot == True: 

                    pass 

                elif admin.status == ChatMemberStatus.OWNER: 

                    ownerList.append(admin.user) 

                else: 

                    adminList.append(admin.user) 

            else: 

                pass 

        lenAdminList = len(ownerList) + len(adminList) 

        text2 = f"**Group staff - {message.chat.title}**\n\n" 

        try: 

            owner = ownerList[0] 

            if owner.username == None: 

                text2 += f"👑 owner\n└ {owner.mention}\n\n👮🏻 admins\n" 

            else: 

                text2 += f"👑 owner\n└ @{owner.username}\n\n👮🏻 admins\n" 

        except: 

            text2 += f"👑 owner\n└ <i>hidden</i>\n\n👮🏻 admins\n" 

        if len(adminList) == 0: 

            text2 += "└ <i>Admins are hidden</i>" 

            await Abishnoi.send_message(message.chat.id, text2) 

        else: 

            while len(adminList) > 1: 

                admin = adminList.pop(0) 

                if admin.username == None: 

                    text2 += f"├ {admin.mention}\n" 

                else: 

                    text2 += f"├ @ {admin.username}\n" 

            else: 

                admin = adminList.pop(0) 

                if admin.username == None: 

                    text2 += f"└ {admin.mention}\n\n" 

                else: 

                    text2 += f"└ @ {admin.username}\n\n" 

            text2 += f"✅ | **Total number of admins**: {lenAdminList}\n❌ | Bots and anonymous admins were rejected." 

            await Abishnoi.send_message(message.chat.id, text2) 

    except FloodWait as e: 

        await asyncio.sleep(e.value) 

  

  

@Abishnoi.on_message(filters.command("bots")) 

async def bots(client, message): 

    try: 

        botList = [] 

        async for bot in Abishnoi.get_chat_members( 

            message.chat.id, filter=enums.ChatMembersFilter.BOTS 

        ): 

            botList.append(bot.user) 

        lenBotList = len(botList) 

        text3 = f"**Bot list - {message.chat.title}**\n\n🤖 bots\n" 

        while len(botList) > 1: 

            bot = botList.pop(0) 

            text3 += f"├ @{bot.username}\n" 

        else: 

            bot = botList.pop(0) 

            text3 += f"└ @{bot.username}\n\n" 

            text3 += f"✅ | **Total number of bots**: {lenBotList}" 

            await Abishnoi.send_message(message.chat.id, text3) 

    except FloodWait as e: 

        await asyncio.sleep(e.value) 

  

  

@bot_admin 

@can_promote 

@user_admin 

@loggable 

def button(update: Update, context: CallbackContext) -> str: 

    query: Optional[CallbackQuery] = update.callback_query 

    user: Optional[User] = update.effective_user 

    bot: Optional[Bot] = context.bot 

    match = re.match(r"demote_\((.+?)\)", query.data) 

    if match: 

        user_id = match.group(1) 

        chat: Optional[Chat] = update.effective_chat 

        member = chat.get_member(user_id) 

        bot_member = chat.get_member(bot.id) 

        bot_permissions = promoteChatMember( 

            chat.id, 

            user_id, 

            can_change_info=bot_member.can_change_info, 

            can_post_messages=bot_member.can_post_messages, 

            can_edit_messages=bot_member.can_edit_messages, 

            can_delete_messages=bot_member.can_delete_messages, 

            can_invite_users=bot_member.can_invite_users, 

            can_promote_members=bot_member.can_promote_members, 

            can_restrict_members=bot_member.can_restrict_members, 

            can_pin_messages=bot_member.can_pin_messages, 

            can_manage_voice_chats=bot_member.can_manage_voice_chats, 

        ) 

        demoted = bot.promoteChatMember( 

            chat.id, 

            user_id, 

            can_change_info=False, 

            can_post_messages=False, 

            can_edit_messages=False, 

            can_delete_messages=False, 

            can_invite_users=False, 

            can_restrict_members=False, 

            can_pin_messages=False, 

            can_promote_members=False, 

            can_manage_voice_chats=False, 

        ) 

        if demoted: 

            update.effective_message.edit_text( 

                f"YEP! {mention_html(user_member.user.id, user_member.user.first_name)} has been demoted in {chat.title}!" 

                f"BY {mention_html(user.id, user.first_name)}", 

                parse_mode=ParseMode.HTML, 

            ) 

            query.answer("DEMoTED!") 

            return ( 

                f"<b>{html.escape(chat.title)}:</b>\n" 

                f"#DEMoTE\n" 

                f"<b>ADMIN:</b> {mention_html(user.id, user.first_name)}\n" 

                f"<b>UseR:</b> {mention_html(member.user.id, member.user.first_name)}" 

            ) 

    else: 

        update.effective_message.edit_text( 

            "This user is not promoted or has left the group!" 

        ) 

        return "" 

  

  

SET_DESC_HANDLER = CommandHandler( 

    "setdesc", set_desc, filters=Filters.chat_type.groups, run_async=True 

) 

SET_STICKER_HANDLER = CommandHandler( 

    "setsticker", set_sticker, filters=Filters.chat_type.groups, run_async=True 

) 

SETCHATPIC_HANDLER = CommandHandler( 

    "setgpic", setchatpic, filters=Filters.chat_type.groups, run_async=True 

) 

RMCHATPIC_HANDLER = CommandHandler( 

    "delgpic", rmchatpic, filters=Filters.chat_type.groups, run_async=True 

) 

SETCHAT_TITLE_HANDLER = CommandHandler( 

    "setgtitle", setchat_title, filters=Filters.chat_type.groups, run_async=True 

) 

  

PIN_HANDLER = CommandHandler( 

    "pin", pin, filters=Filters.chat_type.groups, run_async=True 

) 

UNPIN_HANDLER = CommandHandler( 

    "unpin", unpin, filters=Filters.chat_type.groups, run_async=True 

) 

PINNED_HANDLER = CommandHandler( 

    "pinned", pinned, filters=Filters.chat_type.groups, run_async=True 

) 

  

INVITE_HANDLER = DisableAbleCommandHandler("invitelink", invite, run_async=True) 

  

PROMOTE_HANDLER = DisableAbleCommandHandler("promote", promote, run_async=True) 

FULLPROMOTE_HANDLER = DisableAbleCommandHandler( 

    "fullpromote", fullpromote, run_async=True 

) 

DEMOTE_HANDLER = DisableAbleCommandHandler("demote", demote, run_async=True) 

  

SET_TITLE_HANDLER = CommandHandler("title", set_title, run_async=True) 

ADMIN_REFRESH_HANDLER = CommandHandler( 

    "admincache", refresh_admin, filters=Filters.chat_type.groups, run_async=True 

) 

  

dispatcher.add_handler(SET_DESC_HANDLER) 

dispatcher.add_handler(SET_STICKER_HANDLER) 

dispatcher.add_handler(SETCHATPIC_HANDLER) 

dispatcher.add_handler(RMCHATPIC_HANDLER) 

dispatcher.add_handler(SETCHAT_TITLE_HANDLER) 

dispatcher.add_handler(PIN_HANDLER) 

dispatcher.add_handler(UNPIN_HANDLER) 

dispatcher.add_handler(PINNED_HANDLER) 

dispatcher.add_handler(INVITE_HANDLER) 

dispatcher.add_handler(PROMOTE_HANDLER) 

dispatcher.add_handler(FULLPROMOTE_HANDLER) 

dispatcher.add_handler(DEMOTE_HANDLER) 

dispatcher.add_handler(SET_TITLE_HANDLER) 

dispatcher.add_handler(ADMIN_REFRESH_HANDLER) 

  

__mod_name__ = "ADMIN" 

__command_list__ = [ 

    "setdesc" "setsticker" "setgpic" "delgpic" "setgtitle", 

    "admins", 

    "invitelink", 

    "promote", 

    "fullpromote", 

    "demote", 

    "admincache", 

] 

__handlers__ = [ 

    SET_DESC_HANDLER, 

    SET_STICKER_HANDLER, 

    SETCHATPIC_HANDLER, 

    RMCHATPIC_HANDLER, 

    SETCHAT_TITLE_HANDLER, 

    PIN_HANDLER, 

    UNPIN_HANDLER, 

    PINNED_HANDLER, 

    INVITE_HANDLER, 

    PROMOTE_HANDLER, 

    FULLPROMOTE_HANDLER, 

    DEMOTE_HANDLER, 

    SET_TITLE_HANDLER, 

    ADMIN_REFRESH_HANDLER, 

] 

  

  

# foR HELP MENU 

  

# """ 

from Exon.modules.language import gs 

  

  

def get_help(chat): 

    return gs(chat, "admin_help") 

  

  

# """ 