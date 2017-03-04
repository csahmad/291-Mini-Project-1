import re

from TableTools import UsersTableTools
from UsersMenu import UsersMenu
from TerminalInterface import TerminalInterface

class FindUserMenu:
	"""Interface for searching for a user"""

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
		FindUserMenu.BACK_INDEX
		"""

		keywords = input("Enter keywords:")

		if keywords == "":
			TerminalInterface.alert("Empty search dismissed")
			return FindUserMenu.BACK_INDEX

		userGeneratorMethod = lambda: UsersTableTools.findUsers(
			self._connection, re.split("\s|\s*,\s*", keywords))

		menu = UsersMenu(self._connection, self._userID, userGeneratorMethod,
			emptyMessage = FindUserMenu._EMPTY_MESSAGE)

		choice = menu.showAndGet()

		if choice == UsersMenu.BACK_INDEX:
			return FindUserMenu.BACK_INDEX

		return choice

# Interactive test
if __name__ == "__main__":

	from OracleTerminalConnection import OracleTerminalConnection
	from LoginMenu import LoginMenu

	# Get connection to database
	connection = OracleTerminalConnection.connect()

	user = LoginMenu.getUser(connection)

	menu = FindUserMenu(connection, user)
	print(menu.showAndGet())

	connection.close()