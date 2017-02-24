from DateTools import DateTools
from IDGenerator import IDGenerator
from TerminalMenu import TerminalGeneratorMenu
from TableTools import TweetsTableTools
from TweetTools import TweetTools
from SearchMenu import SearchMenu
from FollowersMenu import FollowersMenu
from ViewTweetMenu import ViewTweetMenu

class MainMenu:
	"""
	The main menu for the terminal interface (shown after login or sign up)
	"""

	_POST_INDEX = 0
	_SEARCH_INDEX = 1
	_FOLLOWERS_INDEX = 2
	LOGOUT_INDEX = 3
	_INITIAL_INDEX = -1

	_OPTIONS = ["Post", "Search", "Followers", "Exit"]
	_EMPTY_MESSAGE = "No tweets to display"

	def __init__(self, cursor, userID):

		self._cursor = cursor
		self._userID = userID
		self._tweetGenerator = TweetsTableTools.getFolloweeTweetsByDate(
			self._cursor, self._userID)

	def showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		MainMenu.LOGOUT_INDEX (if the user chose to logout)
		"""

		choice = MainMenu._INITIAL_INDEX

		while choice == MainMenu._INITIAL_INDEX:
			choice = self._showAndGet()

		return choice

	def _showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		MainMenu.LOGOUT_INDEX (if the user chose to logout)
		"""

		menu = TerminalGeneratorMenu(self._tweetGenerator,
			otherOptions = MainMenu._OPTIONS,
			emptyMessage = MainMenu._EMPTY_MESSAGE)

		result = menu.showAndGet()
		choice = result.chosenOptionIndex

		# If an exit key was pressed, return None
		if result is None: return None

		# If the back option was chosen, return MainMenu.LOGOUT_INDEX
		if result.backWasChosen: return MainMenu.LOGOUT_INDEX

		# If a tweet was chosen, view the tweet
		if result.itemWasChosen():
			viewTweetMenu = ViewTweetMenu(self._cursor, self._userID,
				result.chosenItem)
			result = viewTweetMenu.showAndGet()
			if result is None: return None        # If an exit key was pressed

		# If user chose to post a tweet, let the user post a tweet
		elif choice == MainMenu._POST_INDEX:
			self._postTweet()

		# If user chose to search, open the search menu
		elif choice == MainMenu._SEARCH_INDEX:
			searchMenu = SearchMenu(self._cursor, self._userID)
			result = searchMenu.showAndGet()
			if result is None: return None        # If an exit key was pressed

		# If user chose to view followers, show followers
		elif choice == MainMenu._FOLLOWERS_INDEX:
			followersMenu = FollowersMenu(self._cursor, self._userID)
			result = followersMenu.showAndGet()
			if result is None: return None        # If an exit key was pressed

		return MainMenu._INITIAL_INDEX

	def _postTweet(self):
		"""Let the user post a tweet"""

		tweetText = input("Post:")
		hashtags = TweetTools.getHashtags(tweetText)
		date = DateTools.getCurrentDate()
		tweetID = IDGenerator.getNewTweetID(self._cursor)
		TweetsTableTools.addTweet(self._cursor, self._userID, date, tweetText,
			tweetID, None, hashtags)

# Interactive test
if __name__ == "__main__":

	from OracleTerminalConnection import OracleTerminalConnection
	from LoginMenu import LoginMenu

	# Get connection to database and cursor
	connection = OracleTerminalConnection.connect()
	cursor = connection.cursor()

	user = LoginMenu.getUser(cursor)

	mainMenu = MainMenu(cursor, user)
	print(mainMenu.showAndGet())

	connection.close()