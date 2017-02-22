class CheckStringFormat:
	"""Check the format of a string"""

	@staticmethod
	def isNumeric(string):
		"""Return whether the string is a number"""

		try:
			float(string)
			return True

		except ValueError:
			return False

	@staticmethod
	def isInt(string):
		"""Return whether the string is an integer"""

		try:
			int(string)
			return True

		except ValueError:
			return False