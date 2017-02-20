import cx_Oracle

from Constants import Constants
from TerminalInterface import TerminalInterface
from OracleConnection import OracleConnection

class OracleTerminalConnection:
	"""For connecting to Oracle with a terminal interface"""

	@staticmethod
	def connect():
		"""Connect to Oracle with a terminal interface"""

		# Get username and password for database
		username, password = TerminalInterface.login("Database username:",
			"Database password:")

		# Tell user to wait
		TerminalInterface.tryClear()
		print("Please wait (connecting)")

		# Connect using given username and password and return connection
		try:

			connection = OracleConnection.connect(username, password)

			TerminalInterface.tryClear()
			print("Connected")
			return connection

		# On error, show error message and prompt user to press enter to retry
		except cx_Oracle.DatabaseError as error:
			TerminalInterface.tryClear()
			print("Could not connect (press enter to retry)")
			print("\n")
			print("Connection string:")
			print(Constants.CONNECTION_STRING)
			print("\n")
			print("Error:")
			print(error)
			input("")
			OracleTerminalConnection.connect()

if __name__ == "__main__":
	OracleTerminalConnection.connect()