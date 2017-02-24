class ViewUserMenu:
	"""A menu for viewing a user"""

	def __init__(self, cursor, loginID, userID):
		"""
		Arguments:
		loginID -- the ID of the signed in user
		userID -- the ID of the user to view
		"""

		self._cursor = cursor
		self._loginID = loginID
		self._userID = userID

	def showAndGet(self):

		pass