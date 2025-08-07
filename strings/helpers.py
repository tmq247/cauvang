HELP_1 = """<b><u>ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs :</b></u>

Chỉ cần thêm <b>c</b> vào đầu các lệnh để sử dụng chúng cho kênh.


/pause : Tạm dừng bản nhạc phát hiện tại.

/resume : Tiếp tục phát bản nhạc đang dừng hiện tại

/skip : bỏ qua bản nhạc đang phát và bắt đầu phát track tiếp theo trong hàng đợi.

/end ᴏʀ /stop : dọn dẹp hàng đợi và kết thúc lbản nhạc đang phát hiện tại.

/player : Nhận một bảng điều khiển tương tác người dùng.

/queue : hiển thị danh sách các bản nhạc đã được xếp hàng.
"""

HELP_2 = """
<b><u>ᴀᴜᴛʜ ᴜsᴇʀs :</b></u>

ᴀᴜᴛʜ ᴜsᴇʀs ᴄᴀɴ ᴜsᴇ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ɪɴ ᴛʜᴇ ʙᴏᴛ ᴡɪᴛʜᴏᴜᴛ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ɪɴ ᴛʜᴇ ᴄʜᴀᴛ.

/auth [ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ_ɪᴅ] : ᴀᴅᴅ ᴀ ᴜsᴇʀ ᴛᴏ ᴀᴜᴛʜ ʟɪsᴛ ᴏғ ᴛʜᴇ ʙᴏᴛ.
/unauth [ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ_ɪᴅ] : ʀᴇᴍᴏᴠᴇ ᴀ ᴀᴜᴛʜ ᴜsᴇʀs ғʀᴏᴍ ᴛʜᴇ ᴀᴜᴛʜ ᴜsᴇʀs ʟɪsᴛ.
/authusers : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ᴀᴜᴛʜ ᴜsᴇʀs ᴏғ ᴛʜᴇ ɢʀᴏᴜᴩ.
"""

HELP_3 = """
<u><b>ʙʀᴏᴀᴅᴄᴀsᴛ ғᴇᴀᴛᴜʀᴇ</b></u> [ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs] :

/broadcast [ᴍᴇssᴀɢᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ] : ʙʀᴏᴀᴅᴄᴀsᴛ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ.

<u>ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴍᴏᴅᴇs :</u>
<b>-pin</b> : ᴩɪɴs ʏᴏᴜʀ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇs ɪɴ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs.
<b>-pinloud</b> : ᴩɪɴs ʏᴏᴜʀ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ɪɴ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴀɴᴅ sᴇɴᴅ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ᴛᴏ ᴛʜᴇ ᴍᴇᴍʙᴇʀs.
<b>-user</b> : ʙʀᴏᴀᴅᴄᴀsᴛs ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴛᴏ ᴛʜᴇ ᴜsᴇʀs ᴡʜᴏ ʜᴀᴠᴇ sᴛᴀʀᴛᴇᴅ ʏᴏᴜʀ ʙᴏᴛ.
<b>-assistant</b> : ʙʀᴏᴀᴅᴄᴀsᴛ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ᴛʜᴇ ᴀssɪᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ ᴏғ ᴛʜᴇ ʙᴏᴛ.
<b>-nobot</b> : ғᴏʀᴄᴇs ᴛʜᴇ ʙᴏᴛ ᴛᴏ ɴᴏᴛ ʙʀᴏᴀᴅᴄᴀsᴛ ᴛʜᴇ ᴍᴇssᴀɢᴇ..

<b>ᴇxᴀᴍᴩʟᴇ:</b> <code>/broadcast -user -assistant -pin ᴛᴇsᴛɪɴɢ ʙʀᴏᴀᴅᴄᴀsᴛ</code>
"""

HELP_4 = """<u><b>ᴄʜᴀᴛ ʙʟᴀᴄᴋʟɪsᴛ ғᴇᴀᴛᴜʀᴇ :</b></u> [ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs]

ʀᴇsᴛʀɪᴄᴛ sʜɪᴛ ᴄʜᴀᴛs ᴛᴏ ᴜsᴇ ᴏᴜʀ ᴘʀᴇᴄɪᴏᴜs ʙᴏᴛ.

/blacklistchat [ᴄʜᴀᴛ ɪᴅ] : ʙʟᴀᴄᴋʟɪsᴛ ᴀ ᴄʜᴀᴛ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ.
/whitelistchat [ᴄʜᴀᴛ ɪᴅ] : ᴡʜɪᴛᴇʟɪsᴛ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛ.
/blacklistedchat : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛs.
"""

HELP_5 = """
<u><b>ʙʟᴏᴄᴋ ᴜsᴇʀs:</b></u> [ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs]

sᴛᴀʀᴛs ɪɢɴᴏʀɪɴɢ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴜsᴇʀ, sᴏ ᴛʜᴀᴛ ʜᴇ ᴄᴀɴ'ᴛ ᴜsᴇ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs.

/block [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ʙʟᴏᴄᴋ ᴛʜᴇ ᴜsᴇʀ ғʀᴏᴍ ᴏᴜʀ ʙᴏᴛ.
/unblock [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ᴜɴʙʟᴏᴄᴋs ᴛʜᴇ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀ.
/blockedusers : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs.
"""

