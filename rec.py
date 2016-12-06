#!flask/bin/python
import json
from flask import jsonify
import MySQLdb as MySQL



# def rank_genre(userid,movielist):

#      SELECT
#     #transform Genretype to Genreid and insert the clicktimes into it
#     query = "INSERT INTO UserGenre(UserID,GenreID,Clicktimes) SELECT %d AS UserID, GenreID, %d AS Clicktimes FROM Genre WHERE GenreType = %s" % userid, d[key], key
#     try:
#         x = cursor.execute(query)
#         conn.commit()
#     except MySQL.Error as e:
#         conn.rollback()
#         raise
#         return False, None, "SQL connection error"


#//////////it is used to select out the recommented movies base on the user genre, prefer runtime, prefer production year
def tryrec(userid):
    state1 = "SELECT Runtime, Year FROM USER WHERE USERID = %d" % userid
    state2 = "SELECT GenreID FROM UserGenre WHERE USERID = %d LIMIT 5" % userid
    genids = []
    movies = []
    movieids = []
    try:
        conn = MySQL.connect(host="127.0.0.1", user="root", passwd="cs411fa2016", db="imdb")
        cursor = conn.cursor()
    except MySQL.Error as e:
        print "SQL Connection Error"
        conn.rollback()
        return -1
    try:
        #fetch the user prefer runtime and year
        x = cursor.execute(state1)
        if x == 0:
            return None

        result = cursor.fetchone()
        Runtime = result[0]
        Year = result[1]

        #fecth user prefer top 5 genreid
        x = cursor.execute(state2)
        if x == 0:
            return None

        results = cursor.fetchall()
        for result in results:
            genid = result[0]
            genids.append(genid)
        for genid in genids:
            #recomment 3 movies for each user prefer genre with his or her prefer runtime and year
            if(Runtime == 1):
                if(Year == 1):
                    state3 = "SELECT Name, MovieID,Rating FROM Movie1 m WHERE (m.Runtime <= 60 )AND (2010 < m.Year <=2016) AND m.MovieID IN (SELECT MovieID FROM MovieGenre1 WHERE GenreID = %d) AND (m.MovieID not IN(SELECT MovieID FROM UserSeen WHERE UserID = %d))ORDER BY Rating DESC LIMIT 3" % (genid,userid )
                elif(Year == 2):
                    state3 = "SELECT Name,MovieID,Rating FROM Movie1 m WHERE (m.Runtime <= 60 )AND (2000 < m.Year <=2010) AND m.MovieID IN (SELECT MovieID FROM MovieGenre1 WHERE GenreID = %d) AND (m.MovieID not IN(SELECT MovieID FROM UserSeen WHERE UserID = %d)) ORDER BY Rating DESC LIMIT 3" % (genid, userid)
                elif(Year ==3):
                    state3 = "SELECT Name,MovieID,Rating FROM Movie1 m WHERE (m.Runtime <= 60 )AND ( 2000 <= m.Year ) AND m.MovieID IN (SELECT MovieID FROM MovieGenre1 WHERE GenreID = %d) AND (m.MovieID not IN(SELECT MovieID FROM UserSeen WHERE UserID = %d))ORDER BY Rating DESC LIMIT 3" % (genid, userid)
                elif(Year == 0):
                    state3 = "SELECT Name,MovieID,Rating FROM Movie1 m WHERE (m.Runtime <= 60 ) AND m.MovieID IN (SELECT MovieID FROM MovieGenre1 WHERE GenreID = %d) AND (m.MovieID not IN(SELECT MovieID FROM UserSeen WHERE UserID = %d))ORDER BY Rating DESC LIMIT 3" % (genid,userid)
            elif(Runtime ==2):
                if(Year == 1):
                    state3 = "SELECT Name,MovieID,Rating FROM Movie1 m WHERE (60 < m.Runtime <=90 )AND (2010 < m.Year <=2016) AND m.MovieID IN (SELECT MovieID FROM MovieGenre1 WHERE GenreID = %d)AND (m.MovieID not IN(SELECT MovieID FROM UserSeen WHERE UserID = %d)) ORDER BY Rating DESC LIMIT 3" %( genid,userid )
                elif(Year == 2):
                    state3 = "SELECT Name,MovieID,Rating FROM Movie1 m WHERE (60 < m.Runtime <=90 )AND (2000 < m.Year <=2010) AND m.MovieID IN (SELECT MovieID FROM MovieGenre1 WHERE GenreID = %d)AND (m.MovieID not IN(SELECT MovieID FROM UserSeen WHERE UserID = %d)) ORDER BY Rating DESC LIMIT 3" % (genid,userid)
                elif(Year ==3):
                    state3 = "SELECT Name,MovieID,Rating FROM Movie1 m WHERE (60 < m.Runtime <=90 )AND ( 2000 <= m.Year ) AND m.MovieID IN (SELECT MovieID FROM MovieGenre1 WHERE GenreID = %d)AND (m.MovieID not IN(SELECT MovieID FROM UserSeen WHERE UserID = %d)) ORDER BY Rating DESC LIMIT 3" % (genid,userid)
                elif(Year ==0):
                    state3 = "SELECT Name,MovieID,Rating FROM Movie1 m WHERE (60 < m.Runtime <=90 )AND m.MovieID IN (SELECT MovieID FROM MovieGenre1 WHERE GenreID = %d)AND (m.MovieID not IN(SELECT MovieID FROM UserSeen WHERE UserID = %d))AND (m.MovieID not IN(SELECT MovieID FROM UserSeen WHERE UserID = %d)) ORDER BY Rating DESC LIMIT 3" % (genid,userid)
            elif(Runtime ==3):
                if(Year == 1):
                    state3 = "SELECT Name,MovieID,Rating FROM Movie1 m WHERE (90< m.Runtime )AND (2010 < m.Year <=2016) AND m.MovieID IN (SELECT MovieID FROM MovieGenre1 WHERE GenreID = %d)AND (m.MovieID not IN(SELECT MovieID FROM UserSeen WHERE UserID = %d))AND (m.MovieID not IN(SELECT MovieID FROM UserSeen WHERE UserID = %d)) ORDER BY Rating DESC LIMIT 3" % (genid,userid)
                elif(Year == 2):
                    state3 = "SELECT Name,MovieID,Rating FROM Movie1 m WHERE (90< m.Runtime )AND (2000 < m.Year <=2010) AND m.MovieID IN (SELECT MovieID FROM MovieGenre1 WHERE GenreID = %d)AND (m.MovieID not IN(SELECT MovieID FROM UserSeen WHERE UserID = %d))AND (m.MovieID not IN(SELECT MovieID FROM UserSeen WHERE UserID = %d)) ORDER BY Rating DESC LIMIT 3" % (genid,userid)
                elif(Year ==3):
                    state3 = "SELECT Name,MovieID,Rating FROM Movie1 m WHERE (90 < m.Runtime )AND ( 2000 <= m.Year ) AND m.MovieID IN (SELECT MovieID FROM MovieGenre1 WHERE GenreID = %d)AND (m.MovieID not IN(SELECT MovieID FROM UserSeen WHERE UserID = %d))AND (m.MovieID not IN(SELECT MovieID FROM UserSeen WHERE UserID = %d)) ORDER BY Rating DESC LIMIT 3" % (genid,userid)
                elif(Year ==0):
                    state3 = "SELECT Name,MovieID,Rating FROM Movie1 m WHERE (90 < m.Runtime )AND m.MovieID IN (SELECT MovieID FROM MovieGenre1 WHERE GenreID = %d) AND (m.MovieID not IN(SELECT MovieID FROM UserSeen WHERE UserID = %d))ORDER BY Rating DESC LIMIT 3" % (genid,userid)
            elif(Runtime ==0):
                if(Year == 1):
                    state3 = "SELECT Name,MovieID,Rating FROM Movie1 m WHERE (2010 < m.Year <=2016) AND m.MovieID IN (SELECT MovieID FROM MovieGenre1 WHERE GenreID = %d) AND (m.MovieID not IN(SELECT MovieID FROM UserSeen WHERE UserID = %d)) ORDER BY Rating DESC LIMIT 3" % (genid,userid)
                elif(Year == 2):
                    state3 = "SELECT Name,MovieID,Rating FROM Movie1 m WHERE (2000 < m.Year <=2010) AND m.MovieID IN (SELECT MovieID FROM MovieGenre1 WHERE GenreID = %d) AND (m.MovieID not IN(SELECT MovieID FROM UserSeen WHERE UserID = %d)) ORDER BY Rating DESC LIMIT 3" % (genid,userid)
                elif(Year ==3):
                    state3 = "SELECT Name,MovieID,Rating FROM Movie1 m WHERE ( 2000 <= m.Year ) AND m.MovieID IN (SELECT MovieID FROM MovieGenre1 WHERE GenreID = %d) AND (m.MovieID not IN(SELECT MovieID FROM UserSeen WHERE UserID = %d)) ORDER BY Rating DESC LIMIT 3" %(genid,userid)
                elif(Year ==0):
                    state3 = "SELECT Name,MovieID,Rating FROM Movie1 m WHERE m.MovieID IN (SELECT MovieID FROM MovieGenre1 WHERE GenreID = %d) AND (m.MovieID not IN(SELECT MovieID FROM UserSeen WHERE UserID = %d)) ORDER BY Rating DESC LIMIT 3" %(genid,userid)

            x = cursor.execute(state3)
            #if x == 0:
            #    return None

            results = cursor.fetchall()
            for result in results:
                n = result[0]
                i = result[1]
                movies.append(n)
                movieids.append(i)
                #movie = {"MovieID": i,"Name": n}
                #movies.append(movie)
            #movies = json.dumps(movies, ensure_ascii = False)

        #ADD THE MOVIE WE HAVE DISPLAY IN THE USERSEEN TABLE, SO THAT WE WONT DISPLAY THE MOVIES TO THE USER AGAIN
        for movieid in movieids:

            state4 = "INSERT INTO UserSeen(UserID,MovieID) VALUES('%d','%d')" % (userid, movieid)
            cursor.execute(state4)

        conn.commit()
        #maybe make it a jsonnify ~~thankyou
        return movies,movieids



    except MySQL.Error as e:
        conn.rollback()
        raise
        return False, None, "SQL connection error"
