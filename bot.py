import os
from crr import bot
from dotenv import load_dotenv

load_dotenv('.env')

TOKEN = os.environ["TOKEN"]
bot.run(TOKEN)
