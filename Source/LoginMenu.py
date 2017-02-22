from TerminalMenu import TerminalMenu
from TerminalForm import TerminalForm, FormField
from IDGenerator import IDGenerator

class LoginMenu:
	"""The login/signup menu for the terminal interface"""

	_SIGN_IN_INDEX = 0
	_SIGN_UP_INDEX = 1

	_MENU_OPTIONS = ("Sign in", "Sign up")

	_FORM_FIELDS = [FormField("Password", 4), FormField("Name", 20),
		FormField("Email", 15), FormField("City", 12),
		FormField("Timezone", isNumeric = True)]

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

			# If invalid login, got to main login/sign up menu with error
			# message
			if userID is None:
				return LoginMenu._showAndGet(cursor, True)

			return userID

		# If "Sign up" chosen
		else:

			form = TerminalForm(LoginMenu._FORM_FIELDS)
			values = signUpForm.showAndGet()

			# If form submitted, add user to table and return user ID
			if values.submitted:

				userID = IDGenerator.getNewUserID(cursor)

				TableTools.addUser(values[0], values[1], values[2],
					values[3], values[4], userID)

				return userID

			# If an exit key was pressed, return None
			elif values.exitKeyPressed:
				return None

			# If the cancel option was chosen, go to main login/sign up menu
			else:
				return LoginMenu._showAndGet(cursor, True)

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

# Interactive test
if __name__ == "__main__":

	from OracleTerminalConnection import OracleTerminalConnection

	# Fix: connection is None

	# Get connection to database and cursor
	connection = OracleTerminalConnection.connect()
	cursor = connection.cursor()

	user = LoginMenu.getUser(cursor)
	print(user)

	connection.close()