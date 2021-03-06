from UsersMenu import UsersMenu
from TableTools import FollowsTableTools

class FollowersMenu:
	"""A menu for viewing the followers of a user"""

	BACK_INDEX = 0
	_EMPTY_MESSAGE = "No followers"

	def __init__(self, connection, userID):

		self._connection = connection
		self._userID = userID

		self._userGeneratorMethod = lambda: FollowsTableTools.getFollowers(
			self._connection, self._userID)

	def showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		FollowersMenu.BACK_INDEX
		"""

		menu = UsersMenu(self._connection, self._userID,
			self._userGeneratorMethod,
			emptyMessage = FollowersMenu._EMPTY_MESSAGE)

		choice = menu.showAndGet()

		# If an exit key was pressed, return None
		if choice is None: return None

		# If user chose back option, return FollowersMenu.BACK_INDEX
		return FollowersMenu.BACK_INDEX

# Interactive test
if __name__ == "__main__":

	from OracleTerminalConnection import OracleTerminalConnection
	from LoginMenu import LoginMenu

	# Get connection to database
	connection = OracleTerminalConnection.connect()

	user = LoginMenu.getUser(connection)

	menu = FollowersMenu(connection, user)
	print(menu.showAndGet())

	connection.close()