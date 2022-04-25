from discord.ext import commands


class Tracking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
		

#communicates with extension loader/reloader in main
def setup(bot):
	bot.add_cog(Tracking(bot))
