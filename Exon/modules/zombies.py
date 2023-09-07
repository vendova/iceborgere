from asyncio import sleep

from telethon import events
from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChannelParticipantsAdmins, ChatBannedRights

from Exon import DEMONS, DEV_USERS, DRAGONS, OWNER_ID, telethn

# =================== CONSTANT ===================

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)


OFFICERS = [OWNER_ID] + DEV_USERS + DRAGONS + DEMONS


# Check if user has admin rights
async def is_administrator(user_id: int, message):
    admin = False
    async for user in telethn.iter_participants(
        message.chat_id, filter=ChannelParticipantsAdmins
    ):
        if user_id == user.id or user_id in OFFICERS:
            admin = True
            break
    return admin


@telethn.on(events.NewMessage(pattern="^[!/]das ?(.*)"))
async def zombies(event):
    """For .zombies command, list all the zombies in a chat."""
    con = event.pattern_match.group(1).lower()
    del_u = 0
    del_status = "No DAs found, group is clean."

    if con != "ban":
        find_zombies = await event.respond("Searching for **Deleted Accounts (DAs)**...")
        async for user in event.client.iter_participants(event.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = f"found **{del_u}** DAs in this group.\
            \nremove them all by using - `/das ban`"
        await find_zombies.edit(del_status)
        return

    # Here laying the sanity check
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not await is_administrator(user_id=event.sender_id, message=event):
        await event.respond("You're Not An Admin!")
        return

    if not admin and not creator:
        await event.respond("I am not admin here!")
        return

    cleaning_zombies = await event.respond("Removing Deleted accounts...")
    del_u = 0
    del_a = 0

    async for user in event.client.iter_participants(event.chat_id):
        if user.deleted:
            try:
                await event.client(
                    EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS)
                )
            except ChatAdminRequiredError:
                await cleaning_zombies.edit("I dont have the ban right in your group!")
                return
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1

    if del_u > 0:
        del_status = f"removed `{del_u}` DAs."

    if del_a > 0:
        del_status = f"removed `{del_u}` Deleted accounts \
        \n`{del_a}` Deleted admin accounts are not removed!"

    await cleaning_zombies.edit(del_status)
