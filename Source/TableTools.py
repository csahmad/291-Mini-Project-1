class TableTools:
	"""Static methods for getting information about tables"""

	@staticmethod
	def itemExists(cursor, tableName, columnName, item):
		"""Return whether the given string value exists in the given table"""

		cursor.execute(
			"select unique {1} from {0} where {1} = {2}".format(
				tableName, columnName, item))

		result = cursor.fetchone()

		if result is None: return False
		return True

	@staticmethod
	def addQuotes(stringValue):
		"""
		Add single quotes around the given string value and return

		Return None if None given
		"""

		if stringValue is None: return None
		return "'{0}'".format(stringValue)

	@staticmethod
	def replaceWithNull(string):
		"""If None passed, return 'null', otherwise return string"""

		if string is None: return "null"
		return string

	@staticmethod
	def rankStatement(over, descending = True,
		statementName = "rank"):
		"""Return a rank() over statement"""

		if descending:
			order = "desc"

		else:
			order = "asc"

		return "rank() over({0}) {1}) {2}".format(over, order, statementName)

class Tweet:
	"""Represents a tweet"""

	def __init__(self, tweetID, writer, date, text, replyTo = None):

		if replyTo == "null": replyTo = None
		self._tweetID = tweetID
		self._writer = writer
		self._date = date
		self._text = text
		self._replyTo = replyTo

	def __str__(self):

		if self._replyTo is None:
			replyToString = ""

		else:
			replyToString = "@{0} ".format(replyTo)

		return "{0}: {1}{2} ({3})".format(self._writer, replyToString,
			self._text, self._date)

	@property
	def tweetID(self):
		"""Return the tweet ID"""

		return self._tweetID

	@property
	def writer(self):
		"""Return the writer of the tweet"""

		return self._writer

	@property
	def date(self):
		"""Return the date the tweet was written"""

		return self._date

	@property
	def text(self):
		"""Return the tweet text"""

		return self._text

	@property
	def replyTo(self):
		"""Return the tweet ID this tweet is a reply to or None"""

		return self._replyTo

class TweetsTableTools:
	"""Tools for working with the 'Tweets' table"""

	_TWEETS_TABLE = "Tweets"

	@staticmethod
	def getTweetsByDate(cursor, userID, amount = None):
		"""
		Yield each tweet from the given user by date (recent first)

		Yield as Tweet object

		Keyword arguments:
        userID -- the ID of the writer of the tweets
        amount -- the maximum number of tweets to yield or None (to yield all
        	tweets)
		"""

		columns = "tid, tdate, text, replyto"

		rankStatement = TableTools.rankStatement("max(tdate)")
		rankedSelect = "select {0}, {1}".format(columns,
			rankStatement) + "from {0}".format(TweetsTableTools._TWEETS_TABLE)

		cursor.execute("select {0} from ({1}) where rank = 1".format(
			columns, rankedSelect))

		result = cursor.fetchone()

		i = 1

		while result is not None:

			yield Tweet(result[0], userID, result[1], result[2], result[3])

			i += 1

			if amount is not None and i > amount: break

			cursor.execute("select {0} from ({1}) where rank = {2}".format(
				columns, rankedSelect, i))

class FollowsTableTools:
	"""Tools for working with the 'Follows' table"""

	_FOLLOWS_TABLE = "Follows"

	@staticmethod
	def getFollowing(cursor, follower):
		"""Yield the user ID for each person being followed by follower"""

		cursor.execute("select flwee from {0} where flwer = '{1}'".format(
			FollowsTableTools._FOLLOWS_TABLE, follower))

		result = cursor.fetchone()

		while result is not None:
			yield result[1]
			result = cursor.fetchone()

class UsersTableTools:
	"""Tools for working with the 'Users' table"""

	_USERS_TABLE = "Users"
	_MAX_PASSWORD_LENGTH = 4

	@staticmethod
	def addUser(cursor, password, name, email, city, timezone, userID):
		"""Add a new user"""

		# Add quotation marks to string values
		password = TableTools.addQuotes(password)
		name = TableTools.addQuotes(name)
		email = TableTools.addQuotes(email)
		city = TableTools.addQuotes(city)

		# Replace None with "null"
		userID = TableTools.replaceWithNull(userID)
		password = TableTools.replaceWithNull(password)
		name = TableTools.replaceWithNull(name)
		email = TableTools.replaceWithNull(email)
		city = TableTools.replaceWithNull(city)
		timezone = TableTools.replaceWithNull(timezone)

		insertStatement = "insert into {0} values ".format(
			UsersTableTools._USERS_TABLE) + \
			"({0}, {1}, {2}, {3}, {4}, {5})".format(
			userID, password, name, email, city, timezone)

		cursor.execute(insertStatement)

	@staticmethod
	def userExists(cursor, userID):
		"""Return whether the user exists"""

		return TableTools.itemExists(cursor, UsersTableTools._USERS_TABLE,
			"usr", userID)

	@staticmethod
	def loginExists(cursor, userID, password):
		"""Return whether the given username, password combination exists"""

		if len(password) > UsersTableTools._MAX_PASSWORD_LENGTH: return False

		cursor.execute(
		"select usr, pwd from {0} where usr = {1} and pwd = '{2}'".format(
			UsersTableTools._USERS_TABLE, userID, password))

		result = cursor.fetchone()

		if result is None: return False
		return True