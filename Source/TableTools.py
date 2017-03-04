from TweetTools import Tweet, TweetStats
from UserTools import User, UserStats

class TableTools:
	"""Static methods for getting information about tables"""

	@staticmethod
	def exists(connection, tableName, columnValues):
		"""
		Return whether the given column values exist in the given table

		Arguments:
		tableName -- the name of the table to check
		columnValues -- a dictionary in the format {columnName: value}
		"""

		cursor = connection.cursor()

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
	def itemExists(connection, tableName, item, columnName):
		"""
		Return whether the given value exists in the given table

		If no column name given, assume table only has one column
		"""

		cursor = connection.cursor()

		variables = {"value": item}

		cursor.execute("select {0} from {1} where {0} = :value".format(
			columnName, tableName), variables)

		result = cursor.fetchone()

		if result is None: return False
		return True

	@staticmethod
	def yieldResults(connection, statement, variables = None):
		"""Yield each result of the given statement"""

		cursor = connection.cursor()

		if variables is None:
			cursor.execute(statement)

		else:
			cursor.execute(statement, variables)

		result = cursor.fetchone()

		while result is not None:
			yield result
			result = cursor.fetchone()

	@staticmethod
	def getCount(connection, tableName, condition = None, variables = None,
		unique = False):
		"""
		Return the number of rows in the given table that match the given
		condition

		Return the total number of rows if no condition given
		Do not include the "where" keyword in condition
		"""

		cursor = connection.cursor()

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
	def insertMany(connection, tableName, values, inputSizes = None,
		insertsAtOnce = 20):
		"""
		Insert each collection (list/tuple) in values (list/tuple) into the
		given table

		Arguments:
		tableName -- the name of the table to insert the values into
		values -- a collection (list/tuple) of collections (list/tuple) of
			values, with each sub-collection entered into the table
			For example, [("John", 22), ("Jane", 23)]
		inputSizes -- a list/tuple with the type of each value to be inserted
			or the maximum length of the value if the value is a string
			For example, for the values [("Johnie", 22), ("Jane", 23)],
			inputSizes might be (6, int)
		insertsAtOnce -- how many insert statements to combine into one (how
			many collections of values to insert into the table at a time)
		"""

		length = len(values)

		# If values is empty (if there are no values to insert), return
		if length == 0: return

		# If there is only one set of values to enter, call TableTools.insert
		# and return
		if length == 1:
			TableTools.insert(connection, tableName, values[0])
			return

		cursor = connection.cursor()
		cursor.bindarraysize = insertsAtOnce

		if inputSizes is not None:
			cursor.setinputsizes(*inputSizes)

		# Get a string of the variable names (eg. ":1, :2, :3")
		variableNames = ", ".join([":" + str(i + 1) for i in range(length)])

		cursor.executemany("insert into {0} values ({1})".format(tableName,
			variableNames), values)

	@staticmethod
	def insert(connection, tableName, values):
		"""Insert the given values (list/tuple) into the given table"""

		cursor = connection.cursor()

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
	def insertItem(connection, tableName, value):
		"""Insert the given value into the given one-column table"""

		cursor = connection.cursor()

		variables = {"value": value}

		cursor.execute("insert into {0} values (:value)".format(tableName),
			variables)

	@staticmethod
	def insertItemIfNew(connection, tableName, value, columnName):
		"""
		Insert the given value into the given one-column table if the item does
		not yet exist in the table
		"""

		if not TableTools.itemExists(connection, tableName, value, columnName):
			TableTools.insertItem(connection, tableName, value)

