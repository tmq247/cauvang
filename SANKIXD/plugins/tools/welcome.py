#<<<<<<<<<<<<<<SK>>>>>>>>>>>>>>#
#<<<<<<<<<<<<<<Give<Credit<Else>You>Chutiya>>>>>>>>>>>>>>#
import os
from PIL import ImageDraw, Image, ImageFont, ImageChops
from pyrogram import *
from pyrogram.types import *
from logging import getLogger
from SANKIXD import app
from SANKIXD.utils.dbfeds import check_banned_user, get_fed_id

LOGGER = getLogger(__name__)

class WelDatabase:
    def __init__(self):
        self.data = {}

    async def find_one(self, chat_id):
        return chat_id in self.data

    async def add_wlcm(self, chat_id):
        self.data[chat_id] = {}

    async def rm_wlcm(self, chat_id):
        if chat_id in self.data:
            del self.data[chat_id]

wlcm = WelDatabase()

class temp:
    ME = None
    CURRENT = 2
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None



@app.on_chat_member_updated(filters.group, group=-3)
async def greet_group(_, member: ChatMemberUpdated):
    chat = member.chat
    A = await wlcm.find_one(chat.id)
    if (
        not member.new_chat_member
        or member.new_chat_member.status in {"banned", "left", "restricted"}
        or member.old_chat_member
    ):
        return
    user = member.new_chat_member.user if member.new_chat_member else member.from_user
    try:
        fed_id = await get_fed_id(chat.id)
        if fed_id:
            check_user = await check_banned_user(fed_id, member.id)
            if check_user:
                reason = check_user["reason"]
                date = check_user["date"]
                await chat.ban_member(member.id)
                return await app.send_message(
                    chat.id,
                    f"**Người dùng {member.mention} đã bị fban.\n\nLý do: {reason}.\nNgày: {date}.**",
                )
    except ChatAdminRequired:
        return
    if (temp.MELCOW).get(f"welcome-{member.chat.id}") is not None:
        try:
            await temp.MELCOW[f"welcome-{member.chat.id}"].delete()
        except Exception as e:
            LOGGER.error(e)
    
    

@app.on_message(filters.new_chat_members & filters.group, group=-1)
async def bot_wel(_, message):
    for u in message.new_chat_members:
       if u.id == app.me.id:
            await app.send_message(LOG_CHANNEL_ID, f"""
NEW GROUP
╭───── • ◆ • ─────╮
  NAME: {message.chat.title}
  ID: {message.chat.id}
  USERNAME: @{message.chat.username}
╰───── • ◆ • ─────╯
""")
