
import asyncio
import uuid
import html

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus, ChatType, ParseMode
from pyrogram.errors import FloodWait, PeerIdInvalid, ChatAdminRequired, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.types import (
    CallbackQuery,
    ChatMemberUpdated,
    ChatPermissions,
    ChatPrivileges,
    Message,
)
from config import LOGGER_ID as LOG_GROUP_ID
from SANKIXD.misc import SUDOERS

from SANKIXD import userbot as us, app
from SANKIXD.core.userbot import assistants
from SANKIXD.utils.errors import capture_err
from SANKIXD.utils.dbfeds import *
from SANKIXD.utils.functions import extract_user, extract_user_and_reason

__MODULE__ = "Federation"
__HELP__ = """
Mọi thứ đều vui vẻ, cho đến khi một kẻ gửi thư rác bắt đầu xâm nhập vào nhóm của bạn và bạn phải chặn hắn. Sau đó, bạn cần bắt đầu cấm nhiều hơn, nhiều hơn nữa và điều đó thật đau đớn.
Nhưng sau đó, bạn có nhiều nhóm và bạn không muốn kẻ gửi thư rác này ở trong một trong các nhóm của mình - bạn có thể xử lý như thế nào? Bạn có phải chặn thủ công trong tất cả các nhóm của mình không?\n
**Không còn nữa!** Với Liên kết, bạn có thể thực hiện lệnh cấm trong một cuộc trò chuyện chồng chéo với tất cả các cuộc trò chuyện khác.\n
Bạn thậm chí có thể chỉ định quản trị viên liên kết, để quản trị viên đáng tin cậy của bạn có thể cấm tất cả những kẻ gửi thư rác khỏi các cuộc trò chuyện mà bạn muốn bảo vệ.\n\n
"""

SUPPORT_CHAT = "@muoimuoimusicbot"
#BOT_ID = me.id

@app.on_message(filters.command("newfed"))
@capture_err
async def new_fed(client, message):
    chat = message.chat
    user = message.from_user
    if message.chat.type != ChatType.PRIVATE:
        return await message.reply_text(
            "Chỉ có thể tạo liên đoàn bằng cách nhắn tin riêng cho tôi."
        )

    if len(message.command) < 2:
        return await message.reply_text("Hãy nhập tên liên đoàn!")

    fednam = message.text.split(None, 1)[1]
    if not fednam == "":
        fed_id = f"{user.id}:{uuid.uuid4()}"
        fed_name = fednam
        x = await fedsdb.update_one(
            {"fed_id": str(fed_id)},
            {
                "$set": {
                    "fed_name": str(fed_name),
                    "owner_id": int(user.id),
                    "fadmins": [],
                    "owner_mention": user.mention,
                    "banned_users": [],
                    "chat_ids": [],
                    "log_group_id": LOG_GROUP_ID,
                }
            },
            upsert=True,
        )
        if not x:
            return await message.reply_text(
                f"Không thể liên kết!Vui lòng liên hệ {SUPPORT_CHAT} nếu vấn đề vẫn tiếp diễn."
            )

        await message.reply_text(
            "**Bạn đã thành công trong việc tạo ra một liên đoàn mới!**"
            "\nTên: `{}`"
            "\nID: `{}`"
            "\n\nSử dụng lệnh bên dưới để tham gia liên đoàn:"
            "\n`/joinfed {}`".format(fed_name, fed_id, fed_id),
            parse_mode=ParseMode.MARKDOWN,
        )
        try:
            await app.send_message(
                LOG_GROUP_ID,
                "Liên đoàn mới: <b>{}</b>\nID: <pre>{}</pre>".format(
                    fed_name, fed_id
                ),
                parse_mode=ParseMode.HTML,
            )
        except:
            log.info("Không thể gửi tin nhắn đến EVENT_LOGS")
    else:
        await message.reply_text(
            "Xin hãy nhập tên của liên đoàn"
        )


@app.on_message(filters.command("delfed"))
@capture_err
async def del_fed(client, message):
    chat = message.chat
    user = message.from_user
    if message.chat.type != ChatType.PRIVATE:
        return await message.reply_text(
            "Liên đoàn chỉ có thể bị xóa bằng cách nhắn tin riêng cho tôi."
        )

    args = message.text.split(" ", 1)
    if len(args) > 1:
        is_fed_id = args[1].strip()
        getinfo = await get_fed_info(is_fed_id)
        if getinfo is False:
            return await message.reply_text("Liên đoàn này không tồn tại.")

        if getinfo["owner_id"] == user.id or user.id == SUDOERS:
            fed_id = is_fed_id
        else:
            return await message.reply_text("Chỉ có chủ sở hữu liên đoàn mới có thể làm điều này!")

    else:
        return await message.reply_text("Tôi nên xóa những gì?")

    is_owner = await is_user_fed_owner(fed_id, user.id)
    if is_owner is False:
        return await message.reply_text("Chỉ có chủ sở hữu liên đoàn mới có thể làm điều này!")

    await message.reply_text(
        "Bạn chắc chắn muốn xóa liên đoàn của mình? Điều này không thể hoàn nguyên, bạn sẽ mất toàn bộ danh sách cấm và '{}' sẽ bị mất vĩnh viễn.".format(
            getinfo["fed_name"]
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⚠️ Xóa Liên Đoàn ⚠️",
                        callback_data=f"rmfed_{fed_id}",
                    )
                ],
                [InlineKeyboardButton("Hủy", callback_data="rmfed_cancel")],
            ]
        ),
    )


@app.on_message(filters.command("fedtransfer"))
@capture_err
async def fedtransfer(client, message):
    chat = message.chat
    user = message.from_user
    if message.chat.type != ChatType.PRIVATE:
        return await message.reply_text(
            "Liên đoàn chỉ có thể được chuyển nhượng bằng cách nhắn tin riêng cho tôi."
        )

    is_feds = await get_feds_by_owner(int(user.id))
    if not is_feds:
        return await message.reply_text(
            "**Bạn chưa tạo bất kỳ liên đoàn nào.**"
        )
    if len(message.command) < 2:
        return await message.reply_text(
            "**Bạn cần phải chỉ định người dùng hoặc trả lời tin nhắn của họ!**"
        )
    user_id, fed_id = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text("Tôi không thể tìm thấy người dùng đó.")
    if not fed_id:
        return await message.reply(
            "bạn cần cung cấp 1 ID liên đoàn.\n\nUsage:\n/fedtransfer @usename ID_liên đoàn."
        )
    is_owner = await is_user_fed_owner(fed_id, user.id)
    if is_owner is False:
        return await message.reply_text("Chỉ có chủ sở hữu liên đoàn mới có thể làm điều này!")

    await message.reply_text(
        "**Bạn chắc chắn muốn chuyển nhượng liên đoàn của bạn? Điều này không thể hoàn nguyên.**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⚠️ Chuyển nhượng Liên Đoàn⚠️",
                        callback_data=f"trfed_{user_id}|{fed_id}",
                    )
                ],
                [InlineKeyboardButton("Hủy", callback_data="trfed_cancel")],
            ]
        ),
    )


@app.on_message(filters.command("myfeds"))
@capture_err
async def myfeds(client, message):
    user = message.from_user
    is_feds = await get_feds_by_owner(int(user.id))

    if is_feds:
        response_text = "\n\n".join(
            [
                f"{i + 1}) **Tên liên đoàn:** {fed['fed_name']}\n  **Fed Id:** `{fed['fed_id']}`"
                for i, fed in enumerate(is_feds)
            ]
        )
        await message.reply_text(
            f"**Đây là các liên đoàn bạn đã tạo:**\n\n{response_text}"
        )
    else:
        await message.reply_text("**Bạn chưa tạo bất kỳ liên đoàn nào.**")


