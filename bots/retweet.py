#!/usr/bin/python3

import json
import tweepy
import logging
from palindromer import Palindromer
from peers import Peers
from datetime import datetime
import config

logging.basicConfig(level=logging.INFO, filename="palindrobot.log")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())


API_KEY             = config.get_consumer_key()        
API_KEY_SECRET      = config.get_consumer_secret()     
ACCESS_TOKEN        = config.get_access_token()        
ACCESS_TOKEN_SECRET = config.get_access_token_secret()  


api = config.create_api()

try:
	api.verify_credentials()
	logger.info("API Authentication OK")
except:
	logger.info("Error during authentication")


#  ================================================================================

class MyStreamListener(tweepy.Stream):



	def __init__(self, api, api_key, api_key_secret, access_token, access_token_secret):
		super().__init__(api_key, api_key_secret, access_token, access_token_secret)
		self.api = api
		self.palindromer = Palindromer()
		self.palindromer.min_size = 5

		self.seen = set()
		self.white_list = set()
		self.read_seen()
		self.read_white_list()


	def __del__(self):
		self.save_seen()

	def read_white_list(self):
		peers = Peers()
		for line in open("white_list.txt"):
			self.white_list.add(peers.normalize(line))

		logger.info(f"White_list file was read. [{len(self.white_list)}] lines")


	def read_seen(self):
		self.seen = set(line.strip() for line in open("seen.txt"))
		logger.info(f"Seen       file was read. [{len(self.seen)}] lines")

	def save_seen(self):
		f = open("seen.txt","w")

		for l in self.seen:
			if len(l) > 0:
				f.write(l + "\n")

		logger.info("Seen file was saved")

	
	def add_seen(self, palindrome):
		pal = palindrome.id

		if (pal not in self.seen) and (pal not in self.white_list):
			logger.info(f"Adding '{pal}' to seems")
			self.seen.add(pal)



	def quote_retweet(self, tweet, palindrome):

		if not tweet.retweeted:
			
			tweet_user = tweet.user.screen_name
			tweet_id   = tweet.id
			url        = f"https://twitter.com/{tweet_user}/status/{tweet_id}"
			logger.info(f"url: {url}")

			text = "Encontrei um palindromo!\nI found a palindrome!\n"
			text+= f'\n"{palindrome}"\n\n#palindrobot\n'

			try:
				self.api.update_status(text, attachment_url=url)
				#  logger.info(text)
				logger.info("--- Retweeted ---")
				logger.info(f"id = '{palindrome.id}'")
			except:
				logger.error("Error on quote retweet", exc_info=True)
				


	def like(self, tweet):
		if not tweet.favorited:
			
			try:
				self.api.create_favorite(tweet.id)
				logger.info("Liked...")
			except Exception as e:
				logger.error("Error on like")
				

	def was_seem(self, pal_id):
		 return (pal_id in self.seen) and (pal_id not in self.white_list)


	def on_status(self, tweet):

		if not tweet.truncated:
			text = tweet.text
		else:
			text = tweet.extended_tweet["full_text"]

		if tweet.user.screen_name == "thepalindrobot":
			print(f"\nIt's me. tweet.user.screen_name: '{tweet.user.screen_name}'")
			return

		if tweet.user.screen_name == "palindrobot":
			print(f"No creativity:'{text}'\n'")
			return


		lang = tweet.lang

		min_to_retweet = 1400
		min_to_almost  = 1300

		#  if lang == "es":
			#  min_to_retweet = 1600
			#  min_to_almost  = 1200


		pals = self.palindromer.find_subpalindromes(text)


		seem_pals = [p for p in pals      if p.how_nice() >= min_to_almost ]
		almost    = [p for p in seem_pals if p.how_nice() <  min_to_retweet]
		selection = [p for p in seem_pals if p.how_nice() >= min_to_retweet and not self.was_seem(p.id)]

		if len(selection) > 0:
			self.deal_selection(selection, tweet, text)

		if len(almost) > 0:
			self.deal_almost(almost, tweet)


		for p in seem_pals:
			self.add_seen(p)



	def deal_selection(self, selection, tweet, text):
		time = datetime.now().time().strftime("%H:%M:%S")
		logger.info("\n====================================================")
		logger.info(f"[{time}] Author id: {tweet.user.screen_name} Name: {tweet.user.name}")
		logger.info(f"Original: '{text}'\n")
		
		for p in selection:
			logger.info(f"pal = >> ·{p}· << [{p.how_nice()}]\n")

			self.like(tweet)
			self.quote_retweet(tweet, p)

		logger.info("====================================================\n")


	def deal_almost(self, almost, tweet):
		time = datetime.now().time().strftime("%H:%M:%S")
		print(f"Almost...[{time}] ", end='')
		
		for p in almost:
			print(f"pal = --> ·{p}· <-- [{p.how_nice()}] lang={tweet.lang}")



	def on_error(self, status):
		logger.error("Error detected " + str(status))


