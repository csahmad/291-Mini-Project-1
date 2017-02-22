class TableTools:
	"""Static methods for getting information about tables"""

	@staticmethod
	def itemExists(cursor, tableName, columnName, item):
		"""Return whether the given string value exists in the given table"""

		cursor.execute(
			"select unique ${1} from ${0} where ${1} = ${2}".format(
				tableName, columnName, item))

		results = cursor.fetchone()

		if len(results) == 0: return False
		return True

class UsersTableTools:
	"""Static methods for getting data from the 'Users' table"""

	_USERS_TABLE = "Users"
	_MAX_PASSWORD_LENGTH = 4

	@staticmethod
	def userExists(cursor, userID):
		"""Return whether the user exists"""

		return TableTools.itemExists(cursor, UsersTableTools._USERS_TABLE,
			"usr", userID)

	@staticmethod
	def loginExists(cursor, userID, password):
		"""Return whether the given username, password combination exists"""

		if len(password) > UsersTableTools._MAX_PASSWORD_LENGTH: return False

		cursor.execute(
			"select usr, pwd from ${0} where usr = ${1} and pwd = ${2}".format(
				UsersTableTools._USERS_TABLE, userID, password))

		results = cursor.fetchone()

		if len(results) == 0: return False
		return True