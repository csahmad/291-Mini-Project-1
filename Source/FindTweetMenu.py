import re

from TableTools import TweetsTableTools
from TweetsMenu import TweetsMenu
from TerminalInterface import TerminalInterface

class FindTweetMenu:
	"""Interface for searching for a tweet"""

	BACK_INDEX = 0
	_EMPTY_MESSAGE = "No matches"

	def __init__(self, connection, userID):
		"""
		Arguments:
		userID -- the user ID of the signed in user
		"""

		self._connection = connection
		self._userID = userID

	def showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		FindTweetMenu.BACK_INDEX
		"""

		keywords = input("Enter keywords:")

		if keywords == "":
			TerminalInterface.alert("Empty search dismissed")
			return FindTweetMenu.BACK_INDEX

		tweetGeneratorMethod = lambda: TweetsTableTools.findTweets(
			self._connection, re.split("\s|\s*,\s*", keywords))

		menu = TweetsMenu(self._connection, self._userID, tweetGeneratorMethod,
			emptyMessage = FindTweetMenu._EMPTY_MESSAGE)

		choice = menu.showAndGet()

		if choice == TweetsMenu.BACK_INDEX:
			return FindTweetMenu.BACK_INDEX

		return choice

# Interactive test
if __name__ == "__main__":

	from OracleTerminalConnection import OracleTerminalConnection
	from LoginMenu import LoginMenu

	# Get connection to database
	connection = OracleTerminalConnection.connect()

	user = LoginMenu.getUser(connection)

	menu = FindTweetMenu(connection, user)
	print(menu.showAndGet())

	connection.close()