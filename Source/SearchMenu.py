from TerminalMenu import TerminalMenu

class SearchMenu:
	"""The menu for searching for tweets or users"""

	_FIND_TWEET_INDEX = 0
	_FIND_USER_INDEX = 1
	BACK_INDEX = 2

	def __init__(cursor, userID):

		self._userID = userID

	def showAndGet(self):
		"""
		Show the search menu and return either SearchMenu.BACK_INDEX (if the
		user chose the "back" option) or None (if an exit key was pressed)
		"""

		menu = TerminalMenu(["Find a tweet", "Find a user"])
		choice = menu.showAndGet()

		# If an exit key was pressed, return None
		if choice is None: return None

		# If the user chose to find a tweet, let the user search for a tweet
		if choice == SearchMenu._FIND_TWEET_INDEX:
			pass

		# If the user chose to find a user, let the user search for a user
		elif choice == SearchMenu._FIND_USER_INDEX:
			pass

		# If the user chose to go back, return SearchMenu.BACK_INDEX
		else:
			return SearchMenu.BACK_INDEX

		return self.showAndGet()