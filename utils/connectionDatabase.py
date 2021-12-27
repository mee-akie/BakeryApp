import psycopg2

class ConnectionDatabase:

    def getConnection():
        conn = psycopg2.connect(
                host = "localhost",
                database = "padaria", 
                user = "postgres2",
                password = "1",
                port = "5432"
            )

        return conn