HELP_6 = """
<u><b>ᴄʜᴀɴɴᴇʟ ᴩʟᴀʏ ᴄᴏᴍᴍᴀɴᴅs:</b></u>

ʏᴏᴜ ᴄᴀɴ sᴛʀᴇᴀᴍ ᴀᴜᴅɪᴏ/ᴠɪᴅᴇᴏ ɪɴ ᴄʜᴀɴɴᴇʟ.

/cplay : sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴀᴜᴅɪᴏ ᴛʀᴀᴄᴋ ᴏɴ ᴄʜᴀɴɴᴇʟ's ᴠɪᴅᴇᴏᴄʜᴀᴛ.
/cvplay : sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴠɪᴅᴇᴏ ᴛʀᴀᴄᴋ ᴏɴ ᴄʜᴀɴɴᴇʟ's ᴠɪᴅᴇᴏᴄʜᴀᴛ.
/cplayforce or /cvplayforce : sᴛᴏᴩs ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ.

/channelplay [ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ɪᴅ] ᴏʀ [ᴅɪsᴀʙʟᴇ] : ᴄᴏɴɴᴇᴄᴛ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴀ ɢʀᴏᴜᴩ ᴀɴᴅ sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʀᴀᴄᴋs ʙʏ ᴛʜᴇ ʜᴇʟᴩ ᴏғ ᴄᴏᴍᴍᴀɴᴅs sᴇɴᴛ ɪɴ ɢʀᴏᴜᴩ.
"""

HELP_7 = """
<u><b>ɢʟᴏʙᴀʟ ʙᴀɴ ғᴇᴀᴛᴜʀᴇ</b></u> [ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs] :

/gban [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ɢʟᴏʙᴀʟʟʏ ʙᴀɴs ᴛʜᴇ ᴄʜᴜᴛɪʏᴀ ғʀᴏᴍ ᴀʟʟ ᴛʜᴇ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴀɴᴅ ʙʟᴀᴄᴋʟɪsᴛ ʜɪᴍ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ.
/ungban [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ɢʟᴏʙᴀʟʟʏ ᴜɴʙᴀɴs ᴛʜᴇ ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ ᴜsᴇʀ.
/gbannedusers : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ ᴜsᴇʀs.
"""

HELP_8 = """
<b><u>ʟᴏᴏᴘ sᴛʀᴇᴀᴍ :</b></u>

<b>sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ ɪɴ ʟᴏᴏᴘ</b>

/loop [enable/disable] : ᴇɴᴀʙʟᴇs/ᴅɪsᴀʙʟᴇs ʟᴏᴏᴘ ғᴏʀ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ
/loop [1, 2, 3, ...] : ᴇɴᴀʙʟᴇs ᴛʜᴇ ʟᴏᴏᴘ ғᴏʀ ᴛʜᴇ ɢɪᴠᴇɴ ᴠᴀʟᴜᴇ.
"""

HELP_9 = """
<u><b>ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ</b></u> [ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs] :

/logs : ɢᴇᴛ ʟᴏɢs ᴏғ ᴛʜᴇ ʙᴏᴛ.

/logger [ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ] : ʙᴏᴛ ᴡɪʟʟ sᴛᴀʀᴛ ʟᴏɢɢɪɴɢ ᴛʜᴇ ᴀᴄᴛɪᴠɪᴛɪᴇs ʜᴀᴩᴩᴇɴ ᴏɴ ʙᴏᴛ.

/maintenance [ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ] : ᴇɴᴀʙʟᴇ ᴏʀ ᴅɪsᴀʙʟᴇ ᴛʜᴇ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ ᴏғ ʏᴏᴜʀ ʙᴏᴛ.
"""

HELP_10 = """
<b><u>ᴘɪɴɢ & sᴛᴀᴛs :</b></u>

/start : sᴛᴀʀᴛs ᴛʜᴇ ᴍᴜsɪᴄ ʙᴏᴛ.
/help : ɢᴇᴛ ʜᴇʟᴩ ᴍᴇɴᴜ ᴡɪᴛʜ ᴇxᴩʟᴀɴᴀᴛɪᴏɴ ᴏғ ᴄᴏᴍᴍᴀɴᴅs.

/ping : sʜᴏᴡs ᴛʜᴇ ᴩɪɴɢ ᴀɴᴅ sʏsᴛᴇᴍ sᴛᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ.

/stats : sʜᴏᴡs ᴛʜᴇ ᴏᴠᴇʀᴀʟʟ sᴛᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ.
"""

HELP_11 = """
<u><b>ᴩʟᴀʏ ᴄᴏᴍᴍᴀɴᴅs :</b></u>

<b>v :</b> sᴛᴀɴᴅs ғᴏʀ ᴠɪᴅᴇᴏ ᴩʟᴀʏ.
<b>force :</b> sᴛᴀɴᴅs ғᴏʀ ғᴏʀᴄᴇ ᴩʟᴀʏ.

/play ᴏʀ /vplay : sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ.

/playforce ᴏʀ /vplayforce : sᴛᴏᴩs ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ.
"""

