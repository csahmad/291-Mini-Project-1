from Constants import Constants
from TerminalInterface import TerminalInterface
from KeypressDetector import KeypressDetector
from CheckStringFormat import CheckStringFormat

class TerminalFormResults:
	"""The results of a terminal form"""

	def __init__(self, fields = None, exitKeyPressed = False):
		"""
		Keyword arguments:
		fields -- a collection of Field objects or None (if form not submitted)
		exitKeyPressed -- whether the user pressed an exit key while in the
			form (as opposed to just choosing the cancel option)
		"""

		self._submitted = fields is not None
		self._values = TerminalFormResults._extractValues(fields)
		self._makeEmptyNone()
		self._exitKeyPressed = exitKeyPressed

	@property
	def submitted(self):
		"""Return whether the form was submitted"""

		return self._submitted

	def _makeEmptyNone():
		"""Replace empty strings with None"""

		for i in len(self._values):
			value = self._values[i]
			if value == "": self._values[i] = None

	@property
	def values(self):
		"""Return the values saved in the form"""

		return self._values

	@property
	def exitKeyPressed(self):
		"""Return whether the user used an exit key to exit the form"""

		return self._exitKeyPressed

	@staticmethod
	def _extractValues(fields):
		"""
		Return a dictionary with field name keys and value results

		If fields is None, return None

		Keyword arguments:
		fields -- the collection of Field objects to extract from
		"""

		if fields is None: return None
		values = {}
		for field in fields: values[field.name] = field.value
		return values

class FormField:
	"""A form field"""

	def __init__(self, name, maxValueLength = None, isNumeric = False,
		value = ""):
		"""
		Keyword arguments:
        name -- the name/label of this field
        maxValueLength -- the maximum allowed length of the value for this
        	field (required if not numeric)
        isNumeric -- whether this field can only have a numeric value
        value -- the initial value of this field
		"""

		self._name = name
		self._maxValueLength = maxValueLength
		self._isNumeric = isNumeric
		self.value = value

	@property
	def name(self):
		"""Get the name of this field"""

		return self._name

	@property
	def maxValueLength(self):
		"""Get the maximum allowed length of the value of this field"""

		return self._maxValueLength

	@property
	def isNumeric(self):
		"""Return whether this field can only have a numeric value"""

		return self._isNumeric

