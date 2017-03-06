import cx_Oracle

class Search:
    def formatsearch (keyword):
        result = '%{0}%'.format(keyword.upper())
        return result

    def search(cursor, keyword):
        first = keyword[0].strip()
        if first=='#' :
            Search.searchmentions(cursor, keyword.strip('#'))
        else:
            Search.searchtweet(cursor, keyword)
         

    def searchmentions(cursor, keyword):
        print("to be searched %s" % keyword)
        cursor.execute("select t.text, t.tdate from mentions m, tweets t where upper(m.term)='{0}' and t.tid=m.tid".format(keyword.upper()))
        result = cursor.fetchall()
        if len(result) != 0:
            print("Hashtag Results")

        Search.printtweets(result)
        return result

    def searchtweet(cursor, keyword):
        keywords = keyword.split()
        statements = []       

        for i in keywords:
            fi = Search.formatsearch(i)
            statements.append("select text, tdate from tweets where upper(text) like '{0}'".format(fi))
        
        print("{0} {1}".format(" union ".join(statements), "order by tdate desc"))
        cursor.execute("{0} {1}".format(" union ".join(statements), "order by tdate desc"))
        result = cursor.fetchall()
        Search.printtweets(result)
        return result

    def printtweets(result):
        if len(result) == 0:
            print("------------------------------")
            print()
            print("The search returned no items")
            print()
            print("------------------------------")
        else:
            j=1
            print("------------------------------")
            for i in result:
                print()
                print("| %i | %s" %(j, i[0]))
                print(i[1])
                print()
                print("------------------------------")
                j=j+1

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
