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

		return "rank() over(order by {0} {1}) {2}".format(over, order,
			statementName)

	@staticmethod
	def yieldResults(cursor, statement):
		"""Yield each result of the given statement"""

		cursor.execute(statement)
		result = cursor.fetchone()

		while result is not None:
			yield result
			result = cursor.execute(statement)

	@staticmethod
	def yieldRankedResults(cursor, statement, rankName = "rank"):
		"""
		Yield each result of the given statement ordered by the value stored in
		the column named rankName
		"""

		print("select * from ({0}) where rank = 1".format(statement) + "\n\n")

		cursor.execute("select * from ({0}) where rank = 1".format(statement))

		result = cursor.fetchone()

		i = 1

		while result is not None:

			yield result

			i += 1

			result = cursor.execute(
				"select * from ({0}) where rank = {1}".format(statement, i))

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
	_FOLLOWS_TABLE = "Follows"

	@staticmethod
	def addTweet(cursor, writer, date, text, tweetID, replyTo = None):
		"""Add the given tweet to the 'Tweets' table"""

		# Add quotation marks to text
		text = TableTools.addQuotes(text)

		# Replace None with "null"
		writer = TableTools.replaceWithNull(writer)
		date = TableTools.replaceWithNull(date)
		text = TableTools.replaceWithNull(text)
		replyTo = TableTools.replaceWithNull(replyTo)

		cursor.execute(
			"insert into {0} values ({1}, {2}, {3}, {4}, {5})".format(
				TweetsTableTools._TWEETS_TABLE, tweetID, writer, date, text,
				replyTo))

	@staticmethod
	def getFolloweeTweetsByDate(cursor, follower):
		"""
		Yield each tweet from the followees of the given user by date (recent
		first)

		Yield as Tweet object

		Keyword arguments:
        follower -- the ID of the follower
		"""

		columns = "tid, writer, tdate, text, replyto"

		rankStatement = TableTools.rankStatement("tdate")

		rankedSelect = "select {0}, {1} from {2}, {3} ".format(
			columns, rankStatement, TweetsTableTools._TWEETS_TABLE,
			TweetsTableTools._FOLLOWS_TABLE) + \
			"where flwer = {0} and writer = flwee".format(follower)

		for result in TableTools.yieldRankedResults(cursor, rankedSelect):
			yield Tweet(result[0], result[1], result[2], result[3], result[4])

	@staticmethod
	def getTweetsByDate(cursor, userID):
		"""
		Yield each tweet from the given user by date (recent first)

		Yield as Tweet object

		Keyword arguments:
        userID -- the ID of the writer of the tweets
		"""

		columns = "tid, tdate, text, replyto"

		rankStatement = TableTools.rankStatement("tdate")
		rankedSelect = "select {0}, {1} from {2}".format(columns,
			rankStatement, TweetsTableTools._TWEETS_TABLE)

		for result in TableTools.yieldRankedResults(cursor, rankedSelect):
			yield Tweet(result[0], userID, result[1], result[2], result[3])

class FollowsTableTools:
	"""Tools for working with the 'Follows' table"""

	_FOLLOWS_TABLE = "Follows"

	@staticmethod
	def getFollowers(cursor, followee):
		"""Yield the user ID for each person being following followee"""

		statement = "select flwer from {0} where flwee = '{1}'".format(
			FollowsTableTools._FOLLOWS_TABLE, followee)

		for result in TableTools.yieldResults(cursor, statement):
			yield result

	@staticmethod
	def getFollowing(cursor, follower):
		"""Yield the user ID for each person being followed by follower"""

		statement = "select flwee from {0} where flwer = '{1}'".format(
			FollowsTableTools._FOLLOWS_TABLE, follower)

		for result in TableTools.yieldResults(cursor, statement):
			yield result

class UsersTableTools:
	"""Tools for working with the 'Users' table"""

	_USERS_TABLE = "Users"
	_MAX_PASSWORD_LENGTH = 4

	@staticmethod
	def findUsers(cursor, keyword):
		"""
		Yield each user whose name or city contains the given keyword (yield
		matching names first and sort by value length)
		"""

		for user in UsersTableTools.findUsersByName(cursor, keyword):
			yield user

		for user in UsersTableTools.findUsersByCity(cursor, keyword):
			yield user

	@staticmethod
	def findUsersByName(cursor, keyword):
		"""
		Yield each user whose name contains the given keyword (sort by name
		length)
		"""

		rankStatement = TableTools.rankStatement("length(usr)",
			descending = False)

		rankedSelect = \
			"select usr, {0} from {1} where name like '%{2}%'".format(
				rankStatement, UsersTableTools._USERS_TABLE, keyword)

		for result in TableTools.yieldRankedResults(cursor, rankedSelect):
			yield result

	@staticmethod
	def findUsersByCity(cursor, keyword):
		"""
		Yield each user whose city contains the given keyword (sort by city
		length)
		"""

		rankStatement = TableTools.rankStatement("length(city)",
			descending = False)

		rankedSelect = \
			"select city, {0} from {1} where name like '%{2}%'".format(
				rankStatement, UsersTableTools._USERS_TABLE, keyword)

		for result in TableTools.yieldRankedResults(cursor, rankedSelect):
			yield result

	@staticmethod
	def addUser(cursor, password, name, email, city, timezone, userID):
		"""Add a new user"""

		# Add quotation marks to string values
		password = TableTools.addQuotes(password)
		name = TableTools.addQuotes(name)
		email = TableTools.addQuotes(email)
		city = TableTools.addQuotes(city)

		# Replace None with "null"
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