import re

from TableTools import UsersTableTools
from UsersMenu import UsersMenu

class FindUserMenu:
	"""Interface for searching for a user"""

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
		FindUserMenu.BACK_INDEX
		"""

		keywords = input("Enter keywords:")
		userIDGenerator = UsersTableTools.findUsers(self._cursor,
			re.split("\s|\s*,\s*", keywords))

		menu = UsersMenu(self._cursor, self._userID,
			emptyMessage = FindUserMenu._EMPTY_MESSAGE)

		choice = menu.showAndGet(userIDGenerator)

		if choice == UsersMenu.BACK_INDEX:
			return FindUserMenu.BACK_INDEX

		return choice

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