class TerminalForm:
	"""A form for a terminal interface"""

	_SUBMIT_STRING = "Save"
	_CANCEL_STRING = "Cancel"
	_OPTION_SEPARATOR = " | "

	_SUBMIT_INDEX = -1
	_CANCEL_INDEX = -2

	_FIELD_NAME_END = ":"
	"""The string to add to the end of a field name when displaying it"""

	def __init__(self, fields):
		"""
		Keyword arguments:
        fields -- the fields for this form as a list/tuple of Field objects
		"""

		self._results = None             # The TerminalFormResults
		self._selected = 0               # The index of the selected item
		self._fields = fields

	def showAndGet(self):
		"""Show the form and return a TerminalFormResults"""

		self._selected = 0

		while self._results is None:
			self._show()
			self._handleKeypress()

		return self._results

	def _handleKeypress(self):
		"""Handle the next keypress"""

		pressed = KeypressDetector.getKey(Constants.SPECIAL_KEYS)

		# If an enter key pressed
		if pressed in Constants.ENTER_KEYS:

			# If submit option selected, store results in self._results
			if self._selected == TerminalForm._SUBMIT_INDEX:
				self._results = TerminalFormResults(fields)

			# If cancel option selected, store empty results
			elif self._selected == TerminalForm._CANCEL_INDEX:
				self._results = TerminalFormResults()

			# If field selected, let user edit it
			else:
				self._editField()

		# If an exit key pressed, indicate this in self._results
		elif pressed in Constants.EXIT_KEYS:
			self._results = TerminalFormResults(exitKeyPressed = True)

		# If an up key pressed, move selection
		elif pressed in Constants.UP_KEYS:

			# If on first field, jump to submit option
			if self._selected == 0:
				self._selected = TerminalForm._SUBMIT_INDEX

			# If on the submit or cancel option, move to the last field
			elif self._selected in (TerminalForm._SUBMIT_INDEX,
				TerminalForm._CANCEL_INDEX):

				self._selected = len(self._fields) - 1

			# If on a field other than the first, move selection up
			else:
				self._selected -= 1

			self._show()

		# If a down key pressed, move selection
		elif pressed in Constants.DOWN_KEYS:

			# If on last field, move to submit option
			if self._selected == len(self._fields) - 1:
				self._selected = TerminalForm._SUBMIT_INDEX

			# If on the submit or cancel option, move to the first field
			elif self._selected in (TerminalForm._SUBMIT_INDEX,
				TerminalForm._CANCEL_INDEX):

				self._selected = 0

			# If on a field other than the last, move selection down
			else:
				self._selected += 1

			self._show()

		# If a left key pressed, move selection
		elif pressed in Constants.LEFT_KEYS:

			# If on first field, jump to submit option
			if self._selected == 0:
				self._selected = TerminalForm._SUBMIT_INDEX

			# If on submit option, move to cancel option
			elif self._selected == TerminalForm._SUBMIT_INDEX:
				self._selected = TerminalForm._CANCEL_INDEX

			# If on cancel option, move to submit option
			elif self._selected == TerminalForm._CANCEL_INDEX:
				self._selected = TerminalForm._SUBMIT_INDEX

			# If on a field other than the first, move selection up
			else:
				self._selected -= 1

			self._show()

		# If a right key pressed, move selection
		elif pressed in Constants.RIGHT_KEYS:

			# If on last field, move to submit option
			if self._selected == len(self._fields) - 1:
				self._selected = TerminalForm._SUBMIT_INDEX

			# If on submit option, move to cancel option
			elif self._selected == TerminalForm._SUBMIT_INDEX:
				self._selected = TerminalForm._CANCEL_INDEX

			# If on cancel option, move to submit option
			elif self._selected == TerminalForm._CANCEL_INDEX:
				self._selected = TerminalForm._SUBMIT_INDEX

			# If on a field other than the last, move selection down
			else:
				self._selected += 1

			self._show()

	def _editField(self):
		"""Let user edit selected field"""

		TerminalInterface.tryClear()
		field = self._fields[self._selected]
		fieldLabel = field.name + TerminalForm._FIELD_NAME_END

		value = input(fieldLabel)

		if field.isNumeric:

			notNumericMessage = "Value must be numeric"

			while not CheckStringFormat.isNumeric(value):
				TerminalInterface.tryClear()
				print(notNumericMessage)
				value = input(fieldLabel)

		else:

			tooLongMessage = "Value cannot be longer than " + \
				str(field.maxValueLength) + " characters"

			while len(value) > field.maxValueLength:
				TerminalInterface.tryClear()
				print(tooLongMessage)
				value = input(fieldLabel)

		field.value = value
		self._show()

	def _show(self):
		"""Show the form"""

		TerminalInterface.tryClear()
		self._showFields()
		self._showSubmitCancel()

	def _showSubmitCancel(self):
		"""Show the submit and cancel options"""

		submitString = TerminalForm._SUBMIT_STRING
		cancelString = TerminalForm._CANCEL_STRING
		cancelString = TerminalForm._CANCEL_STRING
		separator = TerminalForm._OPTION_SEPARATOR

		if self._selected == TerminalForm._SUBMIT_INDEX:
			submitString = Constants.SELECTED_STRING + submitString

		elif self._selected == TerminalForm._CANCEL_INDEX:
			cancelString = Constants.SELECTED_STRING + cancelString

		print(submitString + separator + cancelString)

	def _showFields(self):
		"""Show the fields"""

		i = 0

		for field in self._fields:

			if i == self._selected:
				print(Constants.SELECTED_STRING, end="")

			else:
				print(Constants.UNSELECTED_STRING, end="")

			print(field.name + TerminalForm._FIELD_NAME_END + field.value)

			i += 1

# Interactive test
if __name__ == "__main__":

	fields = [FormField("Length 1 String", 1), FormField("Length 2 String", 2),
		FormField("Length 3 String", 3),
		FormField("Number", isNumeric = True)]

	form = TerminalForm(fields)
	form.showAndGet()