class TweetsTableTools:
	"""Tools for working with tweets"""

	_TWEETS_TABLE = "Tweets"
	_FOLLOWS_TABLE = "Follows"
	_HASHTAGS_TABLE = "Hashtags"
	_MENTIONS_TABLE = "Mentions"
	_RETWEETS_TABLE = "Retweets"

	@staticmethod
	def findTweets(connection, keywords):
		"""
		Find tweets that contain any of the given keywords

		If a keyword starts with "#", interpret as hashtag
		"""

		pass

	@staticmethod
	def retweet(connection, tweetID, userID, date):
		"""Add a retweet to the 'Retweets' table"""

		TableTools.insert(connection, TweetsTableTools._RETWEETS_TABLE,
			[userID, tweetID, date])

	@staticmethod
	def isRetweetedByUser(connection, tweetID, userID):
		"""Return whether the given tweet was retweeted by the given user"""

		return TableTools.exists(connection, TweetsTableTools._RETWEETS_TABLE,
			{"tid": tweetID, "usr": userID})

	@staticmethod
	def getTweetStats(connection, tweetID):
		"""Return a TweetStats object for the tweet with the given ID"""

		return TweetStats(
			TweetsTableTools.getRetweetCount(connection, tweetID),
			TweetsTableTools.getReplyCount(connection, tweetID))

	@staticmethod
	def getRetweetCount(connection, tweetID):
		"""Return the number of retweets the tweet with the given ID has"""

		variables = {"tweetID": tweetID}

		return TableTools.getCount(connection,
			TweetsTableTools._RETWEETS_TABLE, "tid = :tweetID", variables)

	@staticmethod
	def getReplyCount(connection, tweetID):
		"""Return the number of replies to the tweet with the given ID"""

		variables = {"tweetID": tweetID}

		return TableTools.getCount(connection, TweetsTableTools._TWEETS_TABLE,
			"replyto = :tweetID", variables)

	@staticmethod
	def addTweet(connection, writer, date, text, tweetID, replyTo = None,
		hashtags = None):
		"""
		Add the given tweet to the 'Tweets' table

		The given hashtags should not contain the "#" at the beginning
		"""

		TableTools.insert(connection, TweetsTableTools._TWEETS_TABLE,
			[tweetID, writer, date, text, replyTo])

		mentionsValues = []

		for hashtag in hashtags:

			TableTools.insertItemIfNew(connection,
				TweetsTableTools._HASHTAGS_TABLE, hashtag, "term")

			mentionsValues.append((tweetID, hashtag))

		TableTools.insertMany(connection, TweetsTableTools._MENTIONS_TABLE,
			mentionsValues, (int, 10))

	@staticmethod
	def getFolloweeTweetsByDate(connection, follower):
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

		for result in TableTools.yieldResults(connection, statement,
			variables):

			yield Tweet(result[0], result[1], result[2], result[3], result[4])

	@staticmethod
	def getTweetsByDate(connection, userID):
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

		for result in TableTools.yieldResults(connection, statement):
			yield Tweet(result[0], userID, result[1], result[2], result[3])

class FollowsTableTools:
	"""Tools for working with the 'Follows' table"""

	_FOLLOWS_TABLE = "Follows"

	@staticmethod
	def getFollowers(connection, followee):
		"""Yield the user ID for each person following followee"""

		variables = {"followee": followee}

		statement = "select flwer from {0} where flwee = :followee".format(
			FollowsTableTools._FOLLOWS_TABLE)

		for result in TableTools.yieldResults(connection, statement,
			variables):

			yield UsersTableTools.getUser(connection, result[0])

	@staticmethod
	def getFollowing(connection, follower):
		"""Yield the user ID for each person being followed by follower"""

		variables = {"follower": follower}

		statement = "select flwee from {0} where flwer = :follower".format(
			FollowsTableTools._FOLLOWS_TABLE)

		for result in TableTools.yieldResults(connection, statement,
			variables):

			yield UsersTableTools.getUser(connection, result[0])

	@staticmethod
	def follow(connection, follower, followee, date):
		"""Make follower follow followee"""

		TableTools.insert(connection, FollowsTableTools._FOLLOWS_TABLE,
			[follower, followee, date])

	@staticmethod
	def isFollowing(connection, follower, followee):
		"""Return whether follower is following followee"""

		return TableTools.exists(connection, FollowsTableTools._FOLLOWS_TABLE,
			{"flwer": follower, "flwee": followee})

