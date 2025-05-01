import discord
from discord import ApplicationContext as Context
from discord.ext import commands

class TeamsCog(discord.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.slash_command(description='Η εντολή στέλνει αίτημα ένταξης σε ομάδα της επιλογής σου!')
    @discord.option(name='team_name',
                    description='Το όνομα της ομάδας',
                    input_type=str)
    async def join(self, ctx: Context, team_name: str) -> None:
        pass

    @commands.slash_command(description='Η εντολή επιστρέφει τα αιτήματα ένταξης χρηστών προς την ομάδα σου!')
    async def requests(self, ctx: Context) -> None:
        pass

    @commands.slash_command(description='Η εντολή αποδέχεται το αίτημα ένταξης του χρήστη της παραμέτρου προς την ομάδα σου!')
    @discord.option(name='user',
                    description='Ο αιτούμενος χρήστης',
                    input_type=discord.Member)
    async def accept(self, ctx: Context, user: discord.Member) -> None:
        pass

    @commands.slash_command(description='Η εντολή απορρίπτει το αίτημα ένταξης του χρήστη της παραμέτρου προς την ομάδα σου!')
    @discord.option(name='user',
                    description='Ο αιτούμενος χρήστης',
                    input_type=discord.Member)
    async def dismiss(self, ctx: Context, user: discord.Member) -> None:
        pass

    @commands.slash_command(description='Η εντολή διώχνει τον χρήστη της παραμέτρου από την ομάδα σου!')
    @discord.option(name='user',
                    description='Ο χρήστος-μέλος της ομάδας',
                    input_type=discord.Member)
    async def kick(self, ctx: Context, user: discord.Member) -> None:
        pass

    @commands.slash_command(description='Η εντολή σε αφαιρεί από την ομάδα σου!')
    async def leave(self, ctx: Context) -> None:
        pass

    @commands.slash_command(description='Η εντολή εκτυπώνει τα μέλη μιας ομάδας!')
    @discord.option(name='team_name',
                    description='',
                    input_type=str,
                    required=False,
                    default='')
    async def members(self, ctx: Context, team_name: str) -> None:
        pass

    @commands.slash_command(description='Η εντολή εκτυπώνει όλες τις υπάρχουσες ομάδες!')
    async def list(self, ctx: Context) -> None:
        pass

def setup(bot: commands.Bot):
    bot.add_cog(TeamsCog(bot))