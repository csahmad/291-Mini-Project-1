class FindTweetMenu:
	"""Interface for searching for a tweet"""

	def __init__(self, cursor, userID):
		"""
		Arguments:
		userID -- the user ID of the signed in user
		"""

		self._cursor = cursor
		self._userID = userID

	def showAndGet(self):
		"""I"""

		pass