loc_brazil  = [-74.5 ,-34.2,-33.7,5.9 ]  # Location Brasil
loc_western = [-139.8,-56.4,48.3 ,71.3]  # Location Ocidente

#  ================================================================================

def start_stream():
	while True:
		logger.info("Here we go!")
		try:

			tweets_listener = MyStreamListener(api, API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


			#  langs = ["en","pt","es"]
			langs = ["en","en-gb" ,"pt","es", "fr", "de", "it", "ja"]
			logger.info(f"langs={langs}")

			#  stream.filter(locations=loc_western, languages=["en","pt","es"])
			#  stream.filter(languages=["en","pt","es"])
			#  stream.filter(locations=loc_western)
			#  stream.filter(locations=loc_brazil)
			#  stream.filter(locations=loc_brazil, filter_level=None)
			#  stream.filter(locations=loc_western, filter_level=None)

			#  tweets_listener.filter(locations=loc_western, filter_level=None)
			#  tweets_listener.filter(locations=loc_brazil, languages=["pt"])
			#  tweets_listener.filter(locations=loc_western, languages=langs)
			
			#  print("traking by palindrome")
			#  t1 = tweets_listener.filter(track=["palindrom"] , languages=langs, threaded=True)
			#  t2 = tweets_listener.filter(locations=loc_brazil, languages=langs, threaded=True)
			#  t.start()
			#  tweets_listener.filter(track=["palindromo"])

			#  tweets_listener.filter(track=["palindromo","palindromos", "palindrome", "palindromes"], locations=loc_western, languages=langs)
			tweets_listener.filter(locations=loc_western, languages=langs)

		except KeyboardInterrupt as e:
			logger.info(e)
			logger.info("\nBye :)")
			break

		except Exception as e:
			logger.info(e)
			time = datetime.now().time().strftime("%H:%M:%S")
			logger.info("\n======================================================================")
			logger.info(f"[{time}]")
			logger.info("Restarting stream\n")
			continue



start_stream()






#  ================================================================================
#  https://twittercommunity.com/t/create-thread-with-tweepy/133853
#  https://auth0.com/blog/how-to-make-a-twitter-bot-in-python-using-tweepy/
#  https://stackoverflow.com/questions/48319243/tweepy-streaming-api-full-text/48326929
#  https://stackoverflow.com/questions/23601634/how-to-restart-tweepy-script-in-case-of-error
#


#  https://developer.twitter.com/en/docs/twitter-api/v1/developer-utilities/supported-languages/api-reference/get-help-languages

	#  api.update_status("Encontrei um palindromo!", attachment_url="https://twitter.com/ovidiojf/status/1442323674946805760")
	# TODO se o úlimo token, mesmo que quebrado, for uma palavra, é legal considerar. -- buscar em um dicionário
	# TODO  Se já twitado ou dado like, responder... 
	# TODO  Se o palindromo for parte do user name, fazer algo diferente
	# TODO  Salvar um csv com tweets médios em suspensão. Depois usar o csv para retuitar
	# TODO  MENTIONS!! Muitos replys são mentions
	# TODO  Quando não tiver a hashtag, diferenciar a mensagem. "Você sabe oque é um palindromo?"


#
			#  text+= "#palindromer\n"
			#  text+= "#palindroseeker\n"
			#  text+= "#palindrohunter\n"
			#  text+= "#palindromo\n"
			#  text+= "#palindrome\n"
			#  text+= "#bot\n"
