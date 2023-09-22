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

  

  

from pyrogram.enums import ChatType 

from pyrogram.errors import MessageDeleteForbidden, RPCError 

from pyrogram.types import Message 

  

from Exon import LOGGER, Abishnoi 

  

  

@Abishnoi.on_cmd("purge") 

@Abishnoi.adminsOnly(permissions="can_delete_messages", is_both=True) 

async def purge(c: Abishnoi, m: Message): 

    if m.chat.type != ChatType.SUPERGROUP: 

        await m.reply_text(text="Cannot purge messages in a basic group!") 

        return 

  

    if m.reply_to_message: 

        message_ids = list(range(m.reply_to_message.id, m.id)) 

  

        def divide_chunks(l: list, n: int = 100): 

            for i in range(0, len(l), n): 

                yield l[i : i + n] 

  

        # Dielete messages in chunks of 100 messages 

        m_list = list(divide_chunks(message_ids)) 

  

        try: 

            for plist in m_list: 

                await c.delete_messages( 

                    chat_id=m.chat.id, 

                    message_ids=plist, 

                    revoke=True, 

                ) 

            await m.delete() 

        except MessageDeleteForbidden: 

            await m.reply_text( 

                text="Cannot delete all messages. the messages may be too old, i might not have delete rights, or this might not be a supergroup." 

            ) 

            return 

        except RPCError as ef: 

            LOGGER.info(f"ERROR on purge {ef}") 

  

        count_del_msg = len(message_ids) 

  

        z = await m.reply_text(text=f"DELETED <i>{count_del_msg}</i> messages.") 

        return 

    await m.reply_text("⚠️ No messages selected") 

    return 

  

  

@Abishnoi.on_cmd("spurge") 

@Abishnoi.adminsOnly(permissions="can_delete_messages", is_both=True) 

async def spurge(c: Abishnoi, m: Message): 

    if m.chat.type != ChatType.SUPERGROUP: 

        await m.reply_text(text="Cannot purge messages in a basic group!") 

        return 

  

    if m.reply_to_message: 

        message_ids = list(range(m.reply_to_message.id, m.id)) 

  

        def divide_chunks(l: list, n: int = 100): 

            for i in range(0, len(l), n): 

                yield l[i : i + n] 

  

        # Dielete messages in chunks of 100 messages 

        m_list = list(divide_chunks(message_ids)) 

  

        try: 

            for plist in m_list: 

                await c.delete_messages( 

                    chat_id=m.chat.id, 

                    message_ids=plist, 

                    revoke=True, 

                ) 

            await m.delete() 

        except MessageDeleteForbidden: 

            await m.reply_text( 

                text="Cannot delete all messages. the messages may be too old, i might not have delete rights, or this might not be a supergroup." 

            ) 

            return 

        except RPCError as ef: 

            LOGGER.info(f"ERROR on purge {ef}") 

        return 

    await m.reply_text("Reply to a message to start spurge !") 

    return 

  

  

@Abishnoi.on_cmd("del") 

@Abishnoi.adminsOnly(permissions="can_delete_messages", is_both=True) 

async def del_msg(c: Abishnoi, m: Message): 

    if m.reply_to_message: 

        await m.delete() 

        await c.delete_messages( 

            chat_id=m.chat.id, 

            message_ids=m.reply_to_message.id, 

        ) 

    else: 

        await m.reply_text(text="What do you wanna delete?") 

    return 

  

  

__PLUGIN__ = "PURGE" 

  

__alt_name__ = ["purge", "del", "spurge"] 

  

__HELP__ = """ 

• /purge: Deletes messages upto replied message. 

• /spurge: Deletes messages upto replied message without a success message. 

• /del: Deletes a single message, used as a reply to message. 

""" 
 
