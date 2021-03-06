from IDGenerator import IDGenerator

class Users:
	"""Get or add users using the 'users' table"""

	_TABLE_NAME = "users"

	@staticmethod
	def getUser(cursor, username, password)
		"""
		Return the user with the given username and password from the 'users'
		table (return None if no such user)
		"""

		cursor.execute("select usr from {0}" +
			"where usr='{1}' and pwd='{2}'".format(
				Login._TABLE_NAME, username, password))

		result = cursor.fetchone()

		if result is None: return None
		return result[0]

	@staticmethod
	def addUser(cursor, password, name, email, city, timezone)
		"""
		Add a user to the 'users' table and return the randomly generated
		username
		"""

		username = IDGenerator.getUniqueInt(cursor, _TABLE_NAME, "usr")

		cursor.execute("insert into {0} values" +
			"($'{1}', $'{2}', {3}, {4}, {5}, {6})".format(
				Login._TABLE_NAME, username, password, name, email, city,
					timezone))