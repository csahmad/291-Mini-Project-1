from TableTools import TweetsTableTools
from TerminalMenu import TerminalGeneratorMenu
from ViewTweetMenu import ViewTweetMenu

class UserTweetsMenu:
	"""A menu for viewing a user's tweets"""

	BACK_INDEX = 0
	_INITIAL_INDEX = -1

	_EMPTY_MESSAGE = "No tweets"

	def __init__(self, connection, loginID, userID):
		"""
		Arguments:
		loginID -- the user ID of the signed in user
		userID -- the ID of the user to view the tweets of
		"""

		self._connection = connection
		self._loginID = loginID
		self._userID = userID
		self._resultsGenerator = None

	def showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		UserTweetsMenu.BACK_INDEX
		"""

		choice = UserTweetsMenu._INITIAL_INDEX

		while choice == UserTweetsMenu._INITIAL_INDEX:
			choice = self._showAndGet()

		return choice

	def _showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		UserTweetsMenu.BACK_INDEX
		"""

		self._resultsGenerator = TweetsTableTools.getTweetsByDate(
			self._connection, self._userID)

		menu = TerminalGeneratorMenu(self._resultsGenerator,
			emptyMessage = UserTweetsMenu._EMPTY_MESSAGE)

		result = menu.showAndGet()

		# If an exit key was pressed, return None
		if result is None: return None

		# If the back option was chosen, return UserTweetsMenu.BACK_INDEX
		if result.backWasChosen: return UserTweetsMenu.BACK_INDEX

		# If a tweet was chosen, view the tweet
		else:
			viewTweetMenu = ViewTweetMenu(self._connection, self._userID,
				result.chosenItem)
			result = viewTweetMenu.showAndGet()
			if result is None: return None        # If an exit key was pressed

		return UserTweetsMenu._INITIAL_INDEX