@app.on_message(filters.command("renamefed"))
@capture_err
async def rename_fed(client, message):
    user = message.from_user
    msg = message
    args = msg.text.split(None, 2)

    if len(args) < 3:
        return await msg.reply_text("usage: /renamefed ID_liên đoàn TÊN MỚI")

    fed_id, newname = args[1], args[2]
    verify_fed = await get_fed_info(fed_id)

    if not verify_fed:
        return await msg.reply_text("Liên đoàn này không tồn tại trong cơ sở dữ liệu của tôi!")

    if await is_user_fed_owner(fed_id, user.id):
        fedsdb.update_one(
            {"fed_id": str(fed_id)},
            {"$set": {"fed_name": str(newname), "owner_id": int(user.id)}},
            upsert=True,
        )
        await msg.reply_text(
            f"Đã đổi tên liên đoàn của bạn thành công {newname}!"
        )
    else:
        await msg.reply_text("Chỉ có chủ sở hữu liên đoàn mới có thể làm điều này!")


@app.on_message(filters.command(["setfedlog", "unsetfedlog"]))
@capture_err
async def fed_log(client, message):
    chat = message.chat
    user = message.from_user
    if message.chat.type == ChatType.PRIVATE:
        if len(message.command) < 3:
            return await message.reply_text(
                f"Cách dùng:\n\n /{message.command[0]} [ID_kênh] [ID_liên đoàn]."
            )
        ids = message.text.split(" ", 2)
        chat_id = ids[1]
        fed_id = ids[2]
        try:
            await app.get_chat(chat_id)
        except Exception as e:
            return await message.reply_text(e)

    else:
        chat_id = chat.id 
        if len(message.command) < 2:
            return await message.reply_text(
                "Vui lòng cung cấp ID của liên đoàn cùng với lệnh!"
            )
        fed_id = message.text.split(" ", 1)[1].strip()

    try:
        chat_member = await app.get_chat_member(chat_id, user.id)
        
    except ChatAdminRequired:
        return await message.reply_text("Tôi cần phải là người quản trị kênh")
        
    except Exception as e:
        print(e)
        return
        
    if not chat_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return await message.reply_text(
            "Bạn cần phải là chủ sở hữu hoặc quản trị viên kênh để sử dụng lệnh này"
        )

    info = await get_fed_info(fed_id)
    if info is False:
        return await message.reply_text("Liên đoàn này không tồn tại.")

    if await is_user_fed_owner(fed_id, user.id):
        if "/unsetfedlog" in message.text:
            log_group_id = LOG_GROUP_ID
        else:
            log_group_id = chat_id
        loged = await set_log_chat(fed_id, log_group_id)
        if "/unsetfedlog" in message.text:
            return await message.reply_text(
                "Kênh nhật ký đã được xóa thành công."
            )
        else:
            await message.reply_text("Kênh nhật ký đã được thiết lập thành công.")


@app.on_message(filters.command("chatfed"))
@capture_err
async def fed_chat(client, message):
    chat = message.chat
    user = message.from_user
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(
            "Lệnh này dùng riêng cho nhóm, không phải trong tin nhắn riêng tư của tôi!",
        )

    fed_id = await get_fed_id(chat.id)

    member = await app.get_chat_member(chat.id, user.id)
    if (
        member.status == ChatMemberStatus.OWNER
        or member.status == ChatMemberStatus.ADMINISTRATOR
    ):
        pass
    else:
        return await message.reply_text(
            "Bạn phải là quản trị viên để thực hiện lệnh này"
        )

    if not fed_id:
        return await message.reply_text("Nhóm này không thuộc bất kỳ liên đoàn nào!")

    info = await get_fed_info(fed_id)

    text = "Nhóm này là một phần của liên đoàn sau:"
    text += "\n{} (ID: <code>{}</code>)".format(info["fed_name"], fed_id)

    await message.reply_text(text, parse_mode=ParseMode.HTML)


@app.on_message(filters.command("joinfed"))
@capture_err
async def join_fed(client, message):
    chat = message.chat
    user = message.from_user
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(
            "Lệnh này dùng trong nhóm, không phải trong tin nhắn riêng của tôi!",
        )

    member = await app.get_chat_member(chat.id, user.id)
    fed_id = await get_fed_id(int(chat.id))

    if user.id in SUDOERS:
        pass
    else:
        if member.status == ChatMemberStatus.OWNER or ChatMemberStatus.ADMINISTRATOR:
            required_permissions = [
            member.privileges.can_change_info,
            member.privileges.can_delete_messages,
            member.privileges.can_invite_users,
            member.privileges.can_restrict_members,
            member.privileges.can_pin_messages,
            member.privileges.can_promote_members,
            member.privileges.can_manage_chat,
            member.privileges.can_manage_video_chats,
        ]
            if not all(required_permissions):
                return await message.reply_text("Bạn cần có tất cả các quyền quản trị viên trong nhóm để sử dụng lệnh này!")
            pass
        else:
            return await message.reply_text(
                "Chỉ những người tạo nhóm mới có thể sử dụng lệnh này!"
            )

    if fed_id:
        return await message.reply_text(
            "Bạn không thể tham gia hai liên đoàn từ một cuộc trò chuyện"
        )

    args = message.text.split(" ", 1)
    if len(args) > 1:
        fed_id = args[1].strip()
        getfed = await search_fed_by_id(fed_id)
        if getfed is False:
            return await message.reply_text("Vui lòng nhập ID liên đoàn hợp lệ")
 

        x = await chat_join_fed(fed_id, chat.title, chat.id)
        if not x:
            return await message.reply_text(
                f"Không thể tham gia liên đoàn! Vui lòng liên hệ {SUPPORT_CHAT} nếu vấn đề này vẫn tiếp diễn!"
            )

        get_fedlog = getfed["log_group_id"]
        if get_fedlog:
            await app.send_message(
                get_fedlog,
                "Nhóm **{}** đã tham gia liên đoàn **{}**".format(
                    chat.title, getfed["fed_name"]
                ),
                parse_mode=ParseMode.MARKDOWN,
            )

        await message.reply_text(
            "Nhóm này đã gia nhập liên đoàn: {}!".format(
                getfed["fed_name"]
            )
        )
    else:
        await message.reply_text(
            "Bạn cần chỉ rõ liên đoàn nào bạn đang nhắc đến bằng cách cung cấp cho tôi ID_liên đoàn!"
        )


@app.on_message(filters.command("leavefed"))
@capture_err
async def leave_fed(client, message):
    chat = message.chat
    user = message.from_user

    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(
            "Lệnh này dùng trong nhóm, không phải trong tin nhắn riêng của tôi!",
        )

    fed_id = await get_fed_id(int(chat.id))
    fed_info = await get_fed_info(fed_id)

    member = await app.get_chat_member(chat.id, user.id)
    if member.status == ChatMemberStatus.OWNER or user.id in SUDOERS:
        if await chat_leave_fed(int(chat.id)) is True:
            get_fedlog = fed_info["log_group_id"]
            if get_fedlog:
                await app.send_message(
                    get_fedlog,
                    "Nhóm **{}** đã rời khỏi liên đoàn **{}**".format(
                        chat.title, fed_info["fed_name"]
                    ),
                    parse_mode=ParseMode.MARKDOWN,
                )
            await message.reply_text(
                "Nhóm này đã rời khỏi liên đoàn {}!".format(
                    fed_info["fed_name"]
                ),
            )
        else:
            await message.reply_text(
                "Làm sao bạn có thể rời khỏi một liên đoàn mà bạn chưa từng tham gia?!"
            )
    else:
        await message.reply_text("Chỉ người tạo nhóm mới có thể sử dụng lệnh này!")


