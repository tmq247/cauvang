from SANKIXD.core.bot import SANKI
from SANKIXD.core.dir import dirr
from SANKIXD.core.git import git
from SANKIXD.core.userbot import Userbot
from SANKIXD.misc import dbb, heroku
from pyrogram import Client
from SafoneAPI import SafoneAPI
from .logging import LOGGER
#from aiohttp import ClientSession

dirr()
git()
dbb()
heroku()

app = SANKI()
api = SafoneAPI()
userbot = Userbot()

x = await app.get_me()
y = await userbot.get_me()


BOT_ID = x.id
USERBOT_ID = y.id


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
