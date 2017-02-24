import time

class DateTools:
	"""Tools for working with dates"""

	@staticmethod
	def getCurrentDate():
		"""Return the current date as a string"""

		return time.strftime("%d-%b-%y")