@app.on_message(filters.command("fedchats"))
@capture_err
async def fed_chat(client, message):
    chat = message.chat
    user = message.from_user
    me = await app.get_me()
    BOT_ID = me.id
    if message.chat.type != ChatType.PRIVATE:
        return await message.reply_text(
            "Danh sách nhóm thuộc liên đoàn chỉ có thể được kiểm tra bằng cách nhắn tin riêng cho tôi."
        )
    if len(message.command) < 2:
        return await message.reply_text(
            "Vui lòng ghi ID của liên đoàn!\n\nUsage:\n/fedchats ID_liên đoàn"
        )
    args = message.text.split(" ", 1)
    if len(args) > 1:
        fed_id = args[1].strip()
        info = await get_fed_info(fed_id)
        if info is False:
            return await message.reply_text("Liên đoàn này không tồn tại.")
        fed_owner = info["owner_id"]
        fed_admins = info["fadmins"]
        all_admins = [fed_owner] + fed_admins + [int(BOT_ID)]
        if user.id in all_admins or user.id in SUDOERS:
            pass
        else:
            return await message.reply_text(
                "Bạn cần phải là Admin liên đoàn để sử dụng lệnh này"
            )

        chat_ids, chat_names = await chat_id_and_names_in_fed(fed_id)
        if not chat_ids:
            return await message.reply_text(
                "Không có cuộc trò chuyện nào trong liên đoàn này!"
            )
        text = "\n".join(
            [
                f"$ {chat_name} [`{chat_id}`]"
                for chat_id, chat_name in zip(chat_ids, chat_names)
            ]
        )
        await message.reply_text(
            f"**Sau đây là danh sách các nhóm được kết nối với liên đoàn này:**\n\n{text}"
        )


@app.on_message(filters.command("fedinfo"))
@capture_err
async def fed_info(client, message):
    if len(message.command) < 2:
        fed_id = await get_fed_id(message.chat.id)
        if not fed_id:
            return await message.reply_text("Vui lòng cung cấp ID_liên đoàn để biết thông tin!")
    else:
        fed_id = message.text.split(" ", 1)[1].strip()
    fed_info = await get_fed_info(fed_id)

    if not fed_info:
        return await message.reply_text("Không tìm thấy liên đoàn.")

    fed_name = fed_info.get("fed_name")
    owner_mention = fed_info.get("owner_mention")
    fadmin_count = len(fed_info.get("fadmins", []))
    banned_users_count = len(fed_info.get("banned_users", []))
    chat_ids_count = len(fed_info.get("chat_ids", []))

    reply_text = (
        f"**Thông tin liên đoàn:**\n\n"
        f"**Tên liên đoàn:** {fed_name}\n"
        f"**Người sở hữu:** {owner_mention}\n"
        f"**Số lượng quản trị viên liên đoàn:** {fadmin_count}\n"
        f"**Số lượng người dùng bị cấm:** {banned_users_count}\n"
        f"**Số lượng nhóm:** {chat_ids_count}"
    )

    await message.reply_text(reply_text)


@app.on_message(filters.command("fedadmins"))
@capture_err
async def get_all_fadmins_mentions(client, message):
    if len(message.command) < 2:
        fed_id = await get_fed_id(message.chat.id)
        if not fed_id:
            return await message.reply_text("Vui lòng cung cấp cho tôi ID liên đoàn để tìm kiếm!")
    else:
        fed_id = message.text.split(" ", 1)[1].strip()
    fed_info = await get_fed_info(fed_id)
    if not fed_info:
        return await message.reply_text("Không tìm thấy liên đoàn.")

    fadmin_ids = fed_info.get("fadmins", [])
    if not fadmin_ids:
        return await message.reply_text(
            f"**Chủ sở hữu: {fed_info['owner_mention']}\n\nKhông tìm thấy danh sách Admin liên đoàn trong liên đoàn."
        )

    user_mentions = []
    for user_id in fadmin_ids:
        try:
            user = await app.get_users(int(user_id))
            user_mentions.append(f"● {user.mention}[`{user.id}`]")
        except Exception:
            user_mentions.append(f"● `Admin🥷`[`{user_id}`]")
    reply_text = (
        f"**Chủ sở hữu: {fed_info['owner_mention']}\n\nDanh sách Admin liên đoàn:**\n"
        + "\n".join(user_mentions)
    )

    await message.reply_text(reply_text)


@app.on_message(filters.command("fpromote"))
@capture_err
async def fpromote(client, message):
    chat = message.chat
    user = message.from_user
    msg = message

    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(
            "Lệnh này dùng trong nhóm, không phải trong tin nhắn riêng của tôi!",
        )

    fed_id = await get_fed_id(chat.id)
    if not fed_id:
        return await message.reply_text(
            "Trước tiên, bạn cần thêm liên đoàn vào nhóm này!"
        )

    if await is_user_fed_owner(fed_id, user.id) or user.id in SUDOERS:
        user_id = await extract_user(msg)

        if user_id is None:
            return await message.reply_text(
                "Không thể trích xuất người dùng từ tin nhắn."
            )

        check_user = await check_banned_user(fed_id, user_id)
        if check_user:
            user = await app.get_users(user_id)
            reason = check_user["reason"]
            date = check_user["date"]
            return await message.reply_text(
                f"**Người dùng {user.mention} đã bị cấm trong Liên Đoàn.\nbạn có thể bỏ lệnh cấm người dùng và thăng chức.\n\nLý do: {reason}.\nNgày: {date}.**"
            )

        getuser = await search_user_in_fed(fed_id, user_id)
        info = await get_fed_info(fed_id)
        get_owner = info["owner_id"]

        if user_id == get_owner:
            return await message.reply_text(
                "Bạn biết rằng người dùng này là chủ sở hữu liên đoàn, đúng không?"
            )

        if getuser:
            return await message.reply_text(
                "Tôi không thể thăng chức cho những người dùng đã là quản trị viên liên đoàn! Bạn có thể xóa họ nếu muốn!"
            )

        if user_id == BOT_ID:
            return await message.reply_text(
                "Tôi đã là quản trị viên liên đoàn trong tất cả các liên đoàn!"
            )

        res = await user_join_fed(str(fed_id), user_id)
        if res:
            await message.reply_text("Đã được thăng chức thành công!")
        else:
            await message.reply_text("Không thể thăng chức!")
    else:
        await message.reply_text("Chỉ có chủ sở hữu liên đoàn mới có thể làm điều này!")


@app.on_message(filters.command("fdemote"))
@capture_err
async def fdemote(client, message):
    chat = message.chat
    user = message.from_user
    msg = message

    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(
            "Lệnh này dùng trong nhóm, không phải trong tin nhắn riêng của tôi!",
        )

    fed_id = await get_fed_id(chat.id)
    if not fed_id:
        return await message.reply_text(
            "Trước tiên, bạn cần thêm liên đoàn vào cuộc trò chuyện này!"
        )

    if await is_user_fed_owner(fed_id, user.id) or user.id in SUDOERS:
        user_id = await extract_user(msg)

        if user_id is None:
            return await message.reply_text(
                "Không thể trích xuất người dùng từ tin nhắn."
            )

        if user_id == BOT_ID:
            return await message.reply_text(
                "Mày điên à! Tau là TRÙM."
            )

        if await search_user_in_fed(fed_id, user_id) is False:
            return await message.reply_text(
                "Tôi không thể hạ cấp những người không phải là quản trị viên liên đoàn!"
            )

        res = await user_demote_fed(fed_id, user_id)
        if res is True:
            await message.reply_text("Đã giáng chức Quản trị viên Liên Đoàn!")
        else:
            await message.reply_text("Việc giáng chức đã thất bại!")
    else:
        return await message.reply_text("Chỉ có chủ sở hữu liên đoàn mới có thể làm điều này!")


