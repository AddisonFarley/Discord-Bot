from discord.ext import commands


class Tracking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
		
    @commands.Cog.listener()
    async def on_ready(self):
	    print('Tracking cog loaded') #Checking to make sure this cog is loaded upon initialization.
		

#communicates with extension loader/reloader in main
def setup(bot):
	bot.add_cog(Tracking(bot))
