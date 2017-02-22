from TableMethods import TableMethods

class IDGenerator:
	"""Generate unique values for columns in tables"""

	@staticmethod
	def getUniqueInt(cursor, tableName, columnName)
		"""
		Return an integer that is not in the given column of the given table
		"""

		unique = 0

		while TableTools.stringExists(cursor, tableName, columnName, unique):
			unique += 1

		return unique