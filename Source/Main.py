from OracleTerminalConnection import OracleTerminalConnection
from LoginScreen import LoginScreen

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
			print Main._EXIT_MESSAGE
			return

		pass

		connection.close()

if __name__ == "__main__":
	Main.main()