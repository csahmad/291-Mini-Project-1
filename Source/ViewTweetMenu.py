from TableTools import TweetsTableTools
from TerminalMenu import TerminalMenu
from IDGenerator import IDGenerator
from DateTools import DateTools
from TerminalInterface import TerminalInterface
from TweetTools import TweetTools

class ViewTweetMenu:
	"""The menu for viewing a tweet and replying to it or retweeting it"""

	BACK_INDEX = 0
	_REPLY_INDEX = 1
	_RETWEET_INDEX = 2
	_INITIAL_INDEX = -1

	_OPTIONS_WITHOUT_RETWEET = ["Back", "Reply"]
	_OPTIONS = ["Back", "Reply", "Retweet"]

	def __init__(self, connection, userID, tweet):

		self._connection = connection
		self._userID = userID
		self._isRetweetedByUser = TweetsTableTools.isRetweetedByUser(
			connection, tweet.tweetID, userID)

		self._tweet = tweet
		self._tweetStats = TweetsTableTools.getTweetStats(connection,
			tweet.tweetID)
		self._tweetString = None

	def showAndGet(self):
		"""
		Show the menu and return either ViewTweetMenu.BACK_INDEX (if back
		option chosen) or None (if an exit key was pressed)
		"""

		choice = ViewTweetMenu._INITIAL_INDEX

		while choice == ViewTweetMenu._INITIAL_INDEX:
			choice = self._showAndGet()

		return choice

	def _showAndGet(self):
		"""
		Show the menu and return either ViewTweetMenu.BACK_INDEX (if back
		option chosen) or None (if an exit key was pressed)
		"""

		self._tweetString = str(self._tweet) + "\n\t" + str(self._tweetStats)

		if self._isRetweetedByUser:

			preMessage = self._tweetString + "\n\t" + \
				"You have retweeted this"

			options = ViewTweetMenu._OPTIONS_WITHOUT_RETWEET

		else:
			preMessage = self._tweetString
			options = ViewTweetMenu._OPTIONS

		menu = TerminalMenu(options, preMessage)
		choice = menu.showAndGet()

		# If an exit key was pressed, return None
		if choice is None: return None

		# If user chose to go back, return ViewTweetMenu.BACK_INDEX
		if choice == ViewTweetMenu.BACK_INDEX:
			return ViewTweetMenu.BACK_INDEX

		# If user chose to reply to the tweet, let user write reply
		if choice == ViewTweetMenu._REPLY_INDEX:
			self._reply()

		# If user chose to retweet the tweet, retweet
		elif choice == ViewTweetMenu._RETWEET_INDEX:
			self._retweet()

		return ViewTweetMenu._INITIAL_INDEX

	def _reply(self):
		"""Let the user reply to the tweet"""

		TerminalInterface.tryClear()
		replyText = input("Reply:")

		if replyText == "":
			TerminalInterface.alert("Empty tweet discarded")
			return

		hashtags = TweetTools.getHashtags(replyText)
		tweet = self._tweet
		replyTweetID = IDGenerator.getNewTweetID(self._connection)
		replyDate = DateTools.getCurrentDate()
		TweetsTableTools.addTweet(self._connection, self._userID, replyDate,
			replyText, replyTweetID, tweet.tweetID, hashtags)
		self._tweetStats.addReply()

	def _retweet(self):
		"""Retweet the tweet"""

		retweetDate = DateTools.getCurrentDate()
		tweet = self._tweet
		TweetsTableTools.retweet(self._connection, tweet.tweetID, self._userID,
			retweetDate)
		self._isRetweetedByUser = True
		self._tweetStats.addRetweet()