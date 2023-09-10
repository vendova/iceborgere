from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
import os

mongo = MongoCli("mongodb+srv://mogenius:mogenius@quickers.rlx3b3f.mongodb.net/?retryWrites=true&w=majority")
db = mongo.Exon

coupledb = db.couple
nsfwdb = db.nsfw


async def _get_lovers(chat_id: int):
    lovers = await coupledb.find_one({"chat_id": chat_id})
    if lovers:
        lovers = lovers["couple"]
    else:
        lovers = {}
    return lovers


async def get_couple(chat_id: int, date: str):
    lovers = await _get_lovers(chat_id)
    if date in lovers:
        return lovers[date]
    else:
        return False


async def save_couple(chat_id: int, date: str, couple: dict):
    lovers = await _get_lovers(chat_id)
    lovers[date] = couple
    await coupledb.update_one(
        {"chat_id": chat_id},
        {"$set": {"couple": lovers}},
        upsert=True,
    )

async def is_nsfw_on(chat_id: int) -> bool:
    chat = await nsfwdb.find_one({"chat_id": chat_id})
    if not chat:
        return True
    return False


async def nsfw_on(chat_id: int):
    is_nsfw = await is_nsfw_on(chat_id)
    if is_nsfw:
        return
    return await nsfwdb.delete_one({"chat_id": chat_id})


async def nsfw_off(chat_id: int):
    is_nsfw = await is_nsfw_on(chat_id)
    if not is_nsfw:
        return
    return await nsfwdb.insert_one({"chat_id": chat_id})
