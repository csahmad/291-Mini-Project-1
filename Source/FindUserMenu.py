import re

from TableTools import UsersTableTools
from TerminalMenu import TerminalGeneratorMenu

class FindUserMenu:
	"""Interface for searching for a user"""

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
		FindUserMenu.BACK_INDEX
		"""

		keywords = input("Enter keywords:")
		self._resultsGenerator = UsersTableTools.findUsers(self._cursor,
			re.split("\s|\s*,\s*", keywords))

		choice = FindUserMenu._INITIAL_INDEX

		while choice is not None and choice != FindUserMenu.BACK_INDEX:
			choice = self._showAndGet()

		return choice

	def _showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		FindUserMenu.BACK_INDEX
		"""

		menu = TerminalGeneratorMenu(self._resultsGenerator,
			emptyMessage = FindUserMenu._EMPTY_MESSAGE)

		result = menu.showAndGet()

		# If an exit key was pressed, return None
		if result is None: return None

		# If the back option was chosen, return FindUserMenu.BACK_INDEX
		if result.backWasChosen: return FindUserMenu.BACK_INDEX

		# If a user was chosen, view the user
		else:
			viewUserMenu = ViewUserMenu(cursor, self._userID,
				result.chosenItem)
			result = viewUserMenu.showAndGet()
			if result is None: return None        # If an exit key was pressed

# Interactive test
if __name__ == "__main__":

	from OracleTerminalConnection import OracleTerminalConnection
	from LoginMenu import LoginMenu

	# Get connection to database and cursor
	connection = OracleTerminalConnection.connect()
	cursor = connection.cursor()

	user = LoginMenu.getUser(cursor)

	menu = FindUserMenu(cursor, user)
	print(menu.showAndGet())

	connection.close()