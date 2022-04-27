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
        equation               	-- User-defined equation. This equation must have all operators
								   and cannot do algebra. Using multiplication in the form x()
								   will return an error, as eval() sees that as calling a function,
								   not multiplication.
        Return Value:
        Floating point number evauluated from equation input by user. 
		'''

		try:
			if eval(equation) // 1 != 0: #checks if answer has a decimal value other than zero
				await ctx.send(round(eval(equation), 2)) #sends float
			else:
				await ctx.send(int(eval(equation))) #sends int
		except:
			await ctx.send(f'Could not evaluate the equation: {equation}')

			
#communicates with extension loader/reloader in main
def setup(bot):
	bot.add_cog(math_calculator(bot))
