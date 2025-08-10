from pyrogram import Client

import config

from ..logging import LOGGER

assistants = []
assistantids = []

class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="SANKIAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
            #proxy=proxy,
        )
        self.two = Client(
            name="SANKIAss2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
        )
        self.three = Client(
            name="SANKIAss3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
        )
        self.four = Client(
            name="SANKIAss4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
        )
        self.five = Client(
            name="SANKIAss5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
        )

    async def start(self):
        LOGGER(__name__).info(f"Trợ lý khởi động...")
        if config.STRING1:
            await self.one.start()
            try:
                await self.one.join_chat("muoimuoimusicbot")
                await self.one.join_chat("coihaycoc")
            except:
                pass
            assistants.append(1)
            try:
                await self.one.send_message(config.LOGGER_ID, "Trợ lý khởi động")
            except:
                LOGGER(__name__).error(
                    "Tài khoản Trợ lý 1 không truy cập được vào Nhóm nhật ký. Đảm bảo rằng bạn đã thêm trợ lý của mình vào nhóm nhật ký của mình và được thăng chức làm quản trị viên!"
                )
                exit()
            self.one.id = self.one.me.id
            self.one.name = self.one.me.mention
            self.one.username = self.one.me.username
            assistantids.append(self.one.id)
            LOGGER(__name__).info(f"Trợ lý khởi động là {self.one.name}")

        if config.STRING2:
            await self.two.start()
            try:
                await self.one.join_chat("muoimuoimusicbot")
                await self.one.join_chat("coihaycoc")
            except:
                pass
            assistants.append(2)
            try:
                await self.two.send_message(config.LOGGER_ID, "Trợ lý khởi động")
            except:
                LOGGER(__name__).error(
                    "Tài khoản Trợ lý 2 không truy cập được vào Nhóm nhật ký. Đảm bảo rằng bạn đã thêm trợ lý của mình vào nhóm nhật ký của mình và được thăng chức làm quản trị viên!"
                )
                exit()
            self.two.id = self.two.me.id
            self.two.name = self.two.me.mention
            self.two.username = self.two.me.username
            assistantids.append(self.two.id)
            LOGGER(__name__).info(f"Trợ lý khởi động 2 là {self.two.name}")

        if config.STRING3:
            await self.three.start()
            try:
                await self.one.join_chat("muoimuoimusicbot")
                await self.one.join_chat("coihaycoc")
            except:
                pass
            assistants.append(3)
            try:
                await self.three.send_message(config.LOGGER_ID, "Trợ lý khởi động")
            except:
                LOGGER(__name__).error(
                    "Tài khoản Trợ lý 3 không truy cập được vào Nhóm nhật ký. Đảm bảo rằng bạn đã thêm trợ lý của mình vào nhóm nhật ký của mình và được thăng chức làm quản trị viên! "
                )
                exit()
            self.three.id = self.three.me.id
            self.three.name = self.three.me.mention
            self.three.username = self.three.me.username
            assistantids.append(self.three.id)
            LOGGER(__name__).info(f"Trợ lý khởi động 3 là {self.three.name}")

        if config.STRING4:
            await self.four.start()
            try:
                await self.one.join_chat("muoimuoimusicbot")
                await self.one.join_chat("coihaycoc")
            except:
                pass
            assistants.append(4)
            try:
                await self.four.send_message(config.LOGGER_ID, "Trợ lý khởi động")
            except:
                LOGGER(__name__).error(
                    "Tài khoản Trợ lý 4 không truy cập được vào Nhóm nhật ký. Đảm bảo rằng bạn đã thêm trợ lý của mình vào nhóm nhật ký của mình và được thăng chức làm quản trị viên! "
                )
                exit()
            self.four.id = self.four.me.id
            self.four.name = self.four.me.mention
            self.four.username = self.four.me.username
            assistantids.append(self.four.id)
            LOGGER(__name__).info(f"Trợ lý khởi động 4 là {self.four.name}")

        if config.STRING5:
            await self.five.start()
            try:
                await self.one.join_chat("muoimuoimusicbot")
                await self.one.join_chat("coihaycoc")
            except:
                pass
            assistants.append(5)
            try:
                await self.five.send_message(config.LOGGER_ID, "Trợ lý khởi động")
            except:
                LOGGER(__name__).error(
                    "Tài khoản Trợ lý 5 không truy cập được vào Nhóm nhật ký. Đảm bảo rằng bạn đã thêm trợ lý của mình vào nhóm nhật ký của mình và được thăng chức làm quản trị viên! "
                )
                exit()
            self.five.id = self.five.me.id
            self.five.name = self.five.me.mention
            self.five.username = self.five.me.username
            assistantids.append(self.five.id)
            LOGGER(__name__).info(f"Trợ lý khởi động 5 là {self.five.name}")

    async def get_me(self):
        # Đảm bảo rằng ít nhất một trợ lý đã start
        if config.STRING1 and self.one.is_connected:
            return await self.one.get_me()
        elif config.STRING2 and self.two.is_connected:
            return await self.two.get_me()
        elif config.STRING3 and self.three.is_connected:
            return await self.three.get_me()
        elif config.STRING4 and self.four.is_connected:
            return await self.four.get_me()
        elif config.STRING5 and self.five.is_connected:
            return await self.five.get_me()
        else:
            raise RuntimeError("Chưa có trợ lý nào được kết nối. Hãy gọi await start() trước.")

    async def stop(self):
        LOGGER(__name__).info(f"Dừng trợ lý...")
        try:
            if config.STRING1:
                await self.one.stop()
            if config.STRING2:
                await self.two.stop()
            if config.STRING3:
                await self.three.stop()
            if config.STRING4:
                await self.four.stop()
            if config.STRING5:
                await self.five.stop()
        except:
            pass


