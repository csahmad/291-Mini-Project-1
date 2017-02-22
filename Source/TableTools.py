class TableTools:
	"""Static methods for getting information about tables"""

	@staticmethod
	def itemExists(cursor, tableName, columnName, item):
		"""Return whether the given string value exists in the given table"""

		cursor.execute(
			"select unique {1} from {0} where {1} = {2}".format(
				tableName, columnName, item))

		result = cursor.fetchone()

		if result is None: return False
		return True

class UsersTableTools:
	"""Static methods for getting data from the 'Users' table"""

	_USERS_TABLE = "Users"
	_MAX_PASSWORD_LENGTH = 4

	@staticmethod
	def addUser(cursor, password, name, email, city, timezone, userID):
		"""Add a new user"""

		# Add quotation marks to string values
		password = "'{0}'".format(password)
		name = "'{0}'".format(name)
		email = "'{0}'".format(email)
		city = "'{0}'".format(city)

		values = (str(userID), password, name, email, city, timezone)

		cursor.execute("insert into {0} values {1}".format(
			UsersTableTools._USERS_TABLE, str(values)))

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
		"select usr, pwd from {0} where usr = {1} and pwd = '{2}'".format(
			UsersTableTools._USERS_TABLE, userID, password))

		result = cursor.fetchone()

		if result is None: return False
		return True