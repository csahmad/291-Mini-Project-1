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

		user = LoginMenu.getUser(cursor)

		# If an exit key was pressed, show exit message and exit
		if user is None:
			Main._showExitMessage()
			return

		mainMenu = MainMenu(cursor, user)
		result = mainMenu.showAndGet()

		if result == MainMenu.LOGOUT_INDEX:
			pass

		Main._showExitMessage()

		connection.close()

	@staticmethod
	def _showExitMessage():
		"""Show the exit message"""

		TerminalInterface.tryClear()
		print(Main._EXIT_MESSAGE)

if __name__ == "__main__":
	Main.main()