from TableTools import TweetsTableTools
from TerminalMenu import TerminalMenu

class ViewTweetMenu:
	"""The menu for viewing a tweet and replying to it or retweeting it"""

	_BACK_INDEX = 0
	_REPLY_INDEX = 1
	_RETWEET_INDEX = 2

	_OPTIONS_WITHOUT_RETWEET = ["Back", "Reply"]
	_OPTIONS = ["Back", "Reply", "Retweet"]

	def __init__(cursor, userID, tweet):

		self._userID = userID
		self._retweetedByUser = TweetsTableTools.retweetedByUser(cursor,
			tweet.tweetID, userID)

		self._tweet = tweet
		self._tweetStats = TweetsTableTools.getTweetStats(cursor,
			tweet.tweetID)
		self._tweetString = str(tweet) + "\n\t" + str(self._tweetStats)

	def showAndGet(self):
		"""I"""

		I

	def _showAndGet(self):
		"""I"""

		if self._retweetedByUser:

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

		# If user chose to go back, return choice
		if choice == ViewTweetMenu._BACK_INDEX:
			return choice

		# If user chose to reply to the tweet, let user write reply
		if choice == ViewTweetMenu._REPLY_INDEX:
			replyText = input("Reply:")
			hashtags = TweetTools.getHashtags(replyText)
			#TweetsTableTools.addTweet()

		# If user chose to retweet the tweet, retweet
		elif choice == ViewTweetMenu._RETWEET_INDEX:
			pass