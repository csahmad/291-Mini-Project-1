import os
import re
from getpass import getpass

from Constants import Constants
from CheckStringFormat import CheckStringFormat

class TerminalInterface:
	"""Static methods for implementing a terminal interface"""

	@staticmethod
	def getSearchKeywords():
		"""
		Prompt the user for a string of keywords, split the string by space
		and/or comma and return the result

		If the entered string is empty, alert the user that the search was
		dismissed and return None
		"""

		keywords = TerminalInterface.getKeywords()

		if keywords is None:
			TerminalInterface.alert("Empty search dismissed")
			return None

		return keywords

	@staticmethod
	def getKeywords():
		"""
		Prompt the user for a string of keywords, split the string by space
		and/or comma and return the result

		If the entered string is empty, return None
		"""

		keywordString = input("Enter keywords:")
		if keywordString == "": return None
		return re.split("\s|\s*,\s*", keywordString.rstrip())

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
