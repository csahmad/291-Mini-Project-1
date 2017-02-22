class TweetToString:
	"""Represent a tweet as a string"""

	@staticmethod
	def toString(writer, date, text, replyTo = None):
		"""Return a string representing the given tweet"""

		if replyTo is None or replyTo == "null":
			replyToString = ""

		else:
			replyToString = "@{0} ".format(replyTo)

		return "{0}: {1}{2} ({3})".format(writer, replyToString, text, date)