@app.on_message(filters.command(["fban", "sfban"]))
@capture_err
async def fban_user(client, message):
    chat = message.chat
    from_user = message.from_user
    me = await app.get_me()
    BOT_ID = me.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(
            "Lệnh này dùng trong nhóm, không phải trong tin nhắn riêng của tôi!."
        )

    fed_id = await get_fed_id(chat.id)
    if not fed_id:
        return await message.reply_text(
            "**Cuộc trò chuyện này không thuộc bất kỳ liên đoàn nào."
        )
    info = await get_fed_info(fed_id)
    fed_owner = info["owner_id"]
    fed_admins = info["fadmins"]
    all_admins = [fed_owner] + fed_admins + [int(BOT_ID)]
    if from_user.id in all_admins or from_user.id in SUDOERS:
        pass
    else:
        return await message.reply_text(
            "Bạn cần phải là Admin liên đoàn để sử dụng lệnh này"
        )
    """if len(message.command) < 2:
        return await message.reply_text(
            "**Bạn cần chỉ định người dùng hoặc trả lời tin nhắn của họ!**"
        )"""
    user_id, reason = await extract_user_and_reason(message)
    try:
        user = await app.get_users(user_id)
    except PeerIdInvalid:
        return await message.reply_msg("Xin lỗi, tôi chưa từng gặp người dùng này.")
    if not user_id:
        return await message.reply_text("Tôi không thể tìm thấy người dùng đó.")
    if user_id in all_admins or user_id in SUDOERS:
        return await message.reply_text("Tôi không thể cấm người dùng đó.")
    check_user = await check_banned_user(fed_id, user_id)
    if check_user:
        reason = check_user["reason"]
        date = check_user["date"]
        return await message.reply_text(
            f"**Người dùng {user.mention} đã bị Cấm trong liên đoàn.\n\nLý do: {reason}.\nNgày: {date}.**"
        )
    if not reason:
        return await message.reply("Không có lý do nào được cung cấp.")

    served_chats, _ = await chat_id_and_names_in_fed(fed_id)
    m = await message.reply_text(
        f"**Fed Banning {user.mention}!**"
        + f" **Hành động này sẽ mất khoảng {len(served_chats)} giây.**"
    )
    await add_fban_user(fed_id, user_id, reason)
    number_of_chats = 0
    for served_chat in served_chats:
        try:
            chat_member = await app.get_chat_member(served_chat, user.id)
            if chat_member.status == ChatMemberStatus.MEMBER:
                await app.ban_chat_member(served_chat, user.id)
                if served_chat != chat.id:
                    if not message.text.startswith("/s"):
                        await app.send_message(
                            served_chat, f"**Bị cấm trong liên đoàn :{user.mention} !**"
                        )
                number_of_chats += 1
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(int(e.value))
        except Exception:
            pass
    try:
        await app.send_message(
            user.id,
            f"Xin chào, Bạn đã bị cấm bởi {from_user.mention},"
            + " Bạn có thể kháng cáo lệnh cấm này bằng cách nói chuyện với họ.",
        )
    except Exception:
        pass
    await m.edit(f"Đã cấm trong liên đoàn: {user.mention} !")
    ban_text = f"""
__**Lệnh cấm liên đoàn mới**__
**Nguồn gốc:** {message.chat.title} [`{message.chat.id}`]
**Quản trị viên:** {from_user.mention}
**Người dùng bị cấm:** {user.mention}
**ID người dùng bị cấm:** `{user_id}`
**Lý do:** __{reason}__
**Số lượng nhóm:** `{number_of_chats}`"""
    try:
        m2 = await app.send_message(
            info["log_group_id"],
            text=ban_text,
            disable_web_page_preview=True,
        )
        await m.edit(
            f"Lệnh cấm liên đoàn {user.mention} !\nNhật ký hành động: {m2.link}",
            disable_web_page_preview=True,
        )
    except Exception:
        await message.reply_text(
            "Người dùng bị Fbanned, nhưng hành động Fban này không được ghi lại, hãy thêm tôi vào LOG_GROUP"
        )


#fdelete

@app.on_message(filters.command("fdel"))
@capture_err
async def fdel(client, message):
    chat = message.chat
    from_user = message.from_user
    me = await app.get_me()
    BOT_ID = me.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(
            "Lệnh này dùng trong nhóm, không phải trong tin nhắn riêng của tôi!."
        )

    fed_id = await get_fed_id(chat.id)
    if not fed_id:
        return await message.reply_text(
            "**Cuộc trò chuyện này không thuộc bất kỳ liên đoàn nào."
        )
    info = await get_fed_info(fed_id)
    fed_owner = info["owner_id"]
    fed_admins = info["fadmins"]
    all_admins = [fed_owner] + fed_admins + [int(BOT_ID)]
    if from_user.id in all_admins or from_user.id in SUDOERS:
        pass
    else:
        return await message.reply_text(
            "Bạn cần phải là Admin liên đoàn để sử dụng lệnh này"
        )
    """if len(message.command) < 2:
        return await message.reply_text(
            "**Bạn cần chỉ định người dùng hoặc trả lời tin nhắn của họ!**"
        )"""
    user_id = await extract_user(message)
    try:
        user = await app.get_users(user_id)
    except PeerIdInvalid:
        return await message.reply_msg("Xin lỗi, tôi chưa từng gặp người dùng này.")
    if not user_id:
        return await message.reply_text("Tôi không thể tìm thấy người dùng đó.")
    if user_id in SUDOERS:
        return await message.reply_text("Tôi không thể xóa tin nhắn người dùng đó.")

    served_chats, _ = await chat_id_and_names_in_fed(fed_id)
    m = await message.reply_text(
        f"**Loading!**"
        + f" **Hành động này sẽ mất khoảng {len(served_chats)} giây.**"
    )
    number_of_chats = 0
    if 1 in assistants:
        ubot = us.one
    app2 = await ubot.get_me()
    user1 = await ubot.get_users(user.id)
    for served_chat in served_chats:
        try:
            try:
                chat_member = await app.get_chat_member(served_chat, user.id)
                chat_member = await ubot.get_chat_member(served_chat, user1.id)
            except UserNotParticipant:
                continue
            #if chat_member.status == ChatMemberStatus.MEMBER:
            admin = await app.get_chat_member(served_chat, app2.id)
            if admin.status != ChatMemberStatus.ADMINISTRATOR:
                return await app.send_message(served_chat, "userbot không có quyền qtv trong nhóm này.")
            checkadmin = admin.privileges.can_delete_messages
            if not checkadmin:
                return await app.send_message(served_chat, "userbot không có quyền xóa tin nhắn người dùng này.")
            await ubot.delete_user_history(served_chat, user1.id)
            number_of_chats += 1
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(int(e.value))
        except Exception as y_e:
            print(y_e)
            return await app.send_message(chat.id, "Lỗi")
    await m.edit(f"Đã xóa tin nhắn trong liên đoàn: {user.mention} !")
    try:
        await m.edit(
            f"Đã xóa tin nhắn {user.mention} trong liên đoàn !",
            disable_web_page_preview=True,
        )
    except Exception:
        await message.reply_text(
            "Người dùng bị Fdel, nhưng hành động Fdel này không được ghi lại, hãy thêm tôi vào LOG_GROUP"
        )
    await asyncio.sleep(10)
    await app.delete_messages(message.chat.id, m.id, revoke=True,)

#Fmute

