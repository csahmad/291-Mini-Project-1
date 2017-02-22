class TableTools:
	"""Static methods for getting information about tables"""

	@staticmethod
	def stringExists(cursor, tableName, columnName, string):
		"""Return whether the given string value exists in the given table"""

		cursor.execute(
			"select unique ${1} from ${0} where ${1} = '${2}'".format(
				tableName, columnName, string))

		results = cursor.fetchone()

		if len(results) == 0: return False
		return True