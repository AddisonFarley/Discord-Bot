from discord.ext import commands
import wikipedia
from textblob import Word
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
from youtube_search import YoutubeSearch
import praw
import bot_tokens as bt


class lookup(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_ready(self):
		print('Lookup cog loaded') #Checking to make sure this cog is loaded upon initialization. 


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
		summary = wikipedia.summary(search) #summary from the queried wiki page is captured.
		page = wikipedia.page(search) #the entirety of the queried wiki page is captured.
		url = page.url #only taking the URL attribute as this will display a thumbnail on discord.
		await ctx.send(f'{url}\n{summary}') #formatted string to send the URL then a newline of the summary.
	
	
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
		text = Word(word) #create a Word instance of the word parameter
		result = text.definitions #finding the definition of the user-defined word
		
		if len(result) != 0: #make sure a definition is only sent for a word that can be defined
			send = f'{word}: *' #creating a formatted string to show the user-defined word first, then open the italics discord command.
			for _ in result: #result is a list, so we need to add all the words in the list to the send variable
				send += _
			send += '*' #close the italics Discord command
			await ctx.send(send)
		
		else: #if no word can be found, let the user know
			await ctx.send(f'Could not find a definition for: {word}')


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
		query = YoutubeSearch(search, max_results=1).to_dict() #send the request for user-defined query. 
		result = query[0] #access the dict from the query variable
		url = 'https://www.youtube.com' #base youtube url
		url += result['url_suffix'] #format the unique URL to the end of the base URL
		await ctx.send(url) #return youtube link to discord
	
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
		
		subreddit = reddit_read_only.subreddit(sub_reddit) #pulls the user-defined subreddit
		try: #conditionals for returned results
			if hot_or_new == 'new'.lower(): #return top 3 new posts if argument=new
				new_list = [] #create a list to store URLs
				for post in subreddit.new(limit=3):
					new_list.append(post.permalink) #store URLs in list
				url = 'https://www.reddit.com' #base URL
				url_list = [] #new list to combine base/returned URLs
				for _ in new_list: 
					url_list.append(f'{url}{_}') #combining URLs
				for _ in url_list:
					await ctx.send(_) #return URLs to discord
	
			elif hot_or_new == "hot".lower() or hot_or_new == None: #return top 3 hot posts if argument=hot or None
				hot_list = [] #create a list to store URLs
				for post in subreddit.hot(limit=3):
					hot_list.append(post.permalink) #store URLs in list
				url = 'https://www.reddit.com' #base URL
				url_list = [] #new list to combine base/returned URLs
				for _ in hot_list:
					url_list.append(f'{url}{_}') #combining URLs
				for _ in url_list:
					await ctx.send(_) #return URLs to discord
		except: #message for no returned results
			await ctx.send(f'Could not find posts for r/{sub_reddit}. Check the spelling of your desired subreddit. If spelt correctly, the subreddit was likely suspended or banned.')


#communicates with extension loader/reloader in main
def setup(bot):
	bot.add_cog(lookup(bot))
