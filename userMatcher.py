import spreadsheet
users = {}
##spreadsheet.setSpreadsheet('1ThDLDzJH7lzZcw1Q9cLNnUJhE6bLBshyULiaWCOmevw')
##users['Other homeless people'] = spreadsheet.getRowList(2, 'N')
##spreadsheet.setSpreadsheet('1eVQhOozH0YUJ_V9Jxay8ictAtqZkhjUgQ3nAYCdSQVM')
##users['Volunteers'] = spreadsheet.getRowList(2, 'U')
##spreadsheet.setSpreadsheet('1dMYV3DBb9uS4wEweWOAyGiAdOY9FfPrAfvRqf_KW6B4')
##users['Organizations'] = spreadsheet.getRowList(2, 'K')
def getMatchCount(user1, user2):
    count = 0
    for i in range(min(len(user1),len(user2))):
        if user1[i] == user2[i]:
            count += 1
    return count
def getUser(string):
    for userType in users:
        for user in users[userType]:
            if user[1] == string or user[3] == string:
                return user
    return None
def getSimilarList(user):
    if type(user) == str:
        return getSimilarList(getUser(user))
    if user[4] in users:
        L = users[user[4]]
    else:
        L = users['Volunteers']
    pairs = []
    for x in L:
        if x == user:
            continue
        pairs.append((getMatchCount(user,x),x))
    pairs = sorted(pairs, reverse=1)
    return pairs
def printSimilarities(user):
    k = 1
    print('Other users in order of decreasing similarity:')
    for n, x in getSimilarList(user):
        print('#%s: %s (%s) - similarity=%s' % (k, x[1], x[3], n))
        k += 1
