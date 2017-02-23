from OracleTerminalConnection import OracleTerminalConnection
from LoginMenu import LoginMenu
from TerminalInterface import TerminalInterface
from MainMenu import MainMenu

class Main:
	"""Run the program"""

	_EXIT_MESSAGE = "Bye"

	@staticmethod
	def main():
		"""Run the program"""

		# Get connection to database and cursor
		connection = OracleTerminalConnection.connect()
		cursor = connection.cursor()

		Main._loginAndRun(cursor)        # Run

		# Exit
		Main._showExitMessage()
		connection.close()

	@staticmethod
	def _loginAndRun(cursor):
		"""Let the user login/sign up and run the main menu"""

		user = LoginMenu.getUser(cursor)

		# If an exit key was pressed, return
		if user is None: return

		# Run the main menu
		mainMenu = MainMenu(cursor, user)
		result = mainMenu.showAndGet()

		# If the user signed out, let the user sign in again or sign up, then
		# run the main menu again
		if result == MainMenu.LOGOUT_INDEX:
			Main._loginAndRun(cursor)

	@staticmethod
	def _showExitMessage():
		"""Show the exit message"""

		TerminalInterface.tryClear()
		print(Main._EXIT_MESSAGE)

if __name__ == "__main__":
	Main.main()