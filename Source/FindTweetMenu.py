import re

from TableTools import TweetsTableTools
from TweetsMenu import TweetsMenu

class FindTweetMenu:
	"""Interface for searching for a tweet"""

	BACK_INDEX = 0
	_EMPTY_MESSAGE = "No matches"

	def __init__(self, cursor, userID):
		"""
		Arguments:
		userID -- the user ID of the signed in user
		"""

		self._cursor = cursor
		self._userID = userID

	def showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		FindTweetMenu.BACK_INDEX
		"""

		keywords = input("Enter keywords:")
		tweetGenerator = TweetsTableTools.findTweets(self._cursor,
			re.split("\s|\s*,\s*", keywords))

		menu = TweetsMenu(self._cursor, self._userID, tweetGenerator,
			emptyMessage = FindTweetMenu._EMPTY_MESSAGE)

		choice = menu.showAndGet()

		if choice == TweetsMenu.BACK_INDEX:
			return FindTweetMenu.BACK_INDEX

		return choice

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