HELP_12 = """
<b><u>sʜᴜғғʟᴇ ᴏ̨ᴜᴇᴜᴇ :</b></u>

/shuffle : sʜᴜғғʟᴇ's ᴛʜᴇ ᴏ̨ᴜᴇᴜᴇ.
/queue : sʜᴏᴡs ᴛʜᴇ sʜᴜғғʟᴇᴅ ᴏ̨ᴜᴇᴜᴇ.
"""

HELP_13 = """
<b><u>sᴇᴇᴋ sᴛʀᴇᴀᴍ :</b></u>

/seek [ᴅᴜʀᴀᴛɪᴏɴ ɪɴ sᴇᴄᴏɴᴅs] : sᴇᴇᴋ ᴛʜᴇ sᴛʀᴇᴀᴍ ᴛᴏ ᴛʜᴇ ɢɪᴠᴇɴ ᴅᴜʀᴀᴛɪᴏɴ.
/seekback [ᴅᴜʀᴀᴛɪᴏɴ ɪɴ sᴇᴄᴏɴᴅs] : ʙᴀᴄᴋᴡᴀʀᴅ sᴇᴇᴋ ᴛʜᴇ sᴛʀᴇᴀᴍ ᴛᴏ ᴛʜᴇ ᴛʜᴇ ɢɪᴠᴇɴ ᴅᴜʀᴀᴛɪᴏɴ.
"""

#"""HELP_14 = """
#<b><u>sᴏɴɢ ᴅᴏᴡɴʟᴏᴀᴅ</b></u>

#/song [sᴏɴɢ ɴᴀᴍᴇ/ʏᴛ ᴜʀʟ] : ᴅᴏᴡɴʟᴏᴀᴅ ᴀɴʏ ᴛʀᴀᴄᴋ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ ɪɴ ᴍᴘ3 ᴏʀ ᴍᴘ4 ғᴏʀᴍᴀᴛs.
#"""

HELP_15 = """
<b><u>sᴘᴇᴇᴅ ᴄᴏᴍᴍᴀɴᴅs :</b></u>

ʏᴏᴜ ᴄᴀɴ ᴄᴏɴᴛʀᴏʟ ᴛʜᴇ ᴘʟᴀʏʙᴀᴄᴋ sᴘᴇᴇᴅ ᴏғ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ. [ᴀᴅᴍɪɴs ᴏɴʟʏ]

/speed or /playback : ғᴏʀ ᴀᴅᴊᴜsᴛɪɴɢ ᴛʜᴇ ᴀᴜᴅɪᴏ ᴘʟᴀʏʙᴀᴄᴋ sᴘᴇᴇᴅ ɪɴ ɢʀᴏᴜᴘ.
/cspeed or /cplayback : ғᴏʀ ᴀᴅᴊᴜsᴛɪɴɢ ᴛʜᴇ ᴀᴜᴅɪᴏ ᴘʟᴀʏʙᴀᴄᴋ sᴘᴇᴇᴅ ɪɴ ᴄʜᴀɴɴᴇʟ.
"""



  #  if data == "owner":
HELP_14 = """
<b><u>Feds</b></u>
**👑 Lệnh cho chủ sở hữu liên đoàn:**
 • /newfed <tên_liên đoàn>**:** Tạo một Liên đoàn, Mỗi người dùng được phép tạo một Liên đoàn
 • /renamefed <ID_liên đoàn> <Tên_Mới_Của liên đoàn>**:** Đổi tên của liên đoàn thành tên mới bằng cách cung cấp ID
 • /delfed <ID_liên đoàn>**:** Xóa Liên đoàn và mọi thông tin liên quan đến nó. Sẽ không hủy người dùng bị cấm
 • /myfeds**:** Để liệt kê các liên đoàn mà bạn đã tạo
 • /fedtransfer <người được chuyển nhượng> <ID_liên đoàn>**:**Để chuyển nhượng quyền sở hữu liên đoàn cho người khác
 • /fpromote <user>**:** Chỉ định người dùng làm quản trị viên liên đoàn. Cho phép tất cả các lệnh cho người dùng theo `Lệnh cho QTV liên đoàn`
 • /fdemote <user>**:** Xóa Người dùng khỏi quản trị Liên đoàn thành Người dùng bình thường
 • /setfedlog <ID_liên đoàn>**:** Đặt nhóm làm cơ sở báo cáo nhật ký được cung cấp cho liên đoàn
 • /unsetfedlog <fed_id>**:** Xóa nhóm làm cơ sở báo cáo nhật ký được cung cấp cho liên đoàn
 • /fbroadcast **:** Phát tin nhắn đến tất cả các nhóm đã tham gia liên đoàn của bạn 
  
**🔱 Lệnh cho QTV liên đoàn:**
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
 • /check**:** kiểm tra người dùng
 • /xacnhan**:** xác nhận đã checkvoice người dùng và hủy cấm chat
 • /huy**:** hủy xác nhận người dùng 
 • /xn**:** xác nhận người dùng đã checkvoice

**Lệnh người dùng:**
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
    
