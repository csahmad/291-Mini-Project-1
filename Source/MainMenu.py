from GeneratorTools import GeneratorTools
from DateTools import DateTools
from IDGenerator import IDGenerator
from TerminalMenu import TerminalMenu
from TableTools import TweetsTableTools
from TweetTools import TweetTools
from SearchMenu import SearchMenu
from FollowersMenu import FollowersMenu
from ViewTweetMenu import ViewTweetMenu

class MainMenu:
	"""
	The main menu for the terminal interface (shown after login or sign up)
	"""

	_SEE_MORE_INDEX = -1
	_POST_INDEX = -2
	_SEARCH_INDEX = -3
	_FOLLOWERS_INDEX = -4
	LOGOUT_INDEX = -5

	def __init__(self, cursor, userID):

		self._cursor = cursor
		self._userID = userID
		self._tweetGenerator = TweetsTableTools.getFolloweeTweetsByDate(
			self._cursor, self._userID)

		self._displayedTweets = None
		self._getNextTweets()
		if self._displayedTweets is None: self._displayedTweets = []

	def showAndGet(self):
		"""
		Show the menu and return either None (if an exit key was pressed) or
		MainMenu.LOGOUT_INDEX if the user chose to logout
		"""

		options = ["Post", "Search", "Followers", "Logout"]
		tweetStrings = self._getTweetStrings()

		# If no tweets to display, indicate this in preMessage
		if self._displayedTweets is None:
			preMessage = "No tweets to display"

		# If tweets to display, include "See more" option
		else:
			options = tweetStrings + ["See more"] + options
			preMessage = None

		menu = TerminalMenu(options, preMessage)
		choice = self._interpretChoice(menu.showAndGet())

		# If an exit key was pressed, return None
		if choice is None:
			return None

		# If user chose to see more, show next few tweets or display no more
		# tweets message
		elif choice == MainMenu._SEE_MORE_INDEX:
			self._getNextTweets()

		# If user chose to post a tweet
		elif choice == MainMenu._POST_INDEX:
			self._postTweet()

		# If user chose to search
		elif choice == MainMenu._SEARCH_INDEX:
			searchMenu = SearchMenu(cursor, self._userID)
			result = searchMenu.showAndGet()
			if result is None: return None        # If an exit key was pressed

		# If user chose to view followers
		elif choice == MainMenu._FOLLOWERS_INDEX:
			followersMenu = FollowersMenu(cursor, self._userID)
			result = followersMenu.showAndGet()
			if result is None: return None        # If an exit key was pressed

		# If user chose to logout, return MainMenu.LOGOUT_INDEX
		elif choice == MainMenu.LOGOUT_INDEX:
			return MainMenu.LOGOUT_INDEX

		# If a tweet was chosen
		else:
			viewTweetMenu = ViewTweetMenu(cursor, self._userID,
				self._displayedTweets[choice])
			result = viewTweetMenu.showAndGet()
			if result is None: return None        # If an exit key was pressed

		# If user did not exit or logout yet (no value returned yet), show menu
		# again
		return self.showAndGet()

	def _interpretChoice(self, choice):
		"""
		If the given choice is not the index of a displayed tweet, return an
		index to represent the choice that corresponds to a MainMenu constant

		Return None if None given
		"""

		if choice is None: return None

		length = len(self._displayedTweets)

		# If choice is a displayed tweet, return the index of the tweet
		if choice < length: return choice

		choices = [MainMenu._SEE_MORE_INDEX, MainMenu._POST_INDEX,
			MainMenu._SEARCH_INDEX, MainMenu._FOLLOWERS_INDEX,
			MainMenu.LOGOUT_INDEX]

		if length == 0: choices.pop(0)

		return choices[length - choice]

	def _getTweetStrings(self):
		"""Return a list of the displayed tweets as strings"""

		return [str(tweet) for tweet in self._displayedTweets]

	def _getNextTweets(self, amount = 5):
		"""Store the next few tweets or None if no more"""

		self._displayedTweets = GeneratorTools.next(self._tweetGenerator,
			amount)

		if len(self._displayedTweets) == 0:
			self._displayedTweets = None

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