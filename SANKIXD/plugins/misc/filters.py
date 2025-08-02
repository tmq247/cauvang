import re
from SANKIXD import app
from config import BOT_USERNAME
from SANKIXD.utils.SANKI_ban import admin_filter
from SANKIXD.mongo.filtersdb import *
from SANKIXD.utils.filters_func import GetFIlterMessage, get_text_reason, SendFilterMessage
from SANKIXD.utils.yumidb import user_admin
from SANKIXD.utils.yumidb import *
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

@app.on_message(filters.command("filter") & admin_filter)
@user_admin
async def _filter(client, message):
    
    chat_id = message.chat.id 
    if (
        message.reply_to_message
        and not len(message.command) == 2
    ):
        await message.reply("Bạn cần đặt tên cho bộ lọc!")  
        return 
    
    filter_name, filter_reason = get_text_reason(message)
    if (
        message.reply_to_message
        and not len(message.command) >=2
    ):
        await message.reply("Bạn cần cung cấp cho bộ lọc một số nội dung!")
        return

    content, text, data_type = await GetFIlterMessage(message)
    await add_filter_db(chat_id, filter_name=filter_name, content=content, text=text, data_type=data_type)
    await message.reply(
        f"Saved filter '`{filter_name}`'."
    )

@app.on_message(filters.command("filterall") & admin_filter)
@user_admin
async def _filter2(client, message):
    
    chat_id = message.chat.id 
    if (
        message.reply_to_message
        and not len(message.command) == 2
    ):
        await message.reply("Bạn cần đặt tên cho bộ lọc!")  
        return 
    
    filter_name2, filter_reason2 = get_text_reason(message)
    if (
        message.reply_to_message
        and not len(message.command) >=2
    ):
        await message.reply("Bạn cần cung cấp cho bộ lọc một số nội dung!")
        return

    content, text, data_type = await GetFIlterMessage(message)
    await add_filter_db(filter_name=filter_name2, content=content, text=text, data_type=data_type)
    await message.reply(
        f"Saved filter '`{filter_name2}`'.")


@app.on_message(~filters.bot & filters.group, group=4)
async def FilterCheckker(client, message):
    if not message.text:
        return
    text = message.text
    chat_id = message.chat.id
    if (
        len(await get_filters_list(chat_id)) == 0
    ):
        return

    ALL_FILTERS = await get_filters_list(chat_id)
    for filter_ in ALL_FILTERS:
        
        if (
            message.command
            and message.command[0] == 'filter'
            and len(message.command) >= 2
            and message.command[1] ==  filter_
        ):
            return
            
        pattern = r"( |^|[^\w])" + re.escape(filter_) + r"( |$|[^\w])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            filter_name, content, text, data_type = await get_filter(chat_id, filter_)
            await SendFilterMessage(
                message=message,
                filter_name=filter_,
                content=content,
                text=text,
                data_type=data_type
            )

@app.on_message(filters.command('filters') & filters.group)
async def _filters(client, message):
    chat_id = message.chat.id
    chat_title = message.chat.title 
    if message.chat.type == 'private':
        chat_title = 'local'
    FILTERS = await get_filters_list(chat_id)
    
    if len(FILTERS) == 0:
        await message.reply(
            f'Không có bộ lọc trong {chat_title}.'
        )
        return

    filters_list = f'Danh sách các bộ lọc trong {chat_title}:\n'
    
    for filter_ in FILTERS:
        filters_list += f'- `{filter_}`\n'
    
    await message.reply(
        filters_list
    )


@app.on_message(filters.command('stopall') & admin_filter)
async def stopall(client, message):
    chat_id = message.chat.id
    chat_title = message.chat.title 
    user = await client.get_chat_member(chat_id,message.from_user.id)
    if not user.status == ChatMemberStatus.OWNER :
        return await message.reply_text("Chỉ chủ sở hữu mới có thể sử dụng cái này!!") 

    KEYBOARD = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text='Xóa tất cả các bộ lọc', callback_data='custfilters_stopall')],
        [InlineKeyboardButton(text='Hủy', callback_data='custfilters_cancel')]]
    )

    await message.reply(
        text=(f'Bạn có chắc chắn muốn dừng **TẤT CẢ** các bộ lọc trong {chat_title}? Hành động này là không thể đảo ngược.'),
        reply_markup=KEYBOARD
    )


@app.on_callback_query(filters.regex("^custfilters_"))
async def stopall_callback(client, callback_query: CallbackQuery):  
    chat_id = callback_query.message.chat.id 
    query_data = callback_query.data.split('_')[1]  

    user = await client.get_chat_member(chat_id, callback_query.from_user.id)

    if not user.status == ChatMemberStatus.OWNER :
        return await callback_query.answer("Chỉ chủ sở hữu mới có thể sử dụng cái này!!") 
    
    if query_data == 'stopall':
        await stop_all_db(chat_id)
        await callback_query.edit_message_text(text="Tôi đã xóa tất cả các bộ lọc trò chuyện.")
    
    elif query_data == 'cancel':
        await callback_query.edit_message_text(text='Đã hủy.')



@app.on_message(filters.command('stopfilter') & admin_filter)
@user_admin
async def stop(client, message):
    chat_id = message.chat.id
    if not (len(message.command) >= 2):
        await message.reply('Sử dụng lệnh /stopfilter')
        return
    
    filter_name = message.command[1]
    if (filter_name not in await get_filters_list(chat_id)):
        await message.reply("Bạn chưa lưu bất kỳ bộ lọc nào về từ này!")
        return
    
    await stop_db(chat_id, filter_name)
    await message.reply(f"Tôi đã tắt bộ lọc `{filter_name}`.")
