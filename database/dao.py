from database.DB_connect import DBConnect
from model.squadre import Squadre

class DAO:
    @staticmethod
    def get_anni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT(t.year )
                    FROM team t 
                    WHERE t.year >=1980 """

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_squadre(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT t.id ,t.name,t.team_code , SUM(s.salary ) AS salaryTot
                    FROM team t , salary s 
                    WHERE  t.id=s.team_id  
                    AND t.year =%s
                    GROUP BY(t.id )  
                    ORDER BY salaryTot DESC"""

        cursor.execute(query,(anno,))

        for row in cursor:
            result.append(Squadre(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_squadre_diz(anno):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT t.id ,t.name,t.team_code , SUM(s.salary ) AS salaryTot
                    FROM team t , salary s 
                    WHERE  t.id=s.team_id  
                    AND t.year =%s
                    GROUP BY(t.id ) 
                    ORDER BY salaryTot DESC """

        cursor.execute(query,(anno,))

        for row in cursor:
            result[row["id"]]=Squadre(**row)
        cursor.close()
        conn.close()
        return result