from TerminalMenu import TerminalMenu
from FindTweetMenu import FindTweetMenu
from FindUserMenu import FindUserMenu
from TerminalInterface import TerminalInterface

class SearchMenu:
	"""The menu for searching for tweets or users"""

	_FIND_TWEET_INDEX = 0
	_FIND_USER_INDEX = 1
	BACK_INDEX = 2
	_INITIAL_INDEX = -1

	def __init__(self, connection, userID):

		self._connection = connection
		self._userID = userID

	def showAndGet(self):
		"""
		Show the search menu and return either SearchMenu.BACK_INDEX (if the
		user
		"""

		choice = SearchMenu._INITIAL_INDEX

		while choice == SearchMenu._INITIAL_INDEX:
			choice = self._showAndGet()

		return choice

	def _showAndGet(self):
		"""
		Show the search menu and return either SearchMenu.BACK_INDEX (if the
		user chose the "back" option) or None (if an exit key was pressed)
		"""

		menu = TerminalMenu(["Find a tweet", "Find a user", "Back"])
		choice = menu.showAndGet()

		# If an exit key was pressed, return None
		if choice is None: return None

		# If the user chose to find a tweet, let the user search for a tweet
		if choice == SearchMenu._FIND_TWEET_INDEX:
			choice = self._findTweet()
			if choice is None: return None
			return SearchMenu.BACK_INDEX

		# If the user chose to find a user, let the user search for a user
		elif choice == SearchMenu._FIND_USER_INDEX:
			choice = self._findUser()
			if choice is None: return None
			return SearchMenu.BACK_INDEX

		# If the user chose to go back, return SearchMenu.BACK_INDEX
		else:
			return SearchMenu.BACK_INDEX

		return SearchMenu._INITIAL_INDEX

	def _findTweet(self):
		"""Let the user enter a keyword and find matching tweets"""

		TerminalInterface.tryClear()
		menu = FindTweetMenu(self._connection, self._userID)
		return menu.showAndGet()

	def _findUser(self):
		"""Let the user enter a keyword and find matching users"""

		TerminalInterface.tryClear()
		menu = FindUserMenu(self._connection, self._userID)
		return menu.showAndGet()

# Interactive test
if __name__ == "__main__":

	from OracleTerminalConnection import OracleTerminalConnection
	from LoginMenu import LoginMenu

	# Get connection to database
	connection = OracleTerminalConnection.connect()

	user = LoginMenu.getUser(connection)

	searchMenu = SearchMenu(connection, user)
	print(searchMenu.showAndGet())

	connection.close()
