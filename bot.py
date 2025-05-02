import discord, os, dotenv
from utils.utilities import *
from utils.database_handler import DatabaseHandler
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

# (For dbg reasons) The event is triggered when the bot connects to the Discord gateaway with no errors
@bot.event
async def on_ready() -> None:
    await aprint("I'm online! Checking the database...")
    await DatabaseHandler.check_tables()

@bot.command()
@commands.has_permissions(manage_guild=True)
async def force_cmd_sync(ctx: commands.Context) -> None:
    await bot.sync_commands(guild_ids=[1366835026741952633])
    await ctx.reply("Forced app commands sync")

@bot.command()
@commands.has_permissions(manage_guild=True)
async def force_cmd_unregister(ctx: commands.Context) -> None:
    await bot.sync_commands(commands=[], guild_ids=[1366835026741952633])
    await ctx.reply("Forced app commands sync")

if __name__ == "__main__":
    dotenv.load_dotenv() # load .env
    token = os.getenv("DISCORD_BOT_TOKEN") # get the token
    bot.run(token) # run the bot