from TweetTools import Tweet, TweetStats
from UserTools import UserStats

class TableTools:
	"""Static methods for getting information about tables"""

	@staticmethod
	def exists(cursor, tableName, columnValues):
		"""
		Return whether the given column values exist in the given table

		Arguments:
		tableName -- the name of the table to check
		columnValues -- a dictionary in the format {columnName: value}
		"""

		variables = {}
		whereConditions = []

		i = 0

		for column, value in columnValues.items():
			valueString = "value{0}".format(i)
			variableName = ":" + valueString
			variables[valueString] = value
			whereConditions.append("{0} = {1}".format(column, variableName))
			i += 1

		whereString = " and ".join(whereConditions)

		statement = "select unique * from {0} where {1}".format(tableName,
			whereString)

		cursor.execute(statement, variables)
		result = cursor.fetchone()

		if result is None: return False
		return True

	@staticmethod
	def itemExists(cursor, tableName, item, columnName):
		"""
		Return whether the given value exists in the given table

		If no column name given, assume table only has one column
		"""

		variables = {"value": item}

		cursor.execute(
			"select unique {0} from {1} where {0} = :value".format(columnName,
				tableName), variables)

		result = cursor.fetchone()

		if result is None: return False
		return True

	@staticmethod
	def yieldResults(cursor, statement, variables = None):
		"""Yield each result of the given statement"""

		if variables is None:
			cursor.execute(statement)

		else:
			cursor.execute(statement, variables)

		result = cursor.fetchone()

		while result is not None:
			yield result
			result = cursor.fetchone()

	@staticmethod
	def getCount(cursor, tableName, condition = None, variables = None,
		unique = False):
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

			if variables is None:
				raise ValueError(
					"Cannot provide a condition without providing variables.")

			end = " where {0}".format(condition)

		statement = start + end

		if variables is None:
			cursor.execute(statement)

		else:
			cursor.execute(statement, variables)

		return cursor.fetchone()[0]

	@staticmethod
	def insert(cursor, tableName, values):
		"""Insert the given values (list) into the given table"""

		variables = {}
		variableNames = []

		for i in range(len(values)):
			valueString = "value{0}".format(i)
			variableNames.append(":" + valueString)
			variables[valueString] = values[i]

		variableString = ", ".join(variableNames)

		cursor.execute("insert into {0} values ({1})".format(tableName,
			variableString), variables)

	@staticmethod
	def insertItem(cursor, tableName, value):
		"""Insert the given value into the given one-column table"""

		variables = {"value": value}

		cursor.execute("insert into {0} values (:value)".format(tableName),
			variables)

	@staticmethod
	def insertItemIfNew(cursor, tableName, value, columnName):
		"""
		Insert the given value into the given one-column table if the item does
		not yet exist in the table

		"""

		if not TableTools.itemExists(cursor, tableName, value, columnName):
			TableTools.insertItem(cursor, tableName, value)

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

		return TweetStats(TweetsTableTools.getRetweetCount(cursor, tweetID),
			TweetsTableTools.getReplyCount(cursor, tweetID))

	@staticmethod
	def getRetweetCount(cursor, tweetID):
		"""Return the number of retweets the tweet with the given ID has"""

		variables = {"tweetID": tweetID}

		return TableTools.getCount(cursor, TweetsTableTools._RETWEETS_TABLE,
			"tid = :tweetID", variables)

	@staticmethod
	def getReplyCount(cursor, tweetID):
		"""Return the number of replies to the tweet with the given ID"""

		variables = {"tweetID": tweetID}

		return TableTools.getCount(cursor, TweetsTableTools._TWEETS_TABLE,
			"replyto = :tweetID", variables)

	@staticmethod
	def addTweet(cursor, writer, date, text, tweetID, replyTo = None,
		hashtags = None):
		"""
		Add the given tweet to the 'Tweets' table

		The given hashtags should not contain the "#" at the beginning
		"""

		TableTools.insert(cursor, TweetsTableTools._TWEETS_TABLE,
			[tweetID, writer, date, text, replyTo])

		for hashtag in hashtags:

			TableTools.insertItemIfNew(cursor,
				TweetsTableTools._HASHTAGS_TABLE, hashtag, "term")

			TableTools.insert(cursor,
				TweetsTableTools._MENTIONS_TABLE, [tweetID, hashtag])

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
		variables = {"follower": follower}

		select = "select {0} from {1}, {2} ".format(columns,
			TweetsTableTools._TWEETS_TABLE, TweetsTableTools._FOLLOWS_TABLE)

		where = "where flwer = :follower and writer = flwee "
		orderBy = "order by tdate desc"

		statement = select + where + orderBy

		for result in TableTools.yieldResults(cursor, statement, variables):
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

		select = "select {0} from {1} ".format(columns,
			TweetsTableTools._TWEETS_TABLE)

		orderBy = "order by tdate desc"

		statement = select + orderBy

		for result in TableTools.yieldResults(cursor, statement):
			yield Tweet(result[0], userID, result[1], result[2], result[3])

