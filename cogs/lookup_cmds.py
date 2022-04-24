from discord.ext import commands
import wikipedia
from textblob import Word
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger') 
nltk.download('brown')
from youtube_search import YoutubeSearch


class lookup(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_ready(self):
		#Checking to make sure this cog is loaded upon initialization. 
		print('Lookup cog loaded')


	@commands.command()
	async def wiki(self, ctx, *, search):
		'''
		!wiki (search parameters go here)
	
		Keyword Arguments:
        self                   	-- This object.
        ctx                 	-- Defined bot command-prefix.
        search                  -- User-defined query.
        
        Return Value:
        Summary and URL of queried Wikipedia page.
		'''
		#summary from the queried wiki page is captured.
		summary = wikipedia.summary(search)
		#the entirety of the queried wiki page is captured.
		page = wikipedia.page(search)
		#only taking the URL attribute as this will display a thumbnail on discord.
		url = page.url
		#formatted string to send the URL then a newline of the summary.
		await ctx.send(f'{url}\n{summary}')
	
	
	@commands.command()
	async def define(self, ctx, word):
		'''
		!define (a single word goes here)
	
		Keyword Arguments:
        self                   	-- This object.
        ctx                 	-- Defined bot command-prefix.
        word                    -- User-defined word.
        
        Return Value:
        Definition (string) of requested word formatted to be italicized on Discord.
		'''
		#create a Word instance of the word parameter
		text = Word(word)
		#finding the definition of the user-defined word
		result = text.definitions
		#creating a formatted string to show the user-defined word first, then open the italics discord command.
		send = f'{word}: *'
		#result is a list, so we need to add all the words in the list to the send variable
		for _ in result:
			send += _
		#close the italics Discord command
		send += '*'
		await ctx.send(send)


	@commands.command()
	async def yt(self, ctx, *, search):
		'''
		!yt (search parameters go here)

		Keyword Arguments:
        self                   	-- This object.
        ctx                 	-- Defined bot command-prefix.
        search                  -- User-defined query.
        
        Return Value:
        Youtube URL (string) result of query. The queried URL is added to the end of the base youtube URL.
		'''
		#send the request for user-defined query. 
		query = YoutubeSearch(search, max_results=1).to_dict()
		#access the dict from the query variable
		result = query[0]
		#base youtube url
		url = 'https://www.youtube.com'
		#format the unique URL to the end of the base URL
		url += result['url_suffix']
		await ctx.send(url)


def setup(bot):
	bot.add_cog(lookup(bot))
