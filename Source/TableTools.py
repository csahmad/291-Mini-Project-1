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

	@staticmethod
	def addQuotes(stringValue):
		"""
		Add single quotes around the given string value and return

		Return None if None given
		"""

		if stringValue is None: return None
		return "'{0}'".format(stringValue)

	@staticmethod
	def replaceWithNull(string):
		"""If None passed, return 'null', otherwise return string"""

		if string is None: return "null"
		return string

class UsersTableTools:
	"""Static methods for getting data from the 'Users' table"""

	_USERS_TABLE = "Users"
	_MAX_PASSWORD_LENGTH = 4

	@staticmethod
	def addUser(cursor, password, name, email, city, timezone, userID):
		"""Add a new user"""

		# Add quotation marks to string values
		password = TableTools.addQuotes(password)
		name = TableTools.addQuotes(name)
		email = TableTools.addQuotes(email)
		city = TableTools.addQuotes(city)

		# Replace None with "null"
		userID = TableTools.replaceWithNull(userID)
		password = TableTools.replaceWithNull(password)
		name = TableTools.replaceWithNull(name)
		email = TableTools.replaceWithNull(email)
		city = TableTools.replaceWithNull(city)
		timezone = TableTools.replaceWithNull(timezone)

		insertStatement = "insert into {0} values ".format(
			UsersTableTools._USERS_TABLE) + \
			"({0}, {1}, {2}, {3}, {4}, {5})".format(
			userID, password, name, email, city, timezone)

		cursor.execute(insertStatement)

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