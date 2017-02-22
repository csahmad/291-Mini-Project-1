import cx_Oracle

from Constants import Constants

class OracleConnection:
	"""Connect to an Oracle database."""

	@staticmethod
	def connect(username, password, connectionString = None):
		"""
		Get a connection to an Oracle database.

		Does not handle exceptions (this should be done by the terminal
		interface classes that call this method).

		Keyword arguments:
		username -- your username for the Oracle database
		password -- your password for the Oracle database
		connectionString -- the connection string (if None, use settings in
		Constants)
		"""

		# If no connection string provided, use settings in Constants
		if connectionString is None:
			connectionString = Constants.CONNECTION_STRING

		return cx_Oracle.connect(username, password, connectionString)