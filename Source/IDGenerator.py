from TableTools import TableTools

class IDGenerator:
	"""Generate unique values for columns in tables"""

	@staticmethod
	def getNewTweetID(cursor):
		"""Return a tweet ID that does not exist in the Tweets table"""

		return IDGenerator.getNewInt(cursor, "Tweets", "tid")

	@staticmethod
	def getNewUserID(cursor):
		"""Return a user ID that does not exist in the Users table"""

		return IDGenerator.getNewInt(cursor, "Users", "usr")

	@staticmethod
	def getNewInt(cursor, tableName, columnName = None):
		"""
		Return an integer that is not in the given column of the given table

		If no column name given, assume table only has one column
		"""

		unique = 0

		while TableTools.itemExists(cursor, tableName, unique, columnName):
			unique += 1

		return unique