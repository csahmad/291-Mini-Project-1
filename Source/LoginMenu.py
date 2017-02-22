from TerminalMenu import TerminalMenu
from TerminalForm import TerminalForm

class LoginMenu:
	"""The login/signup menu for the terminal interface"""

	_SIGN_IN_INDEX = 0
	_SIGN_UP_INDEX = 1

	_MENU_OPTIONS = ("Sign in", "Sign up")

	_FORM_FIELDS = [Field("Password", 4), Field("Name", 20),
		Field("Email", 15), Field("City", 12),
		Field("Timezone", isNumeric = True)]

	@staticmethod
	def getUser(cursor):
		"""
		Show the menu and return the user ID or None (if an exit key is
		pressed)
		"""

		return LoginMenu._showAndGet(cursor)

	@staticmethod
	def _showAndGet(cursor, loginFailed = False):
		"""
		Show the menu and return the user ID or None (if an exit key is
		pressed)

		Keyword arguments:
		loginFailed -- whether the user just made a failed login attempt
		"""

		if loginFailed:
			preMessage = "Invalid username or password"

		else:
			preMessage = ""

		menu = TerminalMenu(LoginMenu._MENU_OPTIONS, preMessage)
		choice = menu.showAndGet()

		# If the user pressed an exit button, return None
		if choice is None: return None

		# If "Sign in" chosen
		if choice == LoginMenu._SIGN_IN_INDEX:

			userID = LoginMenu._login(cursor)

			if userID is None:
				return LoginMenu._showAndGet(cursor, True)

			return userID

		# If "Sign up" chosen
		else:

			signUpForm = TerminalForm(LoginMenu._FORM_FIELDS)
			signUpInfo = signUpForm.showAndGet()

			if signUpInfo.submitted:

				pass

	@staticmethod
	def _login(cursor):
		"""
		Let the user login and return the user ID or None (if login failed)
		"""

		userString, password = TerminalInterface.login(integerUsername = True)
		userID = int(userString)

		if UsersTableTools.loginExists(cursor, userID, password):
			return userID

		return None