from TableTools import TweetsTableTools

class ViewTweetMenu:
	"""The menu for viewing a tweet and replying to it or retweeting it"""

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

		pass