@app.on_message(filters.command(["fmute", "sfmute", "checkvoice"]) & ~filters.private)
@capture_err
async def fmute_user(client, message):
    chat = message.chat
    from_user = message.from_user
    me = await app.get_me()
    BOT_ID = me.id
    link2 = f"tg://openmessage?user_id="
    link = f"t.me/"
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(
            "Lệnh này dùng trong nhóm, không phải trong tin nhắn riêng của tôi!."
        )

    fed_id = await get_fed_id(chat.id)
    if not fed_id:
        return await message.reply_text(
            "**Cuộc trò chuyện này không thuộc bất kỳ liên đoàn nào."
        )
    info = await get_fed_info(fed_id)
    fed_owner = info["owner_id"]
    fed_admins = info["fadmins"]
    all_admins = [fed_owner] + fed_admins + [int(BOT_ID)]
    if from_user.id in all_admins or from_user.id in SUDOERS:
        pass
    else:
        return await message.reply_text(
            "Bạn cần phải là Admin liên đoàn để sử dụng lệnh này"
        )
    """if len(message.command) < 2:
        return await message.reply_text(
            "**Bạn cần chỉ định người dùng hoặc trả lời tin nhắn của họ!**"
        )"""
    user_id, reason = await extract_user_and_reason(message)
    try:
        user = await app.get_users(user_id)
    except PeerIdInvalid:
        return await message.reply_msg("Xin lỗi, tôi chưa từng gặp người dùng này.")
    if not user_id:
        return await message.reply_text("Tôi không thể tìm thấy người dùng đó.")
    if user_id in all_admins or user_id in SUDOERS:
        return await message.reply_text("Tôi không thể cấm chat người dùng đó.")
    check_user = await check_banned_user(fed_id, user_id)
    if check_user:
        reason = check_user["reason"]
        date = check_user["date"]
        return await message.reply_text(
            f"**Người dùng {user.mention} đã bị Cấm trong liên đoàn.\n\nLý do: {reason}.\nNgày: {date}.**"
        )
    check_user1 = await check_muted_user(fed_id, user_id)
    if check_user1:
        reason = check_user1["reason"]
        date = check_user1["date"]
        return await message.reply_text(
            f"**Người dùng {user.mention} đã bị Cấm chat trong liên đoàn.\n\nLý do: {reason}.\nNgày: {date}.**"
        )
    check_user2 = await check_actived_user(fed_id, user_id)
    if message.command[0] == "checkvoice":
        if check_user2:
            reason = check_user2["reason"]
            date = check_user2["date"]
            return await message.reply_text(
                f"**Người dùng {user.mention} đã được xác thực trong liên đoàn.\n\nNote: {reason}.\nNgày: {date}.**"
            )
    #if not reason:
        #return await message.reply("Không có lý do nào được cung cấp.")

    served_chats, _ = await chat_id_and_names_in_fed(fed_id)
    m = await message.reply_text(
        f"**Loading {user.mention}!**"
        + f" **Hành động này sẽ mất khoảng {len(served_chats)} giây.**"
    )
    await add_fmute_user(fed_id, user_id, reason)
    number_of_chats = 0
    for served_chat in served_chats:
        try:
            chat_member = await app.get_chat_member(served_chat, user.id)
            if chat_member.status == ChatMemberStatus.MEMBER:
                await app.restrict_chat_member(served_chat, user.id, permissions=ChatPermissions())
                if served_chat != chat.id:
                    if not message.text.startswith("/s"):
                        await app.send_message(
                            served_chat, f"**Done.**"
                        )
                number_of_chats += 1
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(int(e.value))
        except Exception:
            pass
    username1 = from_user.username
    username2 = user.username 
    if message.command[0][0] == "f":
        try:
            await app.send_message(user.id, f"Xin chào {user.mention}, bạn đã bị cấm chat tại nhóm {message.chat.title} với lý do: {reason}, bạn hãy nhắn tin cho admin {from_user.mention} t.me/{username1} để mở chat.")
        except Exception:
            pass
        await m.edit(f"Đã cấm chat {user.mention} trong liên đoàn!")
        mute_text = f"""
    __**Người dùng bị fmute toàn hệ thống **__
    **Tại nhóm:** {message.chat.title} [`{message.chat.id}`]
    **Quản trị viên:** {from_user.mention} @{username1}
    **Người dùng bị cấm chat:** {user.mention} @{username2} **ID:** `{user_id}`
    **Lý do:** __{reason}__
    **Lúc:** __{timestamp_vietnam}__
    **Số nhóm:** `{number_of_chats}`"""
        try:
            m2 = await app.send_message(info["log_group_id"], text=mute_text, disable_web_page_preview=True)
            lydo_text = f"""
    **🔥Người dùng {user.mention} @{username2} đã bị đeo rọ mõm 👙.**
    **Bởi: {from_user.mention} @{username1}.**
    **Lý do: __{reason}__.**"""
            nut = F"tg://openmessage?user_id={from_user.id}"
            keyboard = ikb({"🚨  LIÊN HỆ ADMIN  🚨": {nut}})
            await m.edit(text=lydo_text, reply_markup=keyboard)
        except Exception:
            await message.reply_text(
                "Người dùng bị cấm chat, nhưng hành động cấm chat này không được ghi lại, hãy thêm tôi vào nhóm quản lý"
            )
    if message.command[0][0] == "s":
        try:
            await app.send_message(user.id, f"Xin chào {user.mention}, bạn đã bị cấm chat tại nhóm {message.chat.title} với lý do: {reason}, bạn hãy nhắn tin cho admin {from_user.mention} t.me/{username1} để mở chat.")
        except Exception:
            pass
        mute_text = f"""
    __**Người dùng bị sfmute toàn hệ thống **__
    **Tại nhóm:** {message.chat.title} [`{message.chat.id}`]
    **Quản trị viên:** {from_user.mention} @{username1}
    **Người dùng bị cấm chat:** {user.mention} @{username2} **ID:** `{user_id}`
    **Lý do:** __{reason}__
    **Lúc:** __{timestamp_vietnam}__
    **Số nhóm:** `{number_of_chats}`"""
        try:
            m2 = await app.send_message(info["log_group_id"], text=mute_text, disable_web_page_preview=True)
        except Exception:
            await message.reply_text(
                "Người dùng bị cấm chat, nhưng hành động cấm chat này không được ghi lại, hãy thêm tôi vào nhóm quản lý"
            )

    if message.command[0] == "checkvoice":
        try:
            await app.send_message(user.id, f"Xin chào {user.mention}, bạn đã bị cấm chat tại nhóm {message.chat.title}, bạn hãy xác thực bằng giọng nói cho admin {from_user.mention} t.me/{username1} để mở chat.")
        except Exception:
            pass
        #await app2.send_message(user.id, f"Xin chào, bạn đã bị cấm chat tại nhóm {message.chat.title} với lý do: {reason}, bạn hãy nhắn tin cho admin {from_user.mention} @{username1} để mở chat.")
        await m.edit(f"Đã cấm chat {user.mention} trong liên đoàn!")
        mute_text = f"""
    __**Người dùng bị fmute chờ checkvoice toàn hệ thống **__
    **Tại nhóm:** {message.chat.title} [`{message.chat.id}`]
    **Quản trị viên:** {from_user.mention} @{username1}
    **Người dùng bị cấm chat:** {user.mention} @{username2} **ID:** `{user_id}`
    **Lý do:** __{reason}__
    **Số nhóm:** `{number_of_chats}`"""
        try:
            m2 = await app.send_message(info["log_group_id"], text=mute_text, disable_web_page_preview=True)
            lydo_text = f"""
    **🔥Người dùng {user.mention} @{username2} đã bị cấm chat 👙.**
    **Bởi: {from_user.mention} @{username1}.**
    **Lý do: Xác thực giọng nói với admin {reason or from_user.mention} để được mở chat  💬💬💬.**"""
            nut = F"tg://openmessage?user_id={from_user.id}"
            keyboard = ikb({"🚨  LIÊN HỆ ADMIN  🚨": {nut}})
            await m.edit(text=lydo_text, reply_markup=keyboard)
        except Exception:
            await message.reply_text(
                "Người dùng bị cấm chat, nhưng hành động cấm chat này không được ghi lại, hãy thêm tôi vào nhóm quản lý"
            )

#Funmute

