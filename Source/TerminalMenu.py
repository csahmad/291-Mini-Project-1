from Constants import Constants
from TerminalInterface import TerminalInterface
from KeypressDetector import KeypressDetector
from GeneratorTools import GeneratorTools

class GeneratorMenuChoice:
	"""Represents a user choice from a TerminalGeneratorMenu"""

	def __init__(self, chosenItem = None, chosenOptionIndex = None,
		backWasChosen = False):
		"""
		Arguments:
		chosenItem -- the item that was chosen (if any)
		chosenOptionIndex -- the index of the non-generator-item option that
			was chosen (if any)
		backChosen -- whether the user chose the back option
		"""

		self._chosenItem = chosenItem
		self._chosenOptionIndex = chosenOptionIndex
		self._backWasChosen = backWasChosen

	@property
	def chosenItem(self):

		return chosenItem

	@property
	def chosenOptionIndex(self):

		return chosenOptionIndex

	@property
	def backWasChosen(self):

		return self._backWasChosen

	def itemWasChosen(self):
		"""Return whether an item was chosen"""

		return self._chosenItem != None

class TerminalGeneratorMenu:
	"""
	A menu that displays a few options at a time with a "See more" option

	Gets options using a given generator
	"""

	_SEE_MORE_INDEX = 0
	_BACK_INDEX = 1

	_SEE_MORE_STRING = "See more"
	_BACK_STRING = "Back"

	def __init__(self, generator, pageSize = 5, otherOptions = None,
		preMessage = None, postMessage = None,
		emptyMessage = "Nothing to display"):
		"""
		Arguments:
		generator -- the generator to get the options from
		pageSize -- the number of items to show per page
		otherOptions -- any options to show below the options from the
			generator
		preMessage -- the message to show above the menu
		postMessage -- the message to show below the menu
		emptyMessage -- the message to display if generator empty
		"""

		self._generator = generator
		self._pageSize = pageSize
		if otherOptions is None: otherOptions = []
		self._otherOptions = otherOptions
		self._preMessage = preMessage
		self._postMessage = postMessage
		self._emptyMessage = emptyMessage

		self._displayedItems = []
		self._displayedItemStrings = []
		self._exhaustedItems = False

	def showAndGet(self):
		"""
		Show the menu and return a GeneratorMenuChoice or None (if an exit key
		was pressed)
		"""

		choice = TerminalGeneratorMenu._SEE_MORE_INDEX

		while choice == TerminalGeneratorMenu._SEE_MORE_INDEX:
			self._getNextItems()
			choice = self._showAndGet()

		return choice

	def _showAndGet(self):
		"""
		Show the menu and return a GeneratorMenuChoice or None (if an exit key
		was pressed)
		"""

		options = list(self._displayedItemStrings)

		# If items not yet exhausted, include the option to see more
		if not self._exhaustedItems:
			options += [TerminalGeneratorMenu._SEE_MORE_STRING]

		# If no items to display, indicate this in the pre-message
		if len(self._displayedItems) == 0:
			self._preMessage = self._emptyMessage

		options += [TerminalGeneratorMenu._BACK_STRING] + self._otherOptions

		menu = TerminalMenu(options, self._preMessage, self._postMessage)

		return self._choiceFromIndex(menu.showAndGet())

	def _choiceFromIndex(self, index):
		"""
		Convert the given choice from an index into a GeneratorMenuChoice or
		return TerminalGeneratorMenu._SEE_MORE_INDEX if the user chose to see
		more

		Return None if None given
		"""

		if index is None: return None

		count = len(self._displayedItems)

		# If an item was chosen, return a GeneratorMenuChoice
		if index < count:
			return GeneratorMenuChoice(self._displayedItems[index])

		optionIndex = count - index

		# If the user chose to see more, return
		# TerminalGeneratorMenu._SEE_MORE_INDEX
		if not self._exhaustedItems and \
			optionIndex == TerminalGeneratorMenu._SEE_MORE_INDEX:

			return TerminalGeneratorMenu._SEE_MORE_INDEX

		# If the user chose to go back, return a GeneratorMenuChoice
		return GeneratorMenuChoice(backWasChosen = True)

		# If another option was chosen, return a GeneratorMenuChoice
		return GeneratorMenuChoice(chosenOptionIndex = optionIndex)

	def _getNextItems(self):
		"""
		Store the next few items or set self._exhaustedItems to True (if no
		more)
		"""

		items = GeneratorTools.next(self._generator, self._pageSize)
		count = len(items)

		if count == 0:
			self._exhaustedItems = True

		else:

			if count < self._pageSize:
				self._exhaustedItems = True

			self._displayedItems = items
			self._displayedItemStrings = [str(item) for item in items]

class TerminalMenu:
	"""A menu (list of options) for a terminal interface"""

	def __init__(self, options, preMessage = None, postMessage = None):
		"""
		Arguments:
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

	def itemGenerator():

		items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6",
			"Item 7", "Item 8", "Item 9", "Item 10", "Last Item"]

		for item in items: yield item

	generator = itemGenerator()
	options = ["Option 1", "Option 2"]
	menu = TerminalGeneratorMenu(generator)
	print(menu.showAndGet())