import discord, os, dotenv
from utils.utilities import *
from discord.ext import commands

intents = discord.Intents().default()
intents.members = True
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix=commands.when_mentioned_or("!"), help_command=None)

@bot.event
async def on_ready() -> None:
    await aprint("I'm online!")

if __name__ == "__main__":
    dotenv.load_dotenv()
    token = os.getenv("DISCORD_BOT_TOKEN")
    bot.run(token)