@app.on_message(filters.command(["unfmute", "sunfmute", "xacnhan"]))
@capture_err
async def funmute_user(client, message):
    chat = message.chat
    from_user = message.from_user
    me = await app.get_me()
    BOT_ID = me.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(
            "Lệnh này dùng trong nhóm, không phải trong tin nhắn riêng của tôi!."
        )

    fed_id = await get_fed_id(chat.id)
    if not fed_id:
        return await message.reply_text(
            "**Cuộc trò chuyện này không thuộc bất kỳ liên đoàn nào."
        )
    info = await get_fed_info(fed_id)
    fed_owner = info["owner_id"]
    fed_admins = info["fadmins"]
    all_admins = [fed_owner] + fed_admins + [int(BOT_ID)]
    if from_user.id in all_admins or from_user.id in SUDOERS:
        pass
    else:
        return await message.reply_text(
            "Bạn cần phải là Admin liên đoàn để sử dụng lệnh này"
        )
    """if len(message.command) < 2:
        return await message.reply_text(
            "**Bạn cần phải chỉ định người dùng hoặc trả lời tin nhắn của họ!**"
        )"""
    user_id, reason = await extract_user_and_reason(message)
    user = await app.get_users(user_id)
    if not user_id:
        return await message.reply_text("Tôi không thể tìm thấy người dùng đó.")
    if user_id in all_admins or user_id in SUDOERS:
        return await message.reply_text(
            "**Làm sao một quản trị viên có thể bị cấm chat!.**"
        )
    check_user = await check_banned_user(fed_id, user_id)
    if check_user:
        reason = check_user["reason"]
        date = check_user["date"]
        return await message.reply_text(
            f"**Người dùng {user.mention} đã bị Cấm trong liên đoàn.\n\nLý do: {reason}.\nNgày: {date}.**"
        )
    check_user1 = await check_muted_user(fed_id, user_id)
    if check_user1:
        reason = check_user1["reason"]
        date = check_user1["date"]
        return await message.reply_text(
            f"**Người dùng {user.mention} đã bị Cấm chat trong liên đoàn.\n\nLý do: {reason}.\nNgày: {date}.**"
        )
    if message.command[0][0] == "x":
        check_user2 = await check_actived_user(fed_id, user_id)
        if check_user2:
            reason = check_user2["reason"]
            date = check_user2["date"]
            return await message.reply_text(
                f"**Người dùng {user.mention} đã được xác thực trong liên đoàn.\n\nNote: {reason}.\nNgày: {date}.**"
            )
    if not reason:
        return await message.reply("Không có lý do nào được cung cấp.")

    served_chats, _ = await chat_id_and_names_in_fed(fed_id)
    m = await message.reply_text(
        f"**Bỏ Lệnh Cấm chat liên đoàn {user.mention}!**"
        + f" **Hành động này sẽ mất khoảng {len(served_chats)} giây.**"
    )
    if message.command[0][0] == "a":
        await add_active_user(fed_id, user_id, reason)
    await remove_fmute_user(fed_id, user_id)
    number_of_chats = 0
    for served_chat in served_chats:
        try:
            chat_member = await app.get_chat_member(served_chat, user.id)
            if chat_member.status == ChatMemberStatus.BANNED:
                await app.unban_chat_member(served_chat, user.id)
                if served_chat != chat.id:
                    if not message.text.startswith("/s"):
                        await app.send_message(served_chat, f"**Đã bỏ cấm trong liên đoàn :{user.mention} !**")
                number_of_chats += 1
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(int(e.value))
        except Exception:
            pass
    try:
        await app.send_message(
            user.id,
            f"Xin chào, Bạn đã được bỏ cấm chat bởi {from_user.mention},"
            + " Bạn có thể cảm ơn họ vì hành động này.",
        )
    except Exception:
        pass
    await m.edit(f"Đã bỏ cấm chat trong liên đoàn :{user.mention} !")
    ban_text = f"""
__**Lệnh bỏ cấm chat liên đoàn mới**__
**Nguồn gốc:** {message.chat.title} [`{message.chat.id}`]
**Quản trị viên:** {from_user.mention}
**Người dùng được bỏ cấm:** {user.mention} **ID:** `{user_id}`
**Lý do:** __{reason}__
**Số lượng nhóm:** `{number_of_chats}`"""
    try:
        m2 = await app.send_message(
            info["log_group_id"],
            text=ban_text,
            disable_web_page_preview=True,
        )
        await m.edit(
            f"Đã bỏ cấm chat trong liên đoàn {user.mention} !\nNhật ký hành động: {m2.link}",
            disable_web_page_preview=True,
        )
    except Exception:
        await message.reply_text(
            "Người dùng unfmute, nhưng hành động Fban này không được ghi lại, hãy thêm tôi vào LOG_GROUP"
        )

##############

#unactive
@app.on_message(filters.command("huy"))
@capture_err
async def unactive_user(client, message):
    chat = message.chat
    from_user = message.from_user
    me = await app.get_me()
    BOT_ID = me.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(
            "Lệnh này dùng trong nhóm, không phải trong tin nhắn riêng của tôi!."
        )

    fed_id = await get_fed_id(chat.id)
    if not fed_id:
        return await message.reply_text(
            "**Cuộc trò chuyện này không thuộc bất kỳ liên đoàn nào."
        )
    info = await get_fed_info(fed_id)
    fed_owner = info["owner_id"]
    fed_admins = info["fadmins"]
    all_admins = [fed_owner] + fed_admins + [int(BOT_ID)]
    if from_user.id in all_admins or from_user.id in SUDOERS:
        pass
    else:
        return await message.reply_text(
            "Bạn cần phải là Admin liên đoàn để sử dụng lệnh này"
        )
    """if len(message.command) < 2:
        return await message.reply_text(
            "**Bạn cần phải chỉ định người dùng hoặc trả lời tin nhắn của họ!**"
        )"""
    user_id, reason = await extract_user_and_reason(message)
    user = await app.get_users(user_id)
    if not user_id:
        return await message.reply_text("Tôi không thể tìm thấy người dùng đó.")
    #if user_id in all_admins or user_id in SUDOERS:
        #return await message.reply_text(
           # "**Làm sao một quản trị viên có thể bị cấm!.**"
        #)
    check_user = await check_actived_user(fed_id, user_id)
    if not check_user:
        return await message.reply_text(
            "**Nguời dùng này chưa được xác thực.**"
        )

    await remove_actived_user(fed_id, user_id)
    await message.reply_text(f"Đã bỏ xác thực {user.mention} trong liên đoàn!")
    ban_text = f"""
__**Lệnh bỏ xác thực liên đoàn mới**__
**Nguồn gốc:** {message.chat.title} [`{message.chat.id}`]
**Quản trị viên:** {from_user.mention}
**Người dùng được bỏ xác thực:** {user.mention} **ID:** `{user_id}`
**Lý do:** __{reason}__"""
    try:
        m2 = await app.send_message(
            info["log_group_id"],
            text=ban_text,
            disable_web_page_preview=True,
        )
    except Exception:
        await message.reply_text(
            "Người dùng unactive, nhưng hành động unactive này không được ghi lại, hãy thêm tôi vào LOG_GROUP"
        )
#xacnhan
@app.on_message(filters.command("xn"))
@capture_err
async def active_user(client, message):
    me = await app.get_me()
    BOT_ID = me.id
    chat = message.chat
    from_user = message.from_user
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(
            "Lệnh này dùng trong nhóm, không phải trong tin nhắn riêng của tôi!."
        )

    fed_id = await get_fed_id(chat.id)
    if not fed_id:
        return await message.reply_text(
            "**Cuộc trò chuyện này không thuộc bất kỳ liên đoàn nào."
        )
    info = await get_fed_info(fed_id)
    fed_owner = info["owner_id"]
    fed_admins = info["fadmins"]
    all_admins = [fed_owner] + fed_admins + [int(BOT_ID)]
    if from_user.id in all_admins or from_user.id in SUDOERS:
        pass
    else:
        return await message.reply_text(
            "Bạn cần phải là Admin liên đoàn để sử dụng lệnh này"
        )
    """if len(message.command) < 2:
        return await message.reply_text(
            "**Bạn cần phải chỉ định người dùng hoặc trả lời tin nhắn của họ!**"
        )"""
    user_id, reason = await extract_user_and_reason(message)
    user = await app.get_users(user_id)
    if not user_id:
        return await message.reply_text("Tôi không thể tìm thấy người dùng đó.")
    #if user_id in all_admins or user_id in SUDOERS:
        #return await message.reply_text(
           # "**Làm sao một quản trị viên có thể bị cấm!.**"
        #)
    check_user = await check_banned_user(fed_id, user_id)
    if check_user:
        reason = check_user["reason"]
        date = check_user["date"]
        return await message.reply_text(
            f"**Người dùng {user.mention} đã bị Cấm trong liên đoàn.\n\nLý do: {reason}.\nNgày: {date}.**"
        )
    check_user1 = await check_muted_user(fed_id, user_id)
    if check_user1:
        reason = check_user1["reason"]
        date = check_user1["date"]
        return await message.reply_text(
            f"**Người dùng {user.mention} đã bị Cấm chat trong liên đoàn.\n\nLý do: {reason}.\nNgày: {date}.**"
        )
    check_user2 = await check_actived_user(fed_id, user_id)
    if check_user2:
        reason = check_user2["reason"]
        date = check_user2["date"]
        return await message.reply_text(
            f"**Người dùng {user.mention} đã được xác thực trong liên đoàn.\n\nNote: {reason}.\nNgày: {date}.**"
        )

    await add_active_user(fed_id, user_id, reason)
    await message.reply_text(f"Đã xác thực {user.mention} trong liên đoàn!")
    ban_text = f"""
__**Lệnh xác thực liên đoàn mới**__
**Nguồn gốc:** {message.chat.title} [`{message.chat.id}`]
**Quản trị viên:** {from_user.mention}
**Người dùng được xác thực:** {user.mention} **ID:** `{user_id}`
**Lý do:** __{reason}__"""
    try:
        m2 = await app.send_message(
            info["log_group_id"],
            text=ban_text,
            disable_web_page_preview=True,
        )
    except Exception:
        await message.reply_text(
            "Người dùng được active, nhưng hành động active này không được ghi lại, hãy thêm tôi vào LOG_GROUP"
        )
