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

  

from telethon import Button, events, types 

from telethon.errors import ChatAdminRequiredError 

from telethon.errors.rpcerrorlist import UserNotParticipantError 

from telethon.tl.functions.channels import GetParticipantRequest 

  

from Exon import BOT_ID 

from Exon import DRAGONS as DEVS 

from Exon import OWNER_ID 

from Exon import telethn as Rani 

from Exon.events import Asuinline 

from Exon.events import register as Asubot 

from Exon.modules.no_sql import fsub_db as db 

  

  

async def is_admin(chat_id, user_id): 

    try: 

        p = await Rani(GetParticipantRequest(chat_id, user_id)) 

    except UserNotParticipantError: 

        return False 

    if isinstance(p.participant, types.ChannelParticipantAdmin) or isinstance( 

        p.participant, types.ChannelParticipantCreator 

    ): 

        return True 

    else: 

        return False 

  

  

async def participant_check(channel, user_id): 

    try: 

        await Rani(GetParticipantRequest(channel, int(user_id))) 

        return True 

    except UserNotParticipantError: 

        return False 

    except: 

        return False 

  

  

@Asubot(pattern="^/(fsub|Fsub|forcesubscribe|Forcesub|forcesub|Forcesubscribe) ?(.*)") 

async def fsub(event): 

    if event.is_private: 

        return 

    if event.is_group: 

        perm = await event.client.get_permissions(event.chat_id, event.sender_id) 

        if not perm.is_admin: 

            return await event.reply("You need to be an admin to do this.") 

        if not perm.is_creator: 

            return await event.reply( 

                "! <b>Group creator reouired</b> \n<i>you have to be the group creator to do that.</i>", 

                parse_mode="html", 

            ) 

    try: 

        channel = event.text.split(None, 1)[1] 

    except IndexError: 

        channel = None 

    if not channel: 

        chat_db = db.fs_settings(event.chat_id) 

        if not chat_db: 

            await event.reply( 

                "<b>❌ force subscribe is disabled in this chat.</b>", parse_mode="HTML" 

            ) 

        else: 

            await event.reply( 

                f"forcesubscribe is currently <b>enabled</b>. users are forced to join <b>@{chat_db.channel}</b> to speak here.", 

                parse_mode="html", 

            ) 

    elif channel in ["on", "yes", "y"]: 

        await event.reply("!Please specify the channel username.") 

    elif channel in ["off", "no", "n"]: 

        await event.reply("**❌ force subscribe is disabled successfully.**") 

        db.disapprove(event.chat_id) 

    else: 

        try: 

            channel_entity = await event.client.get_entity(channel) 

        except: 

            return await event.reply( 

                "!<b>Invalid channel username provided.</b>", parse_mode="html" 

            ) 

        channel = channel_entity.username 

        try: 

            if not channel_entity.broadcast: 

                return await event.reply("That's not a valid channel.") 

        except: 

            return await event.reply("That's not a valid channel.") 

        if not await participant_check(channel, BOT_ID): 

            return await event.reply( 

                f"!**Not an admin in the channel**\ni am not an admin in the [channel](https://t.me/{channel}). add me as a admin in order to enable forcesubscribe.", 

                link_preview=False, 

            ) 

        db.add_channel(event.chat_id, str(channel)) 

        await event.reply(f"✅ **force subscribe is enabled** to @{channel}.") 

  

  

@Rani.on(events.NewMessage()) 

async def fsub_n(e): 

    if not db.fs_settings(e.chat_id): 

        return 

    if e.is_private: 

        return 

    if e.chat.admin_rights: 

        if not e.chat.admin_rights.ban_users: 

            return 

    else: 

        return 

    if not e.from_id: 

        return 

    if ( 

        await is_admin(e.chat_id, e.sender_id) 

        or e.sender_id in DEVS 

        or e.sender_id == OWNER_ID 

    ): 

        return 

    channel = (db.fs_settings(e.chat_id)).get("channel") 

    try: 

        check = await participant_check(channel, e.sender_id) 

    except ChatAdminRequiredError: 

        return 

    if not check: 

        buttons = [Button.url("Join channel", f"t.me/{channel}")], [ 

            Button.inline("UNMUTE ME", data="fs_{}".format(str(e.sender_id))) 

        ] 

        txt = f'<b><a href="tg://user?id={e.sender_id}">{e.sender.first_name}</a></b>, you have <b>not subscribed</b> to our <b><a href="t.me/{channel}">channel</a></b> yet!.please <b><a href="t.me/{channel}">join</a></b> and <b>press the button below</b> to unmute yourself.' 

        await e.reply(txt, buttons=buttons, parse_mode="html", link_preview=False) 

        await e.client.edit_permissions(e.chat_id, e.sender_id, send_messages=False) 

  

  

@Asuinline(pattern=r"fs(\_(.*))") 

async def unmute_fsub(event): 

    user_id = int(((event.pattern_match.group(1)).decode()).split("_", 1)[1]) 

    if not event.sender_id == user_id: 

        return await event.answer("This is not meant for you.", alert=True) 

    channel = (db.fs_settings(event.chat_id)).get("channel") 

    try: 

        check = await participant_check(channel, user_id) 

    except ChatAdminRequiredError: 

        check = False 

        return 

    if not check: 

        return await event.answer( 

            "You have to join the channel first, to get unmuted!", alert=True 

        ) 

    try: 

        await event.client.edit_permissions(event.chat_id, user_id, send_messages=True) 

    except ChatAdminRequiredError: 

        pass 

    await event.delete() 

  

  

__mod_name__ = "F-Sub" 

  

# foR HELP MENU 

  

# """ 

from Exon.modules.language import gs 

  

  

def get_help(chat): 

    return gs(chat, "fsub_help") 

  

  

# """ 

 
