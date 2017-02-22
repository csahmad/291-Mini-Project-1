class SearchTweet:
	def search(cursor, tid):
		"""Return whether the given string value exists in the given table"""
	cursor.execute(
		"select * from tweets where tid = {1}".format(tid))

	result = cursor.fetchone()
	print("--------------------------------")
	print("TWEET:")
	print(result)
	print("--------------------------------")

	if result is None: return null
	return result

# Interactive test
if __name__ == "__main__":

	from OracleTerminalConnection import OracleTerminalConnection

	# Get connection to database and cursor
	connection = OracleTerminalConnection.connect()
	cursor = connection.cursor()
	print()

	tid = input("enter tid to search: ")
	SearchTweet.search(cursor, int(tid))

	connection.close()