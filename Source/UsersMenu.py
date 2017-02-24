from TerminalMenu import TerminalGeneratorMenu
from ViewUserMenu import ViewUserMenu

class UsersMenu:
	"""A menu for viewing users from a user ID generator"""

	BACK_INDEX = 0
	_INITIAL_INDEX = -1

	def __init__(self, cursor, userID, userIDGenerator, preMessage = None,
		emptyMessage = "No users"):
		"""
		Arguments:
		userID -- the user ID of the signed in user
		userIDGenerator -- a generator that yields user IDs
		preMessage -- the message to show before the listed users
		empytMessage -- the message to display if the generator yields nothing
		"""

		self._cursor = cursor
		self._userID = userID
		self._userIDGenerator = userIDGenerator
		self._preMessage = preMessage
		self._emptyMessage = emptyMessage

	def showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		UsersMenu.BACK_INDEX
		"""

		choice = UsersMenu._INITIAL_INDEX

		while choice == UsersMenu._INITIAL_INDEX:
			choice = self._showAndGet()

		return choice

	def _showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		UsersMenu.BACK_INDEX
		"""

		menu = TerminalGeneratorMenu(self._userIDGenerator,
			preMessage = self._preMessage, emptyMessage = self._emptyMessage)

		result = menu.showAndGet()

		# If an exit key was pressed, return None
		if result is None: return None

		# If the back option was chosen, return UsersMenu.BACK_INDEX
		if result.backWasChosen: return UsersMenu.BACK_INDEX

		# If a user was chosen, view the user
		else:
			viewUserMenu = ViewUserMenu(cursor, self._userID,
				result.chosenItem)
			result = viewUserMenu.showAndGet()
			if result is None: return None        # If an exit key was pressed

		return UsersMenu._INITIAL_INDEX