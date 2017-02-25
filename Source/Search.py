import cx_Oracle

class Search:
    def formatsearch (keyword):
        result = '%{0}%'.format(keyword.upper())
        print(result)
        return result

    def search(cursor, keyword):
        first = keyword[0].strip()
        if first=='#' :
            Search.searchmentions(cursor, keyword.strip('#'))
        else:
            Search.searchtweet(cursor, keyword)

    def searchmentions(cursor, keyword):
        print("to be searched %s" % keyword)
        cursor.execute("select * from mentions where upper(term) = '{0}'".format(keyword))
        result = cursor.fetchall()
        print(result)
        return result

    def searchtweet(cursor, keyword):
        fkeyword = Search.formatsearch(keyword)
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
    Search.search(cursor, keyword)

    connection.close()
