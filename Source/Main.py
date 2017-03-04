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

		connection = OracleTerminalConnection.connect()
		Main._loginAndRun(connection)
		Main._commitAndExit(connection, commitChanges)

	@staticmethod
	def _commitAndExit(connection, commitChanges):
		"""
		Show the exit message and close the connection

		Commit changes if commitChanges True, otherwise rollback
		"""

		Main._showExitMessage()

		if commitChanges:
			connection.commit()

		else:
			connection.rollback()
			print("Changes rolled back")

		connection.close()

	@staticmethod
	def _loginAndRun(connection):
		"""Let the user login/sign up and run the main menu"""

		result = MainMenu.BACK_INDEX

		while result == MainMenu.BACK_INDEX:
			result = Main._loginAndRun_(connection)

	@staticmethod
	def _loginAndRun_(connection):
		"""
		Let the user login/sign up and run the main menu

		Return either MainMenu.BACK_INDEX (if the user chose to logout) or
		None (if the user chose to exit)
		"""

		user = LoginMenu.getUser(connection)

		# If an exit key was pressed, return None
		if user is None: return None

		# Run the main menu
		mainMenu = MainMenu(connection, user)
		result = mainMenu.showAndGet()

		# If an exit key was pressed, return None
		if result is None: return None

		# If the user chose to logout, return MainMenu.BACK_INDEX
		return MainMenu.BACK_INDEX

	@staticmethod
	def _showExitMessage():
		"""Show the exit message"""

		TerminalInterface.tryClear()
		print(Main._EXIT_MESSAGE)

if __name__ == "__main__":
	Main.main()