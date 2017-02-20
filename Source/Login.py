class Login:
	"""Login or sign up using the 'users' table"""

	_TABLE_NAME = "users"

	@staticmethod
	def getUser(cursor, username, password)
		"""
		Get the user with the given username and password from the 'users'
		table
		"""

		pass

	@staticmethod
	def addUser(cursor, password, name, email, city, timezone)
		"""
		Add a user to the 'users' table (the username is randomly generated)
		"""

		pass

		#cursor.execute(
		#"insert into ${0} values ($'{1}', $'{2}', ${3}, ${4}, ${5}, ${6})".format(
		#	Login._TABLE_NAME, username, password, name, email, city,
		#		timezone))