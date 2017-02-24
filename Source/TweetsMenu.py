from TerminalMenu import TerminalGeneratorMenu
from ViewTweetMenu import ViewTweetMenu

class TweetsMenu:
	"""A menu for viewing tweets from a Tweet generator"""

	BACK_INDEX = 0
	_INITIAL_INDEX = -1

	def __init__(self, cursor, userID, tweetGenerator, preMessage = None,
		emptyMessage = "No tweets"):
		"""
		Arguments:
		userID -- the user ID of the signed in user
		tweetGenerator -- a generator that yields Tweet objects
		preMessage -- the message to show before the listed tweets
		empytMessage -- the message to display if the generator yields nothing
		"""

		self._cursor = cursor
		self._userID = userID
		self._tweetGenerator = tweetGenerator
		self._preMessage = preMessage
		self._emptyMessage = emptyMessage

	def showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		TweetsMenu.BACK_INDEX
		"""

		choice = TweetsMenu._INITIAL_INDEX

		while choice is not None and choice != TweetsMenu.BACK_INDEX:
			choice = self._showAndGet()

		return choice

	def _showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		TweetsMenu.BACK_INDEX
		"""

		menu = TerminalGeneratorMenu(self._tweetGenerator,
			preMessage = self._preMessage, emptyMessage = self._emptyMessage)

		result = menu.showAndGet()

		# If an exit key was pressed, return None
		if result is None: return None

		# If the back option was chosen, return TweetsMenu.BACK_INDEX
		if result.backWasChosen: return TweetsMenu.BACK_INDEX

		# If a tweet was chosen, view the tweet
		else:
			viewTweetMenu = ViewTweetMenu(cursor, self._userID,
				result.chosenItem)
			result = viewTweetMenu.showAndGet()
			if result is None: return None        # If an exit key was pressed

		return TweetsMenu._INITIAL_INDEX