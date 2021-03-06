from TerminalMenu import TerminalMenu
from TerminalForm import TerminalForm, FormField
from TerminalInterface import TerminalInterface
from IDGenerator import IDGenerator
from TableTools import UsersTableTools

class LoginMenu:
	"""The login/signup menu for the terminal interface"""

	_SIGN_IN_INDEX = 0
	_SIGN_UP_INDEX = 1
	_INITIAL_INDEX = -1

	_MENU_OPTIONS = ("Sign in", "Sign up", "Exit")

	_FORM_FIELDS = [FormField("*Password", 4, isRequired = True),
		FormField("Name", 20), FormField("Email", 15), FormField("City", 12),
		FormField("Timezone", isNumeric = True)]

	@staticmethod
	def getUser(connection):
		"""
		Show the menu and return the user ID or None (if an exit key is
		pressed)
		"""

		return LoginMenu._showAndGet(connection)

	@staticmethod
	def _showAndGet(connection, loginFailed = False):
		"""
		Show the menu and return the user ID or None (if an exit key is
		pressed)

		Arguments:
		loginFailed -- whether the user just made a failed login attempt
		"""

		if loginFailed:
			preMessage = "Invalid username or password"

		else:
			preMessage = "Welcome to Twitter"

		menu = TerminalMenu(LoginMenu._MENU_OPTIONS, preMessage)
		choice = menu.showAndGet()

		# If the user pressed an exit button, return None
		if choice is None: return None

		# If "Sign in" chosen
		if choice == LoginMenu._SIGN_IN_INDEX:

			userID = LoginMenu._login(connection)

			# If invalid login, got to main login/sign up menu with error
			# message
			if userID is None:
				return LoginMenu._showAndGet(connection, True)

			return userID

		# If "Sign up" chosen
		elif choice == LoginMenu._SIGN_UP_INDEX:

			form = TerminalForm(LoginMenu._FORM_FIELDS)
			result = form.showAndGet()

			# If form submitted, add user to table and return user ID
			if result.submitted:

				userID = IDGenerator.getNewUserID(connection)
				values = result.values

				UsersTableTools.addUser(connection, values["*Password"],
					values["Name"], values["Email"], values["City"],
					values["Timezone"], userID)

				TerminalInterface.alert("Thank you for registering {0}!\n your Login user ID: {1}\n".format(values["Name"], userID))

				return userID

			# If an exit key was pressed, return None
			elif values.exitKeyPressed:
				return None

			# If the cancel option was chosen, go to main login/sign up menu
			else:
				return LoginMenu._showAndGet(connection, True)

		# If "Exit" chosen
		else:
			return None

	@staticmethod
	def _login(connection):
		"""
		Let the user login and return the user ID or None (if login failed)
		"""

		userString, password = TerminalInterface.login("user id:",
			integerUsername = True)
		userID = int(userString)

		if UsersTableTools.loginExists(connection, userID, password):
			return userID

		return None

# Interactive test
if __name__ == "__main__":

	from OracleTerminalConnection import OracleTerminalConnection

	# Get connection to database
	connection = OracleTerminalConnection.connect()

	user = LoginMenu.getUser(connection)
	print(user)

	connection.close()
