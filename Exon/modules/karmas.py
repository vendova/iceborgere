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
# TG :- @Abishnoi1M
#      :- Abishnoi_bots
#     GITHUB :- Abishnoi69 ""


import asyncio

from pyrogram import filters

from Exon import OWNER_ID
from Exon import Abishnoi as abishnoi
from Exon.modules.no_sql.karma_db import (
    alpha_to_int,
    get_karma,
    get_karmas,
    int_to_alpha,
    is_karma_on,
    karma_off,
    karma_on,
    update_karma,
)

regex_upvote = r"^((?i)\+|\+\+|\+1|\++|\+69|thx|thanx|thanks|🖤|❣️|💝|💖|💕|❤|💘|cool|good|seer|ch|👍|baby|thankyou|love|pro)$"
regex_downvote = r"^(\-|\-\-|\-1|👎|💔|noob|fool|weak|fuck off|nub|gey|kid|shit|mf)$"

karma_positive_group = 3
karma_negative_group = 4


@abishnoi.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_upvote)
    & ~filters.via_bot
    & ~filters.bot,
    group=karma_positive_group,
)
async def upvote(_, message):
    if not await is_karma_on(message.chat.id):
        return
    if not message.reply_to_message.from_user:
        return
    if not message.from_user:
        return
    if message.reply_to_message.from_user.id == OWNER_ID:
        await message.reply_text("How so PRO ?")
        return
    if message.reply_to_message.from_user.id == message.from_user.id:
        return
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
    if current_karma:
        current_karma = current_karma["karma"]
        karma = current_karma + 1
    else:
        karma = 1
    new_karma = {"karma": karma}
    await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    again = await message.reply_text(
        f"Increased karma of {user_mention} by 1.\n**Total points :** {karma}"
    )
    await asyncio.sleep(18)
    await again.delete()


@abishnoi.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_downvote)
    & ~filters.via_bot
    & ~filters.bot,
    group=karma_negative_group,
)
async def downvote(_, message):
    if not await is_karma_on(message.chat.id):
        return
    if not message.reply_to_message.from_user:
        return
    if not message.from_user:
        return
    if message.reply_to_message.from_user.id == OWNER_ID:
        await message.reply_text("😐.")
        return
    if message.reply_to_message.from_user.id == message.from_user.id:
        return
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    current_karma = await get_karma(message.chat.id, await int_to_alpha(user_id))
    if current_karma:
        current_karma = current_karma["karma"]
        karma = current_karma - 1
    else:
        karma = 0
    new_karma = {"karma": karma}
    await update_karma(message.chat.id, await int_to_alpha(user_id), new_karma)
    again = await message.reply_text(
        f"Decreased karma of {user_mention} by 1.\n**Total points :** {karma}"
    )
    await asyncio.sleep(12)
    await again.delete()
    


@abishnoi.on_cmd("karmastat", group_only=True)
@abishnoi.adminsOnly(permissions="can_change_info", is_both=True)
async def command_karma(_, message):
    chat_id = message.chat.id
    if not message.reply_to_message:
        m = await message.reply_text("Top karma points ...")
        karma = await get_karmas(chat_id)
        if not karma:
            await m.edit("No Karma in database.")
            return
        msg = f"🏆 **   Karma list of {message.chat.title}**\n"
        limit = 0
        karma_dicc = {}
        for i in karma:
            user_id = await alpha_to_int(i)
            user_karma = karma[i]["karma"]
            karma_dicc[str(user_id)] = user_karma
            karma_arranged = dict(
                sorted(
                    karma_dicc.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            )
        if not karma_dicc:
            await m.edit("No Karma in database..")
            return
        for user_idd, karma_count in karma_arranged.items():
            if limit > 9:
                break
            try:
                user = await app.get_users(int(user_idd))
                await asyncio.sleep(0.8)
            except Exception:
                continue
            first_name = user.first_name
            if not first_name:
                continue
            username = user.username
            msg += f"\n≛ [{first_name}](https://t.me/{username}) : {karma_count}"
            limit += 1
        await m.edit(msg, disable_web_page_preview=True)
    else:
        user_id = message.reply_to_message.from_user.id
        karma = await get_karma(chat_id, await int_to_alpha(user_id))
        if karma:
            karma = karma["karma"]
            await message.reply_text(f"**Total points**: __{karma}__")
        else:
            karma = 0
            await message.reply_text(f"**Total points**: __{karma}__")


@abishnoi.on_cmd("karma", group_only=True)
@abishnoi.adminsOnly(permissions="can_change_info", is_both=True)
async def captcha_state(_, message):
    usage = "**ᴜsᴀɢᴇ:**\n/karma [ON|OFF]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "on":
        await karma_on(message.chat.id)
        await message.reply_text("Enabled Karma system.")
    elif state == "off":
        await karma_off(message.chat.id)
        await message.reply_text("Disabled Karma system.")
    else:
        await message.reply_text(usage)
