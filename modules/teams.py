import discord
from discord import ApplicationContext as Context
from discord.ext import commands

from utils.database_handler import DatabaseHandler as dh

class TeamsCog(discord.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.slash_command(description='Η εντολή στέλνει αίτημα ένταξης σε ομάδα της επιλογής σου!')
    @discord.option(name='team_name',
                    description='Το όνομα της ομάδας',
                    input_type=str)
    async def join(self, ctx: Context, team_name: str) -> None:
        await ctx.defer()

        user_id = ctx.author.id
        if not await dh.is_user_on_any_team(user_id):
            if await dh.team_exists(team_name):
                result = await dh.create_team_request(team_name, user_id)
                if result == -1: await ctx.respond('Η ομάδα που ανέφερες έχει συμπληρώσει τον μέγιστο αριθμό επιτρεπτών μελών!',
                                                   ephemeral=True)
                elif result == 0: await ctx.respond(f'Έχεις ήδη αιτηθεί την ένταξή σου στην ομάδα {team_name}',
                                                    ephemeral=True)
                else: await ctx.respond(f'Η αίτηση ένταξης προς την ομάδα {team_name} στάλθηκε!',
                                        ephemeral=True)
            else:
                try:
                    await dh.create_team(team_name, user_id) # create the team

                    # create and assign the role
                    await ctx.guild.create_role(reason=f'Role creation for team {team_name}',
                                                name=team_name,
                                                colour=discord.Colour.random(),
                                                permissions=discord.utils.get(ctx.guild.roles, name="@everyone").permissions,
                                                mentionable=False)
                    await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name=team_name),
                                               reason=f'Adding appropriate role to user of team {team_name}')

                    # create the channel
                    txt_channel = await ctx.guild.create_text_channel(reason=f'Channel creation for team {team_name}',
                                                        name=f'team-{team_name}',
                                                        category=discord.utils.get(ctx.guild.categories, name='Teams'),
                                                        overwrites={
                                                            discord.utils.get(ctx.guild.roles, name=team_name) : discord.PermissionOverwrite(
                                                                view_channel = True
                                                            ),
                                                            discord.utils.get(ctx.guild.roles, name='Moderator') : discord.PermissionOverwrite(
                                                                view_channel = True
                                                            ),
                                                            discord.utils.get(ctx.guild.roles, name='@everyone') : discord.PermissionOverwrite(
                                                                view_channel = False
                                                            )
                                                        })

                    # send the final response
                    await ctx.respond(f'Η ομάδα {team_name} δημιουργήθηκε επιτυχώς! Επιπλέον, πήρες τον ειδικό ρόλο, όπως και '
                                      f'δημιουργήθηκε το κανάλι {txt_channel.mention} αποκλειστικά για τα μέλη της ομάδας σου!')
                except:
                    await ctx.respond(f'**__Σφάλμα__**: Ανεπιτυχής δημιουργία της ομάδας `{team_name}`. Παρακαλώ επικοινώνησε με κάποιο μέλος προσωπικού.')
        else:
            await ctx.respond('Ανήκεις ήδη σε ομάδα! Αν επιθυμείς να ενταχθείς σε κάποια άλλη, χρησιμοποίησε την εντολή `/leave` '
                              'για να αποχωρήσεις από την ομάδα σου και έπειτα προσπάθησε ξανά!', ephemeral=True)

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