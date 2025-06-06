import discord
from discord import ApplicationContext as Context
from discord.ext import commands

from utils.utilities import embed_colour

class HelpCommandCog(discord.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.slash_command(description="Η εντολή σε πλοηγεί στις διάφορες λειτουργίες που προσφέρει το bot!")
    @commands.has_permissions(manage_guild = True)
    @discord.option(
        name='channel',
        input_type=discord.TextChannel
    )
    async def guide(self, ctx: Context, channel: discord.TextChannel) -> None:
        embed = discord.Embed(colour=embed_colour,
                              title='📜 JarBot Help Guide 📜',
                              description='Οι εντολές του συγκεκριμένου bot αφορούν την διαχείριση των ομάδων '
                                          'του διαγωνισμού Open Jar Jam. \n'
                                          'Παρατηρήσεις:\n '
                                          '1) Οι παράμετροι που περικλείονται με {} είναι υποχρεωτικές, ενώ με [] είναι προαιρετικές\n'
                                          '2) Οι εντολές **accept**, **dismiss** και **kick** μπορούν να εκτελεστούν **__MONO__** από τον'
                                          ' αρχηγό της εκάστοτε ομάδας.')

        embed.add_field(
            name='● /join {όνομα ομάδας}',
            value='> Αν ο χρήστης **δεν ανήκει** σε κάποια ομάδα:\n'
                  '> 1) Αν η ομάδα με το συγκεκριμένο όνομα **δεν υπάρχει**, δημιουργεί μια καινούργια ομάδα και θέτει ως αρχηγό τον '
                  'χρήστη που την έστειλε. Παράλληλα, δημιουργεί δύο καινούργια ιδιωτικά κανάλια, ένα Text Channel κάτω από την κατηγορία καναλιών '
                  '**Teams Chats** και ένα Voice Channel κάτω από την κατηγορία **Teams Voice Chats** αποκλειστικά για τα μέλη της ομάδας, όπως και έναν ξεχωριστό ρόλο με το όνομα της ομάδας\n'
                  '> 2) Αν η ομάδα με το συγκεκριμένο όνομα **υπάρχει** και περιέχει κάτω από 4 χρήστες, στέλνει ένα αίτημα ένταξης στην ομάδα ενώ ο χρήστης πρέπει '
                  'να περιμένει για την απάντηση στο αίτημα. Το αίτημα ένταξης είναι σε μορφή μηνύματος το οποίο στέλνετε από το '
                  'bot στο ιδιωτικό κανάλι της ομάδας.\n'
                  '> Σε οποιαδήποτε άλλη περίπτωση επιστρέφει μήνυμα σφάλματος.\n',
            inline=False
        )
        embed.add_field(
            name='● /requests',
            value='> Αν ο χρήστης **ανήκει** σε κάποια ομάδα, στέλνει μια λίστα ονομάτων που έχουν αιτηθεί την ένταξή τους στην ομάδα\n'
                  '> Αν ο χρήστης **δεν ανήκει** σε κάποια ομάδα, επιστρέφει ένα μήνυμα ειδοποιώντας τον ότι δεν βρίσκεται σε ομάδα.',
            inline=False
        )
        embed.add_field(
            name='● /accept {όνομα χρήστη}',
            value='> Αν ο χρήστης **ανήκει** σε κάποια ομάδα και ο χρήστης της παραμέτρου έχει αιτηθεί την ένταξή του στην ομάδα, '
                  'αποδέχεται το αίτημα και του δίνει τον ειδικό ρόλο της ομάδας. Αλλιώς, επιστρέφει μήνυμα σφάλματος.',
            inline=False
        )
        embed.add_field(
            name='● /dismiss {όνομα χρήστη}',
            value='> Αν ο χρήστης **ανήκει** σε κάποια ομάδα και ο χρήστης της παραμέτρου έχει αιτηθεί την ένταξή του στην ομάδα, '
                  'απορρίπτει το αίτημα του. Αλλιώς, επιστρέφει μήνυμα σφάλματος.',
            inline=False
        )
        embed.add_field(
            name='● /kick {όνομα χρήστη}',
            value='> Αν ο χρήστης **ανήκει** σε κάποια ομάδα και ο χρήστης της παραμέτρου ανήκει στην ομάδα αυτή και ΔΕΝ είναι ο αρχηγός της, '
                  'τον διώχνει από την ομάδα. Αλλιώς, επιστρέφει μήνυμα σφάλματος.',
            inline=False
        )
        embed.add_field(
            name='● /leave',
            value='> Αν ο χρήστης **ανήκει** σε κάποια ομάδα και:\n'
                  '> 1) Είναι ένα __απλό μέλος__ της, τον αφαιρεί από την εκάστοτε ομάδα.\n'
                  '> 2) Είναι ο __αρχηγός__ της ομάδας, μεταφέρει την ιδιοκτησία της ομάδας στο επόμενο **κατά σειρά** μέλος '
                  'της ομάδας και τον αφαιρεί από την ομάδα. Αν δεν υπάρχει άλλο μέλος στην ομάδα, **διαγράφει** την ομάδα,'
                  'τον ειδικό της ρόλο και το ιδιωτικό κανάλι για τα μέλη της.\n'
                  '> Σε οποιαδήποτε άλλη περίπτωση επιστρέφει μήνυμα σφάλματος.',
            inline=False
        )
        embed.add_field(
            name='● /members [όνομα ομάδας]',
            value='> Αν η παράμετρος **είναι κενή** και ο χρήστης **ανήκει** σε κάποια ομάδα, εκτυπώνει τα μέλη της ομάδας του.\n'
                  '> Αν η παράμετρος **δεν είναι κενή** και η αναφερθείσα ομάδα **υπάρχει**, εκτυπώνει τα μέλη της.\n'
                  '> Σε οποιαδήποτε άλλη περίπτωση επιστρέφει μήνυμα σφάλματος.',
            inline=False
        )
        embed.add_field(
            name='● /list',
            value='> Εκτυπώνει όλες τις υπάρχουσες ομάδες.'
        )

        embed.set_footer(
            text='With ♥ by the ACM AUTh Student Chapter',
            icon_url=self.bot.user.avatar.url
        )

        await channel.send(embed=embed)
        await ctx.interaction.respond(f'Sent the embedded guide to channel {channel.mention}')

def setup(bot: commands.Bot):
    bot.add_cog(HelpCommandCog(bot))