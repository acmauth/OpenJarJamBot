import discord, os, dotenv
from utils.utilities import *
from discord.ext import commands

# Enabling default...
intents = discord.Intents().default()
# ...guild member-related...
intents.members = True
# ...and message-related intents
intents.message_content = True
# Our main Bot object (derived from discord.ext.commands and not from discord)
bot = commands.Bot(intents=intents, command_prefix=commands.when_mentioned_or("!"), help_command=None)

# Load cogs...
for filename in os.listdir("./modules"):
    if filename.endswith(".py"):
        bot.load_extension(f"modules.{filename[:-3]}")

# (For dbg reasons) The event is triggered when the bot connects to the Discord gateaway with no errros
@bot.event
async def on_ready() -> None:
    await aprint("I'm online!")

if __name__ == "__main__":
    dotenv.load_dotenv() # load .env
    token = os.getenv("DISCORD_BOT_TOKEN") # get the token
    bot.run(token) # run the bot