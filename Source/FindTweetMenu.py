import re

from GeneratorTools import GeneratorTools
from TweetsTableTools import TweetsTableTools

class FindTweetMenu:
	"""Interface for searching for a tweet"""

	NOT_EXIT = 1

	def __init__(self, cursor, userID):
		"""
		Arguments:
		userID -- the user ID of the signed in user
		"""

		self._cursor = cursor
		self._userID = userID
		self._tweetGenerator = None
		self._displayedTweets = None

	def showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		FindTweetMenu.NOT_EXIT
		"""

		keywords = input("Enter keywords:")

		self._tweetGenerator = TweetsTableTools.findTweets(self._cursor,
			re.split("\s", keywords))

		self._getNextTweets()
		if self._displayedTweets is None: self._displayedTweets = []

		self._showAndGet()

	def _showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		FindUserMenu.NOT_EXIT
		"""

		pass

	def _getNextTweets(self, amount = 5):
		"""Store the next few tweets or None if no more"""

		self._displayedTweets = GeneratorTools.next(self._tweetGenerator,
			amount)

		if len(self._displayedTweets) == 0:
			self._displayedTweets = None

# Interactive test
if __name__ == "__main__":

	from OracleTerminalConnection import OracleTerminalConnection
	from LoginMenu import LoginMenu

	# Get connection to database and cursor
	connection = OracleTerminalConnection.connect()
	cursor = connection.cursor()

	user = LoginMenu.getUser(cursor)

	menu = FindTweetMenu(cursor, user)
	print(menu.showAndGet())

	connection.close()