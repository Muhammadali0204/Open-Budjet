from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api import sqlite
from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = sqlite.Database("data/Users.db")
try:
    db.create_table_users()
except:
    pass

try:
    db.create_table_taklifqilganlar()
except:
    pass
ovoz_link = db.select_user_by_id(1)[3]
baza_link = db.select_user_by_id(2)[3]
obunachiga_pul = db.select_user_by_id(3)[2]
taklifga_pul = db.select_user_by_id(4)[2]
vaqt = {}
karta = {}
tolangan_malumot = {}

