from discord.ext import commands
import os
import logging
import bot_tokens as bt


#define what will trigger bot commands
#https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html
bot = commands.Bot(command_prefix='!')


#keeps a running event log while bot is on
#https://discordpy.readthedocs.io/en/stable/logging.html
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


#posts message to console once the bot has succesfully logged into Discord
#https://discordpy.readthedocs.io/en/stable/quickstart.html
@bot.event
async def on_ready():
	print(f'{bot.user} Initialized')


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		bot.load_extension(f'cogs.{filename[:-3]}')


#!reload (command) to reload edited cogs from discord
@bot.command()
async def reload(ctx):
    #reloads the cog file to update without restarting bot
	bot.reload_extension('cogs.tracking')
	await ctx.send('Cog reloaded.')


#bot's authentication token with Discord
bot.run(bt.DISCORD_TOKEN)
