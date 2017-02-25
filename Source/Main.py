from OracleTerminalConnection import OracleTerminalConnection
from LoginMenu import LoginMenu
from TerminalInterface import TerminalInterface
from MainMenu import MainMenu

class Main:
	"""Run the program"""

	_EXIT_MESSAGE = "Bye"

	@staticmethod
	def main(commitChanges = False):
		"""Run the program"""

		# Get connection to database and cursor
		connection = OracleTerminalConnection.connect()
		cursor = connection.cursor()

		Main._loginAndRun(cursor)        # Run

		# Commit and exit
		Main._showExitMessage()
		if commitChanges: connection.commit()
		connection.close()

	@staticmethod
	def _loginAndRun(cursor):
		"""Let the user login/sign up and run the main menu"""

		result = MainMenu.BACK_INDEX

		while result == MainMenu.BACK_INDEX:
			result = Main._loginAndRun_(cursor)

		return

	@staticmethod
	def _loginAndRun_(cursor):
		"""
		Let the user login/sign up and run the main menu

		Return either MainMenu.BACK_INDEX (if the user chose to logout) or
		None (if the user chose to exit)
		"""

		user = LoginMenu.getUser(cursor)

		# If an exit key was pressed, return None
		if user is None: return None

		# Run the main menu
		mainMenu = MainMenu(cursor, user)
		result = mainMenu.showAndGet()

		# If the user chose to logout, return MainMenu.BACK_INDEX
		return MainMenu.BACK_INDEX

	@staticmethod
	def _showExitMessage():
		"""Show the exit message"""

		TerminalInterface.tryClear()
		print(Main._EXIT_MESSAGE)

if __name__ == "__main__":
	Main.main()