class UsersTableTools:
	"""Tools for working with users"""

	_USERS_TABLE = "Users"
	_FOLLOWS_TABLE = "Follows"
	_TWEETS_TABLE = "Tweets"

	@staticmethod
	def getUser(connection, userID):
		"""Get a User object given a user ID"""

		cursor = connection.cursor()

		columns = "usr, name, email, city, timezone"
		variables = {"userID": userID}

		statement = "select {0} from {1} where usr = :userID".format(columns,
			UsersTableTools._USERS_TABLE)

		cursor.execute(statement, variables)
		result = cursor.fetchone()

		return User(result[0], result[1], result[2], result[3], result[4])

	@staticmethod
	def getUserStats(connection, userID):
		"""Return a UserStats object for the user with the given ID"""

		return UserStats(UsersTableTools.getTweetCount(connection, userID),
			UsersTableTools.getFollowingCount(connection, userID),
			UsersTableTools.getFollowerCount(connection, userID))

	@staticmethod
	def getTweetCount(connection, userID):
		"""Return the number of tweets from the given user"""

		variables = {"userID": userID}

		return TableTools.getCount(connection, UsersTableTools._TWEETS_TABLE,
			"writer = :userID", variables)

	@staticmethod
	def getFollowingCount(connection, userID):
		"""Return the number of people this user is following"""

		variables = {"userID": userID}

		return TableTools.getCount(connection, UsersTableTools._FOLLOWS_TABLE,
			"flwer = :userID", variables)

	@staticmethod
	def getFollowerCount(connection, userID):
		"""Return the number of people following this user"""

		variables = {"userID": userID}

		return TableTools.getCount(connection, UsersTableTools._FOLLOWS_TABLE,
			"flwee = :userID", variables)

	@staticmethod
	def findUsers(connection, keyword):
		"""
		Yield each user whose name or city contains the given keyword (yield
		matching names first and sort by value length)
		"""

		for user in UsersTableTools.findUsersByName(connection, keyword):
			yield user

		for user in UsersTableTools._usersByCityNotName(connection, keyword):
			yield UsersTableTools.getUser(connection, user[0])

	@staticmethod
	def findUsersByName(connection, keywords):
		"""
		Yield each user whose name contains any of the given keywords (sort by
		name length)
		"""

		joinedKeywords = "|".join(keywords)
		variables = {"keywords": joinedKeywords}

		select = "select usr from {0} ".format(UsersTableTools._USERS_TABLE)
		where = "where regexp_like (name, :keywords, 'i') "
		orderBy = "order by length(usr) asc"

		statement = select + where + orderBy

		for result in TableTools.yieldResults(connection, statement,
			variables):

			yield UsersTableTools.getUser(connection, result[0])

	@staticmethod
	def _usersByCityNotName(connection, keywords):
		"""
		Yield each user whose city contains any of the given keywords, but
		whose name does not contain any of the given keyword (sort by city
		length)
		"""

		joinedKeywords = "|".join(keywords)
		variables = {"keywords": joinedKeywords}

		select = "select usr from {0} ".format(UsersTableTools._USERS_TABLE)
		where1 = "where regexp_like (city, :keywords, 'i') and "
		where2 = "not regexp_like (name, :keywords, 'i') "
		orderBy = "order by length(city) asc"

		statement = select + where1 + where2 + orderBy

		for result in TableTools.yieldResults(connection, statement,
			variables):

			yield result[0]

	@staticmethod
	def addUser(connection, password, name, email, city, timezone, userID):
		"""Add a new user"""

		TableTools.insert(connection, UsersTableTools._USERS_TABLE,
			[userID, password, name, email, city, timezone])

	@staticmethod
	def userExists(connection, userID):
		"""Return whether the user exists"""

		return TableTools.itemExists(connection, UsersTableTools._USERS_TABLE,
			userID, "usr")

	@staticmethod
	def loginExists(connection, userID, password):
		"""Return whether the given username, password combination exists"""

		cursor = connection.cursor()

		variables = {"userID": userID, "password": password}

		select = "select usr, pwd from {0} ".format(
			UsersTableTools._USERS_TABLE)

		where = "where usr = :userID and pwd = :password"

		cursor.execute(select + where, variables)
		result = cursor.fetchone()

		if result is None: return False
		return True