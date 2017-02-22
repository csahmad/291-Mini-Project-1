import cx_Oracle

class SearchTweet:
    def formatsearch (keyword):
        result = '%{0}%'.format(keyword.upper())
        print(result)
        return result

    def search(cursor, keyword):
        """Return whether the given string value exists in the given table"""
        fkeyword = SearchTweet.formatsearch(keyword)
        cursor.execute("select tid, text from tweets where upper(text) like '{0}'".format(fkeyword))
        result = cursor.fetchall()
        print("--------------------------------")
        for i in result:
            print()
            print("tweet id: %i" % i[0])
            print()
            print("tweet:")
            print(i[1])
            print()
            print("--------------------------------")
        return result

# Interactive test
if __name__ == "__main__":
    from OracleTerminalConnection import OracleTerminalConnection
    
# Get connection to database and cursor
    
    f = open('.info')
    username = f.readline().strip()
    password = f.readline().strip()
    connection = cx_Oracle.connect(username, password, "gwynne.cs.ualberta.ca:1521/CRS")
    cursor = connection.cursor()
    print()
    keyword = input("enter keyword to search: ")
    SearchTweet.search(cursor, keyword)

    connection.close()
