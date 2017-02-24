from TableTools import UsersTableTools
from GeneratorTools import GeneratorTools

class FindUserMenu:
	"""Interface for searching for a user"""

	NOT_EXIT = 1

	def __init__(self, cursor, userID):
		"""
		Arguments:
		userID -- the user ID of the signed in user
		"""

		self._cursor = cursor
		self._userID = userID
		self._resultsGenerator = None
		self._displayedUsers = None

	def showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		FindUserMenu.NOT_EXIT
		"""

		keyword = input("Enter keyword:")

		self._resultsGenerator = UsersTableTools.findUsers(self._cursor,
			keyword)

		self._getNextUsers()
		if self._displayedUsers is None: self._displayedUsers = []

		self._showAndGet()

	def _showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		FindUserMenu.NOT_EXIT
		"""

		pass

	def _getNextUsers(self, amount = 5):
		"""Store the next few users or None if no more"""

		self._displayedUsers = GeneratorTools.next(self._resultsGenerator,
			amount)

		if len(self._displayedUsers) == 0:
			self._displayedUsers = None

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