import os
from getpass import getpass

from Constants import Constants

class TerminalInterface:
	"""Static methods for implementing a terminal interface"""

	def login(usernamePrompt = "username:", passwordPrompt = "password:"):
		"""
		Prompt a user to login and return the entered username and password as
		a tuple (username first)

		Keyword arguments:
		usernamePrompt -- the prompt to show when asking for the username
		passwordPrompt -- the prompt to show when asking for the password
		"""

		TerminalInterface.tryClear()
		username = input(usernamePrompt)
		password = getpass(passwordPrompt)

		return (username, password)

	@staticmethod
	def tryClear():
		"""Try to clear the terminal if Constants.USE_CLEAR is set to True"""

		try:
			TerminalInterface._clear()

		except:
			pass

	@staticmethod
	def _clear():
		"""Clear the terminal if Constants.USE_CLEAR is set to True"""

		if Constants.USE_CLEAR:
			os.system('cls' if os.name == 'nt' else 'clear')