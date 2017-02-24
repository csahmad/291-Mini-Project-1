import re

from TableTools import TweetsTableTools
from TerminalMenu import TerminalGeneratorMenu

class FindTweetMenu:
	"""Interface for searching for a tweet"""

	BACK_INDEX = 0
	_INITIAL_INDEX = -1

	_EMPTY_MESSAGE = "No matches"

	def __init__(self, cursor, userID):
		"""
		Arguments:
		userID -- the user ID of the signed in user
		"""

		self._cursor = cursor
		self._userID = userID
		self._resultsGenerator = None

	def showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		FindTweetMenu.BACK_INDEX
		"""

		keywords = input("Enter keywords:")
		self._resultsGenerator = TweetsTableTools.findTweets(self._cursor,
			re.split("\s|\s*,\s*", keywords))

		choice = FindTweetMenu._INITIAL_INDEX

		while choice is not None and choice != FindTweetMenu.BACK_INDEX:
			choice = self._showAndGet()

		return choice

	def _showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		FindTweetMenu.BACK_INDEX
		"""

		menu = TerminalGeneratorMenu(self._resultsGenerator,
			emptyMessage = FindTweetMenu._EMPTY_MESSAGE)

		result = menu.showAndGet()

		# If an exit key was pressed, return None
		if result is None: return None

		# If the back option was chosen, return FindTweetMenu.BACK_INDEX
		if result.backWasChosen: return FindTweetMenu.BACK_INDEX

		# If a tweet was chosen, view the tweet
		else:
			viewTweetMenu = ViewTweetMenu(cursor, self._userID,
				result.chosenItem)
			result = viewTweetMenu.showAndGet()
			if result is None: return None        # If an exit key was pressed

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