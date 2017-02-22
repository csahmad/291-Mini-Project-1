from TableTools import TableTools

class IDGenerator:
	"""Generate unique values for columns in tables"""

	@staticmethod
	def getNewUserID(cursor):
		"""Return a user ID that does not exist in the Users table"""

		return IDGenerator.getNewInt(cursor, "Users", "usr")

	@staticmethod
	def getNewInt(cursor, tableName, columnName):
		"""
		Return an integer that is not in the given column of the given table
		"""

		unique = 0

		while TableTools.itemExists(cursor, tableName, columnName, unique):
			unique += 1

		return unique