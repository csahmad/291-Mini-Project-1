from TerminalMenu import TerminalMenu
from TableTools import UsersTableTools, FollowsTableTools
from UserTweetsMenu import UserTweetsMenu
from DateTools import DateTools

class ViewUserMenu:
	"""A menu for viewing a user"""

	_FOLLOW_INDEX = 0
	_VIEW_TWEETS_INDEX = 1
	BACK_INDEX = 2
	_INITIAL_INDEX = -1

	_OPTIONS = ["Follow", "View tweets", "Back"]
	_OPTIONS_WITHOUT_FOLLOW = ["View tweets", "Back"]

	def __init__(self, cursor, loginID, userID):
		"""
		Arguments:
		loginID -- the ID of the signed in user
		userID -- the ID of the user to view
		"""

		self._cursor = cursor
		self._loginID = loginID
		self._userID = userID
		self._userStats = UsersTableTools.getUserStats(cursor, userID)
		self._isFollowing = FollowsTableTools.isFollowing(cursor, loginID,
			userID)

	def showAndGet(self):
		"""
		Show the menu and return either ViewUserMenu.BACK_INDEX (if back
		option chosen) or None (if an exit key was pressed)
		"""

		choice = ViewUserMenu._INITIAL_INDEX

		while choice is not None and choice != ViewUserMenu.BACK_INDEX:
			choice = self._showAndGet()

		return choice

	def _showAndGet(self):
		"""
		Show the menu and return either ViewUserMenu.BACK_INDEX (if back
		option chosen) or None (if an exit key was pressed)
		"""

		preMessage = str(self._userID) + "\n\t" + str(self._userStats)

		if self._isFollowing:
			preMessage = "You follow this user\n" + preMessage
			options = ViewUserMenu._OPTIONS_WITHOUT_FOLLOW

		else:
			options = ViewUserMenu._OPTIONS

		menu = TerminalMenu(options, preMessage)
		choice = menu.showAndGet()

		if self._isFollowing: choice += 1

		# If an exit key was pressed, return None
		if choice is None: return None

		# If user chose to go back, return ViewUserMenu.BACK_INDEX
		if choice == ViewUserMenu.BACK_INDEX:
			return ViewUserMenu.BACK_INDEX

		# If user chose to follow, follow
		elif choice == ViewUserMenu._FOLLOW_INDEX:
			date = DateTools.getCurrentDate()
			FollowsTableTools.follow(self._cursor, self._loginID, self._userID,
				date)
			self._isFollowing = True

		# If user chose to view tweets, view tweets
		else:
			tweetsMenu = UserTweetsMenu(self._cursor, self._loginID,
				self._userID)
			result = tweetsMenu.showAndGet()
			if result is None: return None        # If an exit key was pressed

		return ViewUserMenu._INITIAL_INDEX