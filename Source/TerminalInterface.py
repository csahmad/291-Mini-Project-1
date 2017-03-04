import os
from getpass import getpass

from Constants import Constants
from CheckStringFormat import CheckStringFormat

class TerminalInterface:
	"""Static methods for implementing a terminal interface"""

	@staticmethod
	def alert(message, prompt = "\n(Press Enter to continue)"):
		"""
		Clear the terminal, display the given message, and wait for the user to
		press Enter
		"""

		TerminalInterface.tryClear()
		input(message + prompt)

	@staticmethod
	def login(usernamePrompt = "username:", passwordPrompt = "password:",
		integerUsername = False):
		"""
		Prompt a user to login and return the entered username and password as
		a tuple (username first)

		Arguments:
		usernamePrompt -- the prompt to show when asking for the username
		passwordPrompt -- the prompt to show when asking for the password
		integerUsername -- whether to only allow an integer username
		"""

		TerminalInterface.tryClear()

		username = input(usernamePrompt)

		# If username must be an integer, make sure it is
		if integerUsername:

			while not CheckStringFormat.isInt(username):
				TerminalInterface.tryClear()
				print("Must be an integer")
				username = input(usernamePrompt)

		TerminalInterface.tryClear()
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