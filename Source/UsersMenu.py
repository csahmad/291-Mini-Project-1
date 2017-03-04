from TerminalMenu import TerminalGeneratorMenu
from ViewUserMenu import ViewUserMenu

class UsersMenu:
	"""A menu for viewing users from a user ID generator"""

	BACK_INDEX = 0
	_INITIAL_INDEX = -1

	def __init__(self, connection, userID, userGeneratorMethod,
		preMessage = None, emptyMessage = "No users"):
		"""
		Arguments:
		userID -- the user ID of the signed in user
		userGeneratorMethod -- the method to call to get the User generator as
			a lambda with arguments
		preMessage -- the message to show before the listed users
		empytMessage -- the message to display if the generator yields nothing
		"""

		self._connection = connection
		self._userID = userID
		self._userGeneratorMethod = userGeneratorMethod
		self._preMessage = preMessage
		self._emptyMessage = emptyMessage
		self._menu = None

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

		userGenerator = self._userGeneratorMethod()

		menu = TerminalGeneratorMenu(userGenerator,
			preMessage = self._preMessage, emptyMessage = self._emptyMessage)

		result = menu.showAndGet()

		# If an exit key was pressed, return None
		if result is None: return None

		# If the back option was chosen, return UsersMenu.BACK_INDEX
		if result.backWasChosen: return UsersMenu.BACK_INDEX

		# If a user was chosen, view the user
		else:
			viewUserMenu = ViewUserMenu(self._connection, self._userID,
				result.chosenItem)
			result = viewUserMenu.showAndGet()
			if result is None: return None        # If an exit key was pressed

		return UsersMenu._INITIAL_INDEX