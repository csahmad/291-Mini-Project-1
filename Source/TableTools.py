import cx_Oracle

from Constants import Constants
from TweetTools import Tweet, TweetStats
from UserTools import User, UserStats

class TableTools:
	"""Static methods for getting information about tables"""

	@staticmethod
	def execute(connection, cursor, statement, variables = None,
		inputSizes = None, statementsAtOnce = None,
		stringsToFixedChars = True,
		commit = Constants.COMMIT_CHANGES):
		"""
		Execute the given statement with the given cursor

		Arguments:
		cursor -- the cursor to execute the statement with
		statement -- the SQL statement to execute
		variables -- any variables to pass to Cursor.execute or
			Cursor.executemany (if statementsAtOnce not None) as a list (not
			tuple) or dictionary
		inputSizes -- a list (not tuple) or dictionary with the type of each
			variable (in the same format as the arguments passed to
			Cursor.setinputsizes)
		statementsAtOnce -- how many statements to combine into one
			(bindarraysize)
		stringsToFixedChars -- whether to convert each integer in inputSizes to
			a cx_Oracle.FIXED_CHAR variable type with the length of the integer
		commit -- whether to commit changes after executing the statement
		"""

		# If inputSizes given, pass it to cursor.setinputsizes
		if inputSizes is not None:

			# Change string types to fixed char types (if that option is set to
			# True)
			if stringsToFixedChars:
				TableTools.stringsToFixedChars(cursor, inputSizes)

			if isinstance(inputSizes, dict):
				cursor.setinputsizes(**inputSizes)

			else:
				cursor.setinputsizes(*inputSizes)

		# If should only execute one statement, set executeMethod to
		# cursor.execute
		if statementsAtOnce is None or len(variables) == 1:

			if statementsAtOnce is not None:
				variables = variables[0]

			executeMethod = cursor.execute

		# If should execute many statements, set executeMethod to
		# cursor.executemany
		else:

			# If no values given, return
			if len(variables) == 0:
				return

			cursor.bindarraysize = statementsAtOnce
			executeMethod = cursor.executemany

		if variables is None:
			executeMethod(statement)

		else:
			executeMethod(statement, variables)

		if commit:
			connection.commit()

	@staticmethod
	def stringsToFixedChars(cursor, inputSizes):
		"""
		For the given inputSizes, convert each integer (representing the
		maximum length of a cx_Oracle.STRING variable) into a
		cx_Oracle.FIXED_CHAR variable type with the length of the integer

		Arguments:
		inputSizes -- a list (not tuple) or dictionary with the type of each
			variable (in the same format as the arguments passed to
			Cursor.setinputsizes)
		"""

		if isinstance(inputSizes, dict):

			for key, value in inputSizes.items():

				if isinstance(value, int):
					inputSizes[key] = TableTools.intToFixedChar(cursor, value)

		else:

			length = len(inputSizes)

			for i in range(length):

				if isinstance(inputSizes[i], int):

					inputSizes[i] = TableTools.intToFixedChar(cursor,
						inputSizes[i])

	@staticmethod
	def intToFixedChar(cursor, integer):
		"""
		Return a cx_Oracle.FIXED_CHAR variable type with the length of the
		given integer
		"""

		return cursor.var(cx_Oracle.FIXED_CHAR, integer)

	@staticmethod
	def exists(connection, tableName, columnValues, inputSizes = None):
		"""
		Return whether the given column values exist in the given table

		Arguments:
		tableName -- the name of the table to check
		columnValues -- a dictionary in the format {columnName: value}
		inputSizes -- a list (not tuple) or dictionary with the type of each
			variable (in the same format as the arguments passed to
			Cursor.setinputsizes)
		"""

		cursor = connection.cursor()

		variables = []
		whereConditions = []

		i = 1

		for column, value in columnValues.items():
			variables.append(value)
			whereConditions.append("{0} = :{1}".format(column, i))
			i += 1

		whereString = " and ".join(whereConditions)

		statement = "select unique * from {0} where {1}".format(tableName,
			whereString)

		TableTools.execute(connection, cursor, statement, variables,
			inputSizes)

		result = cursor.fetchone()

		if result is None: return False
		return True

	@staticmethod
	def itemExists(connection, tableName, item, columnName, inputSize = None):
		"""
		Return whether the given value exists in the given table

		If no column name given, assume table only has one column
		"""

		if inputSize is not None:
			inputSize = [inputSize]

		cursor = connection.cursor()

		variables = [item]

		statement = "select {0} from {1} where {0} = :1".format(
			columnName, tableName)

		TableTools.execute(connection, cursor, statement, variables, inputSize)
		result = cursor.fetchone()

		if result is None: return False
		return True

	@staticmethod
	def yieldResults(connection, statement, variables = None,
		inputSizes = None):
		"""Yield each result of the given statement"""

		cursor = connection.cursor()

		TableTools.execute(connection, cursor, statement, variables,
			inputSizes)

		result = cursor.fetchone()

		while result is not None:
			yield result
			result = cursor.fetchone()

	@staticmethod
	def getCount(connection, tableName, condition = None, variables = None,
		unique = False, inputSizes = None):
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

		TableTools.execute(connection, cursor, statement, variables,
			inputSizes)

		return cursor.fetchone()[0]

	@staticmethod
	def insert(connection, tableName, values, inputSizes = None,
		insertsAtOnce = None):
		"""
		Insert the given values (list/tuple) into the given table

		Arguments:
		tableName -- the name of the table to insert the values into
		values -- the values to insert into the table
		inputSizes -- a list (not tuple) or dictionary with the type of each
			variable (in the same format as the arguments passed to
			Cursor.setinputsizes)
		insertsAtOnce -- how many insert statements to combine into one (how
			many collections of values to insert into the table at a time)
		"""

		if insertsAtOnce is None:

			return TableTools._insert(connection, tableName, values,
				inputSizes)

		return TableTools._insertMany(connection, tableName, values,
			insertsAtOnce, inputSizes)

	@staticmethod
	def _insertMany(connection, tableName, values, insertsAtOnce,
		inputSizes = None):
		"""
		Insert each collection (list/tuple) in values (list/tuple) into the
		given table

		Arguments:
		tableName -- the name of the table to insert the values into
		values -- a collection (list/tuple) of collections (list/tuple) of
			values, with each sub-collection entered into the table
			For example, [("John", 22), ("Jane", 23)]
		inputSizes -- a list (not tuple) or dictionary with the type of each
			variable (in the same format as the arguments passed to
			Cursor.setinputsizes)
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

		# Get a string of the variable names (eg. ":0, :1, :2")
		variableNames = ", ".join([":" + str(i) for i in range(length)])

		statement = "insert into {0} values ({1})".format(tableName,
			variableNames)

		TableTools.execute(connection, cursor, statement, values, inputSizes,
			insertsAtOnce)

	@staticmethod
	def _insert(connection, tableName, values, inputSizes = None):
		"""Insert the given values (list/tuple) into the given table"""

		cursor = connection.cursor()

		variables = []
		variableNames = []

		for i in range(len(values)):
			variableNames.append(":{0}".format(i))
			variables.append(values[i])

		variableString = ", ".join(variableNames)

		statement = "insert into {0} values ({1})".format(tableName,
			variableString)

		TableTools.execute(connection, cursor, statement, variables,
			inputSizes)

	@staticmethod
	def insertItem(connection, tableName, value, inputSize = None):
		"""Insert the given value into the given one-column table"""

		if inputSize is not None:
			inputSize = [inputSize]

		cursor = connection.cursor()
		variables = [value]
		statement = "insert into {0} values (:1)".format(tableName)
		TableTools.execute(connection, cursor, statement, variables, inputSize)

	@staticmethod
	def insertItemIfNew(connection, tableName, value, columnName,
		inputSize = None):
		"""
		Insert the given value into the given one-column table if the item does
		not yet exist in the table
		"""

		if not TableTools.itemExists(connection, tableName, value, columnName,
			inputSize):

			TableTools.insertItem(connection, tableName, value, inputSize)

class TweetsTableTools:
	"""Tools for working with tweets"""

	_TWEETS_TABLE = "Tweets"
	_FOLLOWS_TABLE = "Follows"
	_HASHTAGS_TABLE = "Hashtags"
	_MENTIONS_TABLE = "Mentions"
	_RETWEETS_TABLE = "Retweets"

	@staticmethod
	def formatsearch (keyword):
			result = '%{0}%'.format(keyword.upper())
			return result

	@staticmethod
	def findTweets(connection, keywords):
		"""
		Find tweets that contain any of the given keywords

		If a keyword starts with "#", interpret as hashtag
		"""
		cursor = connection.cursor()
		
		if keywords[0]=='#' :
			TweetsTableTools.searchmentions(cursor, keywords.strip('#'))
		else:
			TweetsTableTools.searchtweet(cursor, keywords)
	
	@staticmethod
	def searchmentions(cursor, keyword):
		cursor.execute("select t.text, t.tdate from mentions m, tweets t where upper(m.term)='{0}' and t.tid=m.tid".format(keyword.upper()))
		result = cursor.fetchall()
		if len(result) != 0:
			print("Hashtag Results")
			Search.printtweets(result)
			return result

		else:
    		return None

	@staticmethod
	def searchtweet(cursor, keywords):
		statements = []       

		columns = "tid, tdate, text, replyto"

		for i in keywords:
				fi = TweetsTableTools.formatsearch(i)
				statements.append("select {0} where upper(text) like '{1}'".format(columns, fi))
	
		statement = "{0} {1}".format(" union ".join(statements), "order by tdate desc")

		print(statement)

		for result in TableTools.yieldResults(connection, statement,
			variables, [int]):

			yield Tweet(result[0], result[1], result[2], result[3])

	@staticmethod
	def retweet(connection, tweetID, userID, date):
		"""Add a retweet to the 'Retweets' table"""

		TableTools.insert(connection, TweetsTableTools._RETWEETS_TABLE,
			[userID, tweetID, date], [int, int, cx_Oracle.DATETIME])

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

		variables = [tweetID]

		return TableTools.getCount(connection,
			TweetsTableTools._RETWEETS_TABLE, "tid = :1", variables)

	@staticmethod
	def getReplyCount(connection, tweetID):
		"""Return the number of replies to the tweet with the given ID"""

		variables = [tweetID]

		return TableTools.getCount(connection, TweetsTableTools._TWEETS_TABLE,
			"replyto = :1", variables)

	@staticmethod
	def addTweet(connection, writer, date, text, tweetID, replyTo = None,
		hashtags = None):
		"""
		Add the given tweet to the 'Tweets' table

		The given hashtags should not contain the "#" at the beginning
		"""

		TableTools.insert(connection, TweetsTableTools._TWEETS_TABLE,
			[tweetID, writer, date, text, replyTo],
			[int, int, cx_Oracle.DATETIME, 80, int])

		mentionsValues = []

		for hashtag in hashtags:

			TableTools.insertItemIfNew(connection,
				TweetsTableTools._HASHTAGS_TABLE, hashtag, "term", 10)

			mentionsValues.append((tweetID, hashtag))

		TableTools.insert(connection, TweetsTableTools._MENTIONS_TABLE,
			mentionsValues, [int, 10], insertsAtOnce = 50)

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
		variables = [follower]

		select = "select {0} from {1}, {2} ".format(columns,
			TweetsTableTools._TWEETS_TABLE, TweetsTableTools._FOLLOWS_TABLE)

		where = "where flwer = :1 and writer = flwee "
		orderBy = "order by tdate desc"

		statement = select + where + orderBy

		for result in TableTools.yieldResults(connection, statement,
			variables, [int]):

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

		where = "where writer = :1 "
		orderBy = "order by tdate desc"

		statement = select + where + orderBy

		for result in TableTools.yieldResults(connection, statement, [userID],
			[int]):

			yield Tweet(result[0], userID, result[1], result[2], result[3])

class FollowsTableTools:
	"""Tools for working with the 'Follows' table"""

	_FOLLOWS_TABLE = "Follows"

	@staticmethod
	def getFollowers(connection, followee):
		"""Yield the user ID for each person following followee"""

		variables = [followee]

		statement = "select flwer from {0} where flwee = :1".format(
			FollowsTableTools._FOLLOWS_TABLE)

		for result in TableTools.yieldResults(connection, statement,
			variables, [int]):

			yield UsersTableTools.getUser(connection, result[0])

	@staticmethod
	def getFollowing(connection, follower):
		"""Yield the user ID for each person being followed by follower"""

		variables = [follower]

		statement = "select flwee from {0} where flwer = :1".format(
			FollowsTableTools._FOLLOWS_TABLE)

		for result in TableTools.yieldResults(connection, statement,
			variables, [int]):

			yield UsersTableTools.getUser(connection, result[0])

	@staticmethod
	def follow(connection, follower, followee, date):
		"""Make follower follow followee"""

		TableTools.insert(connection, FollowsTableTools._FOLLOWS_TABLE,
			[follower, followee, date], [int, int, cx_Oracle.DATETIME])

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
		variables = (userID,)
		inputSizes = [int]

		statement = "select {0} from {1} where usr = :1".format(columns,
			UsersTableTools._USERS_TABLE)

		TableTools.execute(connection, cursor, statement, variables,
			inputSizes)

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

		variables = [userID]

		return TableTools.getCount(connection, UsersTableTools._TWEETS_TABLE,
			"writer = :1", variables)

	@staticmethod
	def getFollowingCount(connection, userID):
		"""Return the number of people this user is following"""

		variables = [userID]

		return TableTools.getCount(connection, UsersTableTools._FOLLOWS_TABLE,
			"flwer = :1", variables)

	@staticmethod
	def getFollowerCount(connection, userID):
		"""Return the number of people following this user"""

		variables = [userID]

		return TableTools.getCount(connection, UsersTableTools._FOLLOWS_TABLE,
			"flwee = :1", variables)

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
		variables = [joinedKeywords]

		select = "select usr from {0} ".format(UsersTableTools._USERS_TABLE)
		where = "where regexp_like (name, :1, 'i') "
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
		variables = [joinedKeywords]

		select = "select usr from {0} ".format(UsersTableTools._USERS_TABLE)
		where1 = "where regexp_like (city, :1, 'i') and "
		where2 = "not regexp_like (name, :1, 'i') "
		orderBy = "order by length(city) asc"

		statement = select + where1 + where2 + orderBy

		for result in TableTools.yieldResults(connection, statement,
			variables):

			yield result[0]

	@staticmethod
	def addUser(connection, password, name, email, city, timezone, userID):
		"""Add a new user"""

		TableTools.insert(connection, UsersTableTools._USERS_TABLE,
			[userID, password, name, email, city, timezone],
			[int, int, 20, 15, 12, int])

	@staticmethod
	def userExists(connection, userID):
		"""Return whether the user exists"""

		return TableTools.itemExists(connection, UsersTableTools._USERS_TABLE,
			userID, "usr")

	@staticmethod
	def loginExists(connection, userID, password):
		"""Return whether the given username, password combination exists"""

		cursor = connection.cursor()

		variables = (userID, password)
		inputSizes = [int, 4]

		select = "select usr, pwd from {0} ".format(
			UsersTableTools._USERS_TABLE)

		where = "where usr = :1 and pwd = :2"

		statement = select + where

		TableTools.execute(connection, cursor, statement, variables,
			inputSizes)

		result = cursor.fetchone()

		if result is None: return False
		return True
