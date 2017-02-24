class TableTools:
	"""Static methods for getting information about tables"""

	@staticmethod
	def exists(cursor, tableName, columnValues):
		"""
		Return whether the given column values exist in the given table

		Replaces None values with "null"
		Does not add quotation marks to strings

		Arguments:
		tableName -- the name of the table to check
		columnValues -- a dictionary in the format {columnName: value}
		"""

		whereConditions = []

		for column, value in columnValues.items():
			if value is None: value = "null"
			whereConditions.append("{0} = {1}".format(column, value))

		whereString = "where " + " and ".join(whereConditions)

		statement = "select unique * from {0} ".format(
			tableName) + whereString

		cursor.execute(statement)

		result = cursor.fetchone()

		if result is None: return False
		return True

	@staticmethod
	def itemExists(cursor, tableName, item, columnName = None):
		"""
		Return whether the given value exists in the given table

		If no column name given, assume table only has one column
		Does not add quotation marks if item is a string
		"""

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

		cursor.execute("select * from ({0}) where rank = 1".format(statement))

		result = cursor.fetchone()

		i = 1

		while result is not None:

			yield result

			i += 1

			result = cursor.execute(
				"select * from ({0}) where rank = {1}".format(statement, i))

	@staticmethod
	def getCount(cursor, tableName, condition = None, unique = False):
		"""
		Return the number of rows in the given table that match the given
		condition

		Return the total number of rows if no condition given
		Do not include the "where" keyword in condition
		"""

		if unique:
			start = "select unique count(*) from {0}".format(tableName)

		else:
			start = "select count(*) from {0}".format(tableName)

		if condition is None:
			end = ""

		else:
			end = " where {0}".format(condition)

		cursor.execute(start + end)
		return cursor.fetchone()[0]

	@staticmethod
	def insert(cursor, tableName, values):
		"""
		Insert the given values (list) into the given table

		Replaces None with "null"
		Does not add quotation marks to strings
		"""

		for i in range(len(values)):
			if values[i] is None: values[i] = "null"
			values[i] = str(values[i])

		cursor.execute("insert into {0} values ({1})".format(tableName,
			", ".join(values)))

	@staticmethod
	def insertItem(cursor, tableName, value):
		"""
		Insert the given value into the given one-column table

		Does not add quotation marks if the given value is a string
		"""

		cursor.execute("insert into {0} values ({1})".format(tableName, value))

	@staticmethod
	def insertItemIfNew(cursor, tableName, value):
		"""
		Insert the given value into the given one-column table if the item does
		not yet exist in the table

		Does not add quotation marks if the given value is a string
		"""

		if not TableTools.itemExists(cursor, tableName, value):
			TableTools.insertItem(cursor, tableName, value)

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

class TweetStats:
	"""Contains stats for a tweet"""

	def __init__(self, retweetCount, replyCount):

		self._retweetCount = retweetCount
		self._replyCount = replyCount

	def __str__(self):

		return "{0} Retweets | {1} Replies".format(self._retweetCount,
			self._replyCount)

	@property
	def retweetCount(self):
		"""Get the number of retweets"""

		return self._retweetCount

	@property
	def replyCount(self):
		"""Get the number of replies"""

		return self._replyCount

	def addRetweet(self):
		"""Increase retweet count by one"""

		self._retweetCount += 1

	def addReply(self):
		"""Increase reply count by one"""

		self._replyCount += 1

