from TableTools import TweetsTableTools
from TerminalMenu import TerminalGeneratorMenu
from TweetsMenu import TweetsMenu

class UserTweetsMenu:
	"""A menu for viewing a user's tweets"""

	BACK_INDEX = 0

	def __init__(self, connection, loginID, userID):
		"""
		Arguments:
		loginID -- the user ID of the signed in user
		userID -- the ID of the user to view the tweets of
		"""

		self._connection = connection
		self._loginID = loginID
		self._userID = userID

		self._tweetGeneratorMethod = lambda: TweetsTableTools.getTweetsByDate(
			connection, userID)

	def showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		UserTweetsMenu.BACK_INDEX
		"""

		menu = TweetsMenu(self._connection, self._userID,
			self._tweetGeneratorMethod)

		result = menu.showAndGet()

		# If an exit key was pressed, return None
		if result is None: return None

		# If the back option was chosen, return UserTweetsMenu.BACK_INDEX
		return UserTweetsMenu.BACK_INDEX