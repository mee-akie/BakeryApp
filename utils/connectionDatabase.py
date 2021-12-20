import psycopg2

class ConnectionDatabase:

    def getConnection():
        conn = psycopg2.connect(
                host = "localhost",
                database = "padaria", 
                user = "postgre2",
                password = "123",
                port = "5432"
            )

        return conn