##############
#check
@app.on_message(filters.command("check") & ~filters.private)
async def check(client, message):
    user_id = await extract_user(message)
    from_user = message.from_user
    fed_id = await get_fed_id(chat.id)
    if not fed_id:
        return await message.reply_text(
            "**Cuộc trò chuyện này không thuộc bất kỳ liên đoàn nào."
        )
    if not user_id:
        return await message.reply_text("Tôi không thể tìm thấy người dùng đó.")
    user = await app.get_users(user_id)

    check_user = await check_banned_user(fed_id, user_id)
    if check_user:
        reason = check_user["reason"]
        date = check_user["date"]
        return await message.reply_text(
            f"**Người dùng {user.mention} đã bị Cấm trong liên đoàn.\n\nLý do: {reason}.\nNgày: {date}.**"
        )
    check_user1 = await check_muted_user(fed_id, user_id)
    if check_user1:
        reason = check_user1["reason"]
        date = check_user1["date"]
        return await message.reply_text(
            f"**Người dùng {user.mention} đã bị Cấm chat trong liên đoàn.\n\nLý do: {reason}.\nNgày: {date}.**"
        )
    check_user2 = await check_actived_user(fed_id, user_id)
    if check_user2:
        reason = check_user2["reason"]
        date = check_user2["date"]
        return await message.reply_text(
            f"**Người dùng {user.mention} đã được xác thực trong liên đoàn.\n\nNote: {reason}.\nNgày: {date}.**"
        )

    else:
        await message.reply_text("Người này chưa được xác nhận.")



################        
#Funban
@app.on_message(filters.command(["unfban", "sunfban"]))
@capture_err
async def funban_user(client, message):
    chat = message.chat
    from_user = message.from_user
    me = await app.get_me()
    BOT_ID = me.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(
            "Lệnh này dùng trong nhóm, không phải trong tin nhắn riêng của tôi!."
        )

    fed_id = await get_fed_id(chat.id)
    if not fed_id:
        return await message.reply_text(
            "**Cuộc trò chuyện này không thuộc bất kỳ liên đoàn nào."
        )
    info = await get_fed_info(fed_id)
    fed_owner = info["owner_id"]
    fed_admins = info["fadmins"]
    all_admins = [fed_owner] + fed_admins + [int(BOT_ID)]
    if from_user.id in all_admins or from_user.id in SUDOERS:
        pass
    else:
        return await message.reply_text(
            "Bạn cần phải là Admin liên đoàn để sử dụng lệnh này"
        )
    """if len(message.command) < 2:
        return await message.reply_text(
            "**Bạn cần phải chỉ định người dùng hoặc trả lời tin nhắn của họ!**"
        )"""
    user_id, reason = await extract_user_and_reason(message)
    user = await app.get_users(user_id)
    if not user_id:
        return await message.reply_text("Tôi không thể tìm thấy người dùng đó.")
    if user_id in all_admins or user_id in SUDOERS:
        return await message.reply_text(
            "**Làm sao một quản trị viên có thể bị cấm!.**"
        )
    check_user = await check_banned_user(fed_id, user_id)
    if not check_user:
        return await message.reply_text(
            "**Tôi không thể bỏ lệnh cấm một người dùng chưa bao giờ bị cấm.**"
        )
    if not reason:
        return await message.reply("Không có lý do nào được cung cấp.")

    served_chats, _ = await chat_id_and_names_in_fed(fed_id)
    m = await message.reply_text(
        f"**Bỏ Lệnh Cấm liên đoàn {user.mention}!**"
        + f" **Hành động này sẽ mất khoảng {len(served_chats)} giây.**"
    )
    await remove_fban_user(fed_id, user_id)
    number_of_chats = 0
    for served_chat in served_chats:
        try:
            chat_member = await app.get_chat_member(served_chat, user.id)
            if chat_member.status == ChatMemberStatus.BANNED:
                await app.unban_chat_member(served_chat, user.id)
                if served_chat != chat.id:
                    if not message.text.startswith("/s"):
                        await app.send_message(
                            served_chat, f"**Đã bỏ cấm trong liên đoàn :{user.mention} !**"
                        )
                number_of_chats += 1
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(int(e.value))
        except Exception:
            pass
    try:
        await app.send_message(
            user.id,
            f"Xin chào, Bạn đã được bỏ cấm bởi {from_user.mention},"
            + " Bạn có thể cảm ơn họ vì hành động này.",
        )
    except Exception:
        pass
    await m.edit(f"Đã bỏ cấm trong liên đoàn :{user.mention} !")
    ban_text = f"""
__**Lệnh bỏ cấm liên đoàn mới**__
**Nguồn gốc:** {message.chat.title} [`{message.chat.id}`]
**Quản trị viên:** {from_user.mention}
**Người dùng được bỏ cấm:** {user.mention}
**ID người dùng được bỏ cấm:** `{user_id}`
**Lý do:** __{reason}__
**Số lượng nhóm:** `{number_of_chats}`"""
    try:
        m2 = await app.send_message(
            info["log_group_id"],
            text=ban_text,
            disable_web_page_preview=True,
        )
        await m.edit(
            f"Đã bỏ cấm trong liên đoàn {user.mention} !\nNhật ký hành động: {m2.link}",
            disable_web_page_preview=True,
        )
    except Exception:
        await message.reply_text(
            "Người dùng FUnbanned, nhưng hành động Fban này không được ghi lại, hãy thêm tôi vào LOG_GROUP"
        )


async def status(message, user_id):
    status = await get_user_fstatus(user_id)
    user = await app.get_users(user_id)
    if status:
        response_text = "\n\n".join(
            [
                f"{i + 1}) **Tên liên đoàn:** {fed['fed_name']}\n  **ID liên đoàn:** `{fed['fed_id']}`"
                for i, fed in enumerate(status)
            ]
        )
        await message.reply_text(
            f"**Dưới đây là danh sách các liên đoàn {user.mention} đã bị cấm trong:**\n\n{response_text}"
        )
    else:
        return await message.reply_text(f"**{user.mention} không bị cấm ở bất kỳ liên đoàn nào.**")


@app.on_message(filters.command("fedstat"))
@capture_err
async def fedstat(client, message):
    user = message.from_user
    if message.chat.type != ChatType.PRIVATE:
        return await message.reply_text(
            "Trạng thái Cấm Liên đoàn chỉ có thể được kiểm tra bằng cách nhắn tin riêng cho tôi."
        )

    if len(message.command) < 2:
        user_id = user.id
        return await status(message, user_id)

    user_id, fed_id = await extract_user_and_reason(message)
    if not user_id:
        user_id = message.from_user.id
        fed_id = message.text.split(" ", 1)[1].strip()
    if not fed_id:
        return await status(message, user_id)

    info = await get_fed_info(fed_id)
    if not info:
        await message.reply_text("Vui lòng nhập ID liên đoàn hợp lệ")
    else:
        check_user = await check_banned_user(fed_id, user_id)
        if check_user:
            user = await app.get_users(user_id)
            reason = check_user["reason"]
            date = check_user["date"]
            return await message.reply_text(
                f"**Người dùng {user.mention} đã bị cấm trong liên đoàn vì:\n\nLý do: {reason}.\nNgày: {date}.**"
            )
        else:
            await message.reply_text(
                f"**Người dùng {user.mention} không bị Cấm trong liên đoàn này.**"
            )


