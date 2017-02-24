import re

class TweetTools:
	"""Tools for tweets"""

	@staticmethod
	def getHashtags(tweetText):
		"""Extract and return the hashtags in the given tweet text as a list"""

		hashtags = re.findall("\#\w+", tweetText)

		# Remove "#"s and return
		return [hashtag[1:] for hashtag in hashtags]

class Tweet:
	"""Represents a tweet"""

	def __init__(self, tweetID, writer, date, text, replyTo = None):

		if replyTo == "null": replyTo = None
		self._tweetID = tweetID
		self._writer = writer
		self._date = date
		self._text = text
		self._replyTo = replyTo

	def __str__(self):

		if self._replyTo is None:
			replyToString = ""

		else:
			replyToString = "@{0} ".format(self._replyTo)

		return "{0}: {1}{2} ({3})".format(self._writer, replyToString,
			self._text, self._date)

	@property
	def tweetID(self):
		"""Return the tweet ID"""

		return self._tweetID

	@property
	def writer(self):
		"""Return the writer of the tweet"""

		return self._writer

	@property
	def date(self):
		"""Return the date the tweet was written"""

		return self._date

	@property
	def text(self):
		"""Return the tweet text"""

		return self._text

	@property
	def replyTo(self):
		"""Return the tweet ID this tweet is a reply to or None"""

		return self._replyTo

class TweetStats:
	"""Contains stats for a tweet"""

	def __init__(self, retweetCount, replyCount):

		self._retweetCount = retweetCount
		self._replyCount = replyCount

	def __str__(self):

		return "{0} Retweets | {1} Replies".format(self._retweetCount,
			self._replyCount)

	@property
	def retweetCount(self):
		"""Get the number of retweets"""

		return self._retweetCount

	@property
	def replyCount(self):
		"""Get the number of replies"""

		return self._replyCount

	def addRetweet(self):
		"""Increase retweet count by one"""

		self._retweetCount += 1

	def addReply(self):
		"""Increase reply count by one"""

		self._replyCount += 1