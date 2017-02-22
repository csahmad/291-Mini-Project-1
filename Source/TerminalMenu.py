from Constants import Constants
from TerminalInterface import TerminalInterface
from KeypressDetector import KeypressDetector

class TerminalMenu:
	"""A menu (list of options) for a terminal interface"""

	def __init__(self, options, preMessage = None, postMessage = None):
		"""
		Keyword arguments:
		options -- the options the user can choose from as a collection of
			strings
		preMessage -- the message to show above the menu (optional)
		postMessage -- the message to show below the menu (optional)
		"""

		self._options = options
		self._preMessage = preMessage
		self._postMessage = postMessage
		self._selected = 0                 # The index of the selected item
		self._result = None

	def showAndGet(self):
		"""
		Show the menu and return the index of the selected option or None (if
		an exit key is pressed)
		"""

		self._selected = 0
		self._show()
		return self._handleKeypresses()

	def _handleKeypresses(self):
		"""
		Handle keypresses and return the index of the selected option or None
		(if an exit key is pressed)
		"""

		combinedUpKeys = Constants.UP_KEYS + Constants.LEFT_KEYS
		combinedDownKeys = Constants.DOWN_KEYS + Constants.RIGHT_KEYS

		while True:

			pressed = KeypressDetector.getKey(Constants.SPECIAL_KEYS)

			# If an enter key pressed, return the selected option
			if pressed in Constants.ENTER_KEYS:
				return self._selected

			# If an exit key is pressed, return None
			elif pressed in Constants.EXIT_KEYS:
				return None

			# If an up or left key is pressed, move the selection up
			elif pressed in combinedUpKeys:
				self._selected = (self._selected - 1) % len(self._options)
				self._show()

			# If a down or right key is pressed, move the selection down
			elif pressed in combinedDownKeys:
				self._selected = (self._selected + 1) % len(self._options)
				self._show()

	def _show(self):
		"""Show the menu"""

		TerminalInterface.tryClear()
		if self._preMessage is not None: print(self._preMessage)
		self._showOptions()
		if self._postMessage is not None: print(self._postMessage)

	def _showOptions(self):
		"""Show the menu options"""

		i = 0

		for option in self._options:

			if i == self._selected:
				print(Constants.SELECTED_STRING, end="")

			else:
				print(Constants.UNSELECTED_STRING, end="")

			print(option)

			i += 1

# Interactive test
if __name__ == "__main__":

	options = ("Option 0", "Option 1", "Option 2")

	menu = TerminalMenu(options)
	print(menu.showAndGet())