from TerminalMenu import TerminalGeneratorMenu
from ViewTweetMenu import ViewTweetMenu

class TweetsMenu:
	"""A menu for viewing tweets from a Tweet generator"""

	BACK_INDEX = 0
	_INITIAL_INDEX = -1

	def __init__(self, connection, userID, tweetGeneratorMethod,
		preMessage = None, emptyMessage = "No tweets"):
		"""
		Arguments:
		userID -- the user ID of the signed in user
		tweetGeneratorMethod -- the method to call to get the tweet generator
			as a lambda with arguments
		preMessage -- the message to show before the listed tweets
		empytMessage -- the message to display if the generator yields nothing
		"""

		self._connection = connection
		self._userID = userID
		self._tweetGeneratorMethod = tweetGeneratorMethod
		self._preMessage = preMessage
		self._emptyMessage = emptyMessage

	def showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		TweetsMenu.BACK_INDEX
		"""

		choice = TweetsMenu._INITIAL_INDEX

		while choice == TweetsMenu._INITIAL_INDEX:
			choice = self._showAndGet()

		return choice

	def _showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		TweetsMenu.BACK_INDEX
		"""

		tweetGenerator = self._tweetGeneratorMethod()

		menu = TerminalGeneratorMenu(tweetGenerator,
			preMessage = self._preMessage, emptyMessage = self._emptyMessage)

		result = menu.showAndGet()

		# If an exit key was pressed, return None
		if result is None: return None

		# If the back option was chosen, return TweetsMenu.BACK_INDEX
		if result.backWasChosen: return TweetsMenu.BACK_INDEX

		# If a tweet was chosen, view the tweet
		else:
			viewTweetMenu = ViewTweetMenu(self._connection, self._userID,
				result.chosenItem)
			result = viewTweetMenu.showAndGet()
			if result is None: return None        # If an exit key was pressed

		return TweetsMenu._INITIAL_INDEX