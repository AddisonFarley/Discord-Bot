from discord.ext import commands

class math_calculator(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
	    print('Math cog loaded') #Checking to make sure this cog is loaded upon initialization.

	@commands.command()
	async def math(self, ctx, *, equation):
		'''
		!math (equation)

		Keyword Arguments:
        self                   	-- This object.
        ctx                 	-- Defined bot command-prefix.
        equation               	-- User-defined equation.
        
        Return Value:
        Floating point number evauluated from equation input by user. 
		'''
		result = round(eval(equation), 2) #rounds answer to two decimals

		if result // 1 != 0: #checks if answer has a decimal value other than zero
			await ctx.send(result) #sends float
		else:
			await ctx.send(int(result)) #sends int

#communicates with extension loader/reloader in main
def setup(bot):
	bot.add_cog(math_calculator(bot))
