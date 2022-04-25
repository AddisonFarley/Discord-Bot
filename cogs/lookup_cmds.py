from discord.ext import commands
from matplotlib.pyplot import hot
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
import praw
import bot_tokens as bt


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
	
	@commands.command()
	async def reddit(self, ctx, sub_reddit=None, hot_or_new=None):
		'''
		!reddit (sub-name, hot or new (hot by default), number of posts (3 by default))

		Keyword Arguments:
        self                   	-- This object.
        ctx                 	-- Defined bot command-prefix.
        subreddit               -- User-defined subreddit.
		hot_or_new				-- Sort results by hot or new. Hot is set by default.
        
        Return Value:
        Reddit URLs (strings) from user-defined subreddit. This can be customized to 
		pull from either hot (by default) or by new. 
		'''
		#read-only instance authenticates with reddit
		reddit_read_only = praw.Reddit(
		client_id = bt.REDDIT_CLIENT_ID,          	#your client id
        client_secret = bt.REDDIT_CLIENT_SECRET,  	#your client secret
        user_agent = bt.REDDIT_USER_AGENT, 			#your user agent
		check_for_async=False)
		#pulls the user-defined subreddit
		subreddit = reddit_read_only.subreddit(sub_reddit)

		if sub_reddit == 'popular' or sub_reddit == 'all':
			front_list = []
			reddit_read_only.subreddit('all')
			for post in subreddit.hot(limit=3):
				front_list.append(post.permalink)
			url = 'https://www.reddit.com'
			url_list = []
			for _ in front_list:
				url_list.append(f'{url}{_}')
			for _ in url_list:
				await ctx.send(_)

		elif hot_or_new == 'new'.lower():
			new_list = []
			for post in subreddit.new(limit=3):
				new_list.append(post.permalink)
			url = 'https://www.reddit.com'
			url_list = []
			for _ in new_list:
				url_list.append(f'{url}{_}')
			for _ in url_list:
				await ctx.send(_)

		elif hot_or_new == "hot".lower() or hot_or_new == None:
			hot_list = []
			for post in subreddit.hot(limit=3):
				hot_list.append(post.permalink)
			url = 'https://www.reddit.com'
			url_list = []
			for _ in hot_list:
				url_list.append(f'{url}{_}')
			for _ in url_list:
				await ctx.send(_)


def setup(bot):
	bot.add_cog(lookup(bot))
