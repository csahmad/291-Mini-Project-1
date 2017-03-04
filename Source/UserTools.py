class User:
	"""Represents a user"""

	def __init__(self, userID, name, email, city, timezone):

		self._userID = userID
		self._name = name
		self._email = email
		self._city = city
		self._timezone = timezone

	def __str__(self):

		return "[{0}] {1}".format(self._userID, self._name)

	@property
	def userID(self):

		return self._userID

	@property
	def name(self):

		return self._name

	@property
	def email(self):

		return self._email

	@property
	def city(self):

		return self._city

	@property
	def timezone(self):

		return self._timezone

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

	def __str__(self):

		return "{0} Tweets | {1} Following | {2} Followers".format(
			self._tweetCount, self._followingCount, self._followerCount)

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