@app.on_message(filters.command("fbroadcast"))
@capture_err
async def fbroadcast_message(client, message):
    chat = message.chat
    from_user = message.from_user
    me = await app.get_me()
    BOT_ID = me.id
    reply_message = message.reply_to_message
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(
            "Lệnh này dùng trong nhóm, không phải trong tin nhắn riêng của tôi!."
        )

    fed_id = await get_fed_id(chat.id)
    if not fed_id:
        return await message.reply_text(
            "**Cuộc trò chuyện này không phải là một phần của bất kỳ liên đoàn nào."
        )
    info = await get_fed_info(fed_id)
    fed_owner = info["owner_id"]
    fed_admins = info["fadmins"]
    all_admins = [fed_owner] + fed_admins + [int(BOT_ID)]
    if from_user.id in all_admins or from_user.id in SUDOERS:
        pass
    else:
        return await message.reply_text(
            "Bạn cần phải là Admin liên đoàn để sử dụng lệnh này"
        )
    if not reply_message:
        return await message.reply_text(
            "**Bạn cần trả lời tin nhắn để Phát sóng nó.**"
        )
    sleep_time = 0.1

    sent = 0
    chats, _ = await chat_id_and_names_in_fed(fed_id)
    m = await message.reply_text(
        f"Đang phát sóng, sẽ mất {len(chats) * sleep_time} giây."
    )
    to_copy = not reply_message.poll
    for i in chats:
        try:
            if to_copy:
                await reply_message.copy(i)
            else:
                await reply_message.forward(i)
            sent += 1
            await asyncio.sleep(sleep_time)
        except FloodWait as e:
            await asyncio.sleep(int(e.value))
        except Exception:
            pass
    await m.edit(f"**Tin nhắn được gửi đi trong {sent} nhóm.**")


@app.on_callback_query(filters.regex("rmfed_(.*)"))
async def del_fed_button(client, cb):
    query = cb.data
    userid = cb.message.chat.id
    fed_id = query.split("_")[1]

    if fed_id == "cancel":
        await cb.message.edit_text("Xóa Liên đoàn đã bị hủy bỏ")
        return

    getfed = await get_fed_info(fed_id)
    if getfed:
        delete = fedsdb.delete_one({"fed_id": str(fed_id)})
        if delete:
            await cb.message.edit_text(
                "Bạn đã xóa Liên đoàn của mình! Bây giờ tất cả các Nhóm được kết nối với `{}` đều không có Liên đoàn.".format(
                    getfed["fed_name"]
                ),
                parse_mode=ParseMode.MARKDOWN,
            )


@app.on_callback_query(filters.regex("trfed_(.*)"))
async def fedtransfer_button(client, cb):
    query = cb.data
    userid = cb.message.chat.id
    data = query.split("_")[1]

    if data == "cancel":
        return await cb.message.edit_text("Chuyển nhượng liên đoàn bị hủy bỏ")

    data2 = data.split("|", 1)
    new_owner_id = int(data2[0])
    fed_id = data2[1]
    transferred = await transfer_owner(fed_id, userid, new_owner_id)
    if transferred:
        await cb.message.edit_text(
            "**Đã chuyển nhượng quyền sở hữu thành công cho chủ sở hữu mới.**"
        )


@app.on_callback_query(filters.regex("fed_(.*)"))
async def fed_owner_help(client, cb):
    query = cb.data
    userid = cb.message.chat.id
    data = query.split("_")[1]
    if data == "owner":
        text = """**👑 Lệnh cho chủ sở hữu liên đoàn:**
 • /newfed <tên_liên đoàn>**:** Tạo một Liên đoàn, Mỗi người dùng được phép tạo một Liên đoàn
 • /renamefed <ID_liên đoàn> <Tên_Mới_Của liên đoàn>**:** Đổi tên của liên đoàn thành tên mới bằng cách cung cấp ID
 • /delfed <ID_liên đoàn>**:** Xóa Liên đoàn và mọi thông tin liên quan đến nó. Sẽ không hủy người dùng bị cấm
 • /myfeds**:** Để liệt kê các liên đoàn mà bạn đã tạo
 • /fedtransfer <người được chuyển nhượng> <ID_liên đoàn>**:**Để chuyển nhượng quyền sở hữu liên đoàn cho người khác
 • /fpromote <user>**:** Chỉ định người dùng làm quản trị viên liên đoàn. Cho phép tất cả các lệnh cho người dùng theo `Lệnh cho QTV liên đoàn`
 • /fdemote <user>**:** Xóa Người dùng khỏi quản trị Liên đoàn thành Người dùng bình thường
 • /setfedlog <ID_liên đoàn>**:** Đặt nhóm làm cơ sở báo cáo nhật ký được cung cấp cho liên đoàn
 • /unsetfedlog <fed_id>**:** Xóa nhóm làm cơ sở báo cáo nhật ký được cung cấp cho liên đoàn
 • /fbroadcast **:** Phát tin nhắn đến tất cả các nhóm đã tham gia liên đoàn của bạn """
    elif data == "admin":
        text = """**🔱 Lệnh cho QTV liên đoàn:**
 • /fban <user> <reason>**:** cấm một người dùng
 • /sfban**:** cấm người dùng mà không gửi thông báo đến cuộc trò chuyện
 • /unfban <user> <reason>**:** Xóa người dùng khỏi lệnh cấm của liên đoàn
 • /sunfban**:** Bỏ cấm người dùng mà không gửi thông báo
 • /fdel**:** xóa tất cả tin nhắn của một người trong các nhóm thuộc liên đoàn
 • /fmute <user> <reason>**:** cấm chat một người dùng
 • /sfmute**:** cấm chat một người dùng mà không gửi thông báo
 • /unfmute <user> <reason>**:** Xóa người dùng khỏi lệnh cấm chat của liên đoàn
 • /sunfmute**:** Bỏ cấm chat người dùng mà không gửi thông báo
 • /fedadmins**:** Hiển thị quản trị viên Liên đoàn
 • /fedchats <Fed_ID>**:** Nhận tất cả các cuộc trò chuyện được kết nối trong Liên đoàn
 • /fbroadcast **:** Phát tin nhắn đến tất cả các nhóm đã tham gia liên đoàn của bạn
 """
    else:
        text = """**Lệnh người dùng:**
• /fedinfo <Fed_ID>: Thông tin về một liên đoàn.
• /fedadmins <Fed_ID>: Liệt kê các quản trị viên trong một liên đoàn.
• /joinfed <Fed_ID>: Tham gia nhóm hiện tại vào một liên đoàn. Một nhóm chỉ có thể tham gia một liên đoàn. Chỉ dành cho chủ sở hữu nhóm.
• /leavefed: Rời khỏi liên đoàn hiện tại. Chỉ chủ sở hữu nhóm mới có thể thực hiện việc này.
• /fedstat: Liệt kê tất cả các liên đoàn mà bạn đã bị cấm.
• /fedstat <user_ID>: Liệt kê tất cả các liên đoàn mà người dùng đã bị cấm.
• /fedstat <Fed_ID>: Cung cấp thông tin về lệnh cấm của bạn trong liên đoàn.
• /fedstat <user_ID> <FedID>: Cung cấp thông tin về lệnh cấm của người dùng trong liên đoàn.
• /chatfed: Thông tin về liên đoàn nơi cuộc trò chuyện hiện tại đang diễn ra.
"""
    await cb.message.edit(
        html.escape(text),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Quay lại", callback_data="help_module(federation)"
                    ),
                ]
            ]
        ),
        parse_mode=ParseMode.MARKDOWN,
    )
