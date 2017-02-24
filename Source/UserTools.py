class UserStats:
	"""Contains stats for a user"""

	def __init__(self, tweetCount, followingCount, followerCount):
		"""
		Arguments:
		tweetCount -- the number of tweets from this user
		followingCount -- the number of people this user is following
		followerCount -- the number of people following this user
		"""

		self._tweetCount = tweetCount
		self._followingCount = followingCount
		self._followerCount = followerCount

	@property
	def tweetCount(self):

		return self._tweetCount

	@property
	def followingCount(self):

		return self._followingCount

	@property
	def followerCount(self):

		return self._followerCount

	def follow(self):
		"""Add 1 to followerCount"""

		self._followerCount += 1