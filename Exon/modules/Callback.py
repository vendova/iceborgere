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

from pyrogram.types import CallbackQuery
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackQueryHandler

from Exon import BOT_NAME, OWNER_ID, OWNER_USERNAME, SUPPORT_CHAT
from Exon import Abishnoi as pbot
from Exon import dispatcher


@pbot.on_callback_query()
async def close(Client, cb: CallbackQuery):
    if cb.data == "close2":
        await cb.answer()
        await cb.message.delete()


# CALLBACKS


def ABG_about_callback(update, context):
    query = update.callback_query
    if query.data == "ABG_":
        query.message.edit_text(
            text=f"I'm {BOT_NAME} ,A @werewolfquicker group management bot."
            "\nI can restrict and scan for disruptive users."
            "\nI greet new users with customizable welcome messages and can even set group rules."
            "\nI have an advanced anti-flood system."
            "\nI warn users until they reach max warns, with predefined actions like ban, mute, kick, etc."
            "\nI feature note keeping, blacklists, and predetermined replies to certain keywords."
            "\nI check for admins' permissions before executing any command and more."
            "\n\n_quickerobot licensed under the GNU general public license v3.0_"
            "\n\n*Click the button below to get basic help for using quickerobot.*.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ADMINS", callback_data="ABG_admin"),
                        InlineKeyboardButton(text="NOTES", callback_data="ABG_notes"),
                    ],
                    [
                        InlineKeyboardButton(
                            text="SUPPORT", callback_data="ABG_support"
                        ),
                        InlineKeyboardButton(
                            text="CREDIT", callback_data="ABG_credit"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="SOURCE",
                            callback_data="source_",
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="GO BACK", callback_data="start_back"
                        ),
                    ],
                ]
            ),
        )

    elif query.data == "ABG_admin":
        query.message.edit_text(
            text=f"━━━━━━━ *ADMIN* ━━━━━━━\nHere is the help for the music module\n⍟*ADMIN*\nOnly Admins can use these commands\n/pause/n»Pause the current ongoing stream.\n/resume\n» Resumed the paused stream.\n/skip ᴏʀ /next\n»Skip the current ongoing stream.\n/end ᴏʀ /stop\n» End the current ongoing stream.\n⍟*ᴀᴜᴛʜ*\nCommands to AUTH/UNAUTH any user\n• Authorized users can SKIP, PAUSE, RESUME and END the stream without admin rights./n/auth Username or reply to a user's message\n» Add a user to authorized users list of the group.\n/unauth Username or reply to a user's message \n» Removes the user from authorized users list.\n/authusers \n» Shows the list of authorized users of the group.\n⍟*ᴘʟᴀʏ*\nCommands to play songs\n/play <sᴏɴɢ ɴᴀᴍᴇ/ʏᴛ ᴜʀʟ>\n» Starts playing the reouested song on vc.!",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🏡", callback_data="start_back"),
                        InlineKeyboardButton(text="🛡️", callback_data="AsuX_help"),
                        InlineKeyboardButton(text="💳", callback_data="ABG_credit"),
                        InlineKeyboardButton(text="🕹️", callback_data="source_"),
                        InlineKeyboardButton(text="🖥️", callback_data="help_back"),
                    ]
                ]
            ),
        )

    elif query.data == "ABG_notes":
        query.message.edit_text(
            text=f"<b>SETTING UP NOTES</b>"
            f"\nyou can save ᴍᴇssᴀɢᴇ/ᴍᴇᴅɪᴀ/ᴀᴜᴅɪᴏ or anything as notes"
            f"\nto get a note simply use # at the beginning of a word"
            f"\n\nyou can also set buttons for notes and filters (ʀᴇғᴇʀ ʜᴇʟᴘ ᴍᴇɴᴜ)",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="ɢᴏ ʙᴀᴄᴋ", callback_data="ABG_")]]
            ),
        )
    elif query.data == "ABG_support":
        query.message.edit_text(
            text=f"*{BOT_NAME} SUPPORT CHATS*"
            "\njoin my support ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ for see or report a problem on quickerobot",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="SUPPORT", url=f"t.me/{SUPPORT_CHAT}"
                        ),
                        InlineKeyboardButton(
                            text="UPDATES", url="https://t.me/werewolfquicker"
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="GO BACK", callback_data="ABG_"),
                    ],
                ]
            ),
        )

    elif query.data == "ABG_credit":  # Credit  i hope edit nai hoga
        query.message.edit_text(
            text=f"━━━━━━━ *CREDIT* ━━━━━━━"
            "\n🛡️ *credit for quickerobot robot* 🛡️"
            "\n\nhere is the developer and"
            f"\nsponsor of [{BOT_NAME}](t.me/quickerobot)",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🏡", callback_data="start_back"),
                        InlineKeyboardButton(text="🛡️", callback_data="ABG_admin"),
                        InlineKeyboardButton(text="💳", callback_data="AsuX_help"),
                        InlineKeyboardButton(text="🧑‍", callback_data="source_"),
                        InlineKeyboardButton(text="🖥️", callback_data="help_back"),
                    ],
                    [
                        InlineKeyboardButton(
                            text="VLADMIR", url="https://t.me/iceborger"
                        ),
                        InlineKeyboardButton(
                            text="CHAT", url=f"https://t.me/{SUPPORT_CHAT}"
                        ),
                    ],
                ]
            ),
        )


def Source_about_callback(update, context):
    query = update.callback_query
    if query.data == "source_":
        query.message.edit_text(
            text=f"""
*Hey,
 This is {BOT_NAME} ,
An open-source telegram group management bot.*

Written in python with the help of : [ᴛᴇʟᴇᴛʜᴏɴ](https://github.com/LonamiWebs/Telethon)
[ᴩʏʀᴏɢʀᴀᴍ](https://github.com/pyrogram/pyrogram)
[ᴩʏᴛʜᴏɴ-ᴛᴇʟᴇɢʀᴀᴍ-ʙᴏᴛ](https://github.com/python-telegram-bot/python-telegram-bot)
And using [sǫʟᴀʟᴄʜᴇᴍʏ](https://www.sqlalchemy.org) and [ᴍᴏɴɢᴏ](https://cloud.mongodb.com) as Database.

*Here is the source code that helped developing the bot :* [{BOT_NAME}](https://github.com/PaulSonOfLars/tgbot)


Quickerobot is licensed.
© 2022 - 2023 [sᴜᴘᴘᴏʀᴛ](https://t.me/{SUPPORT_CHAT}) ᴄʜᴀᴛ, ᴀʟʟ ʀɪɢʜᴛs ʀᴇsᴇʀᴠᴇᴅ.
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🏡", callback_data="start_back"),
                        InlineKeyboardButton(text="🛡️", callback_data="ABG_admin"),
                        InlineKeyboardButton(text="💳", callback_data="ABG_credit"),
                        InlineKeyboardButton(text="🧑‍", url=f"tg://user?id={OWNER_ID}"),
                        InlineKeyboardButton(text="🖥️", callback_data="help_back"),
                    ],
                    [
                        InlineKeyboardButton(
                            text="SOURCE",
                            url="https://github.com/PaulSonOfLars/tgbot",  
                        ),
                    ],
                ]
            ),
        )


about_callback_handler = CallbackQueryHandler(
    ABG_about_callback, pattern=r"ABG_", run_async=True
)

source_callback_handler = CallbackQueryHandler(
    Source_about_callback, pattern=r"source_", run_async=True
)


dispatcher.add_handler(about_callback_handler)
dispatcher.add_handler(source_callback_handler)