class FollowsTableTools:
	"""Tools for working with the 'Follows' table"""

	_FOLLOWS_TABLE = "Follows"

	@staticmethod
	def getFollowers(cursor, followee):
		"""Yield the user ID for each person following followee"""

		variables = {"followee": followee}

		statement = "select flwer from {0} where flwee = :followee".format(
			FollowsTableTools._FOLLOWS_TABLE)

		for result in TableTools.yieldResults(cursor, statement, variables):
			yield result[0]

	@staticmethod
	def getFollowing(cursor, follower):
		"""Yield the user ID for each person being followed by follower"""

		variables = {"follower": follower}

		statement = "select flwee from {0} where flwer = :follower".format(
			FollowsTableTools._FOLLOWS_TABLE)

		for result in TableTools.yieldResults(cursor, statement, variables):
			yield result[0]

	@staticmethod
	def follow(cursor, follower, followee, date):
		"""Make follower follow followee"""

		TableTools.insert(cursor, FollowsTableTools._FOLLOWS_TABLE,
			[follower, followee, date])

	@staticmethod
	def isFollowing(cursor, follower, followee):
		"""Return whether follower is following followee"""

		return TableTools.exists(cursor, FollowsTableTools._FOLLOWS_TABLE,
			{"flwer": follower, "flwee": followee})

class UsersTableTools:
	"""Tools for working with users"""

	_USERS_TABLE = "Users"
	_FOLLOWS_TABLE = "Follows"
	_TWEETS_TABLE = "Tweets"

	@staticmethod
	def getUserStats(cursor, userID):
		"""Return a UserStats object for the user with the given ID"""

		return UserStats(UsersTableTools.getTweetCount(cursor, userID),
			UsersTableTools.getFollowingCount(cursor, userID),
			UsersTableTools.getFollowerCount(cursor, userID))

	@staticmethod
	def getTweetCount(cursor, userID):
		"""Return the number of tweets from the given user"""

		variables = {"userID": userID}

		return TableTools.getCount(cursor, UsersTableTools._TWEETS_TABLE,
			"writer = :userID", variables)

	@staticmethod
	def getFollowingCount(cursor, userID):
		"""Return the number of people this user is following"""

		variables = {"userID": userID}

		return TableTools.getCount(cursor, UsersTableTools._FOLLOWS_TABLE,
			"flwer = :userID", variables)

	@staticmethod
	def getFollowerCount(cursor, userID):
		"""Return the number of people following this user"""

		variables = {"userID": userID}

		return TableTools.getCount(cursor, UsersTableTools._FOLLOWS_TABLE,
			"flwee = :userID", variables)

	@staticmethod
	def findUsers(cursor, keyword):
		"""
		Yield each user whose name or city contains the given keyword (yield
		matching names first and sort by value length)
		"""

		for user in UsersTableTools.findUsersByName(cursor, keyword):
			yield user

		for user in UsersTableTools._usersByCityNotName(cursor, keyword):
			yield user[0]

	@staticmethod
	def findUsersByName(cursor, keywords):
		"""
		Yield each user whose name contains any of the given keywords (sort by
		name length)
		"""

		joinedKeywords = "|".join(keywords).replace("'", "")

		select = "select usr from {0} ".format(UsersTableTools._USERS_TABLE)
		where = "where regexp_like (name, '{0}', 'i') ".format(joinedKeywords)
		orderBy = "order by length(usr) asc"

		statement = select + where + orderBy

		for result in TableTools.yieldResults(cursor, statement):
			yield result[0]

	@staticmethod
	def _usersByCityNotName(cursor, keywords):
		"""
		Yield each user whose city contains any of the given keywords, but
		whose name does not contain any of the given keyword (sort by city
		length)
		"""

		joinedKeywords = "|".join(keywords).replace("'", "")

		select = "select usr from {0} ".format(UsersTableTools._USERS_TABLE)

		where1 = "where regexp_like (city, '{0}', 'i') and ".format(
			joinedKeywords)

		where2 = "not regexp_like (name, '{0}', 'i') ".format(joinedKeywords)

		orderBy = "order by length(city) asc"

		statement = select + where1 + where2 + orderBy

		for result in TableTools.yieldResults(cursor, statement):
			yield result[0]

	@staticmethod
	def addUser(cursor, password, name, email, city, timezone, userID):
		"""Add a new user"""

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

		variables = {"userID": userID, "password": password}

		select = "select usr, pwd from {0} ".format(
			UsersTableTools._USERS_TABLE)

		where = "where usr = :userID and pwd = :password"

		cursor.execute(select + where, variables)
		result = cursor.fetchone()

		if result is None: return False
		return True