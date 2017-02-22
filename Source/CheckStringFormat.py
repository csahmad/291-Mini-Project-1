class CheckStringFormat:
	"""Check the format of a string"""

	@staticmethod
	def isInt(string):
		"""Return whether the string is an integer"""

		try:
			int(string)
			return True

		except ValueError:
			return False