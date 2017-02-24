from UsersMenu import UsersMenu
from TableTools import FollowsTableTools

class FollowersMenu:
	"""A menu for viewing the followers of a user"""

	BACK_INDEX = 0
	_EMPTY_MESSAGE = "No followers"

	def __init__(cursor, userID):

		self._cursor = cursor
		self._userID = userID

	def showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		FollowersMenu.BACK_INDEX
		"""

		userIDGenerator = FollowsTableTools.getFollowers(self._cursor,
			self._userID)

		menu = UsersMenu(self._cursor, self._userID, userIDGenerator,
			emptyMessage = FollowersMenu._EMPTY_MESSAGE)

		choice = menu.showAndGet()

		if choice == UsersMenu.BACK_INDEX:
			return FollowersMenu.BACK_INDEX

		return choice

# Interactive test
if __name__ == "__main__":

	from OracleTerminalConnection import OracleTerminalConnection
	from LoginMenu import LoginMenu

	# Get connection to database and cursor
	connection = OracleTerminalConnection.connect()
	cursor = connection.cursor()

	user = LoginMenu.getUser(cursor)

	menu = FollowersMenu(cursor, user)
	print(menu.showAndGet())

	connection.close()