class TweetsTableTools:
	"""Tools for working with tweets"""

	_TWEETS_TABLE = "Tweets"
	_FOLLOWS_TABLE = "Follows"
	_HASHTAGS_TABLE = "Hashtags"
	_MENTIONS_TABLE = "Mentions"
	_RETWEETS_TABLE = "Retweets"

	@staticmethod
	def findTweets(cursor, keywords):
		"""
		Find tweets that contain any of the given keywords

		If a keyword starts with "#", interpret as hashtag
		"""

		pass

	@staticmethod
	def retweet(cursor, tweetID, userID, date):
		"""Add a retweet to the 'Retweets' table"""

		TableTools.insert(cursor, TweetsTableTools._RETWEETS_TABLE,
			[userID, tweetID, date])

	@staticmethod
	def isRetweetedByUser(cursor, tweetID, userID):
		"""Return whether the given tweet was retweeted by the given user"""

		return TableTools.exists(cursor, TweetsTableTools._RETWEETS_TABLE,
			{"tid": tweetID, "usr": userID})

	@staticmethod
	def getTweetStats(cursor, tweetID):
		"""Return a TweetStats object for the tweet with the given ID"""

		return TweetStats(TweetsTableTools.getRetweetCount,
			TweetsTableTools.getReplyCount(cursor, tweetID))

	@staticmethod
	def getRetweetCount(cursor, tweetID):
		"""Return the number of retweets the tweet with the given ID has"""

		return TableTools.getCount(cursor, TweetsTableTools._RETWEETS_TABLE,
			"tid = {0}".format(tweetID))

	@staticmethod
	def getReplyCount(cursor, tweetID):
		"""Return the number of replies to the tweet with the given ID"""

		return TableTools.getCount(cursor, TweetsTableTools._TWEETS_TABLE,
			"replyto = {0}".format(tweetID))

	@staticmethod
	def addTweet(cursor, writer, date, text, tweetID, replyTo = None,
		hashtags = None):
		"""
		Add the given tweet to the 'Tweets' table

		The given hashtags should not contain the "#" at the beginning
		"""

		# Add quotation marks to text
		text = TableTools.addQuotes(text)

		# Replace None with "null"
		writer = TableTools.replaceWithNull(writer)
		date = TableTools.replaceWithNull(date)
		text = TableTools.replaceWithNull(text)
		replyTo = TableTools.replaceWithNull(replyTo)

		TableTools.insert(cursor, TweetsTableTools._TWEETS_TABLE,
			[tweetID, writer, date, text, replyTo])

		for hashtag in hashtags:

			hashtag = "'{0}'".format(hashtag)

			TableTools.insertItemIfNew(cursor,
				TweetsTableTools._HASHTAGS_TABLE, hashtag)

			TableTools.insert(cursor,
				TweetsTableTools._MENTIONS_TABLE, tweetID, hashtag)

	@staticmethod
	def getFolloweeTweetsByDate(cursor, follower):
		"""
		Yield each tweet from the followees of the given user by date (recent
		first)

		Yield as Tweet object

		Arguments:
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

		Arguments:
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

		for user in UsersTableTools._usersByCityNotName(cursor, keyword):
			yield user

	@staticmethod
	def findUsersByName(cursor, keywords):
		"""
		Yield each user whose name contains any of the given keywords (sort by
		name length)
		"""

		# Make keywords lowercase and surround each with "%"s and "'"s
		keywords = ["'%{0}%'".format(keyword.lower())
			for keyword in keywords]

		rankStatement = TableTools.rankStatement("length(usr)",
			descending = False)

		rankedSelect = \
			"select usr, {0} from {1} where lower(name) like any({2})".format(
				rankStatement, UsersTableTools._USERS_TABLE,
				", ".join(keywords))

		for result in TableTools.yieldRankedResults(cursor, rankedSelect):
			yield result

	@staticmethod
	def _usersByCityNotName(cursor, keywords):
		"""
		Yield each user whose city contains any of the given keywords, but
		whose name does not contain any of the given keyword (sort by city
		length)
		"""

		# Make keywords lowercase and surround each with "%"s and "'"s
		keywords = ["'%{0}%'".format(keyword.lower())
			for keyword in keywords]

		anyString = "any({0})".format(", ".join(keywords))

		rankStatement = TableTools.rankStatement("length(city)",
			descending = False)

		whereConditions = \
			"lower(city) like {0} and lower(name) not like {0}".format(
				anyString)

		rankedSelect = \
			"select usr, {0} from {1} where ".format(rankStatement,
				UsersTableTools._USERS_TABLE) + whereConditions

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

		TableTools.insert(cursor, UsersTableTools._USERS_TABLE,
			[userID, password, name, email, city, timezone])

	@staticmethod
	def userExists(cursor, userID):
		"""Return whether the user exists"""

		return TableTools.itemExists(cursor, UsersTableTools._USERS_TABLE,
			userID, "usr")

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