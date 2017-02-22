from OracleTerminalConnection import OracleTerminalConnection
from LoginScreen import LoginScreen

class Main:
	"""Run the program"""

	@staticmethod
	def main():
		"""Run the program"""

		# Get connection to database and cursor
		connection = OracleTerminalConnection.connect()
		cursor = connection.cursor()

		user = LoginMenu.getUser(cursor)

		pass

		connection.close()

if __name__ == "__main__":
	Main.main()