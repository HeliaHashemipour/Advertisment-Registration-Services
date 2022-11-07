import mysql.connector


class database_class(): 
    def __init__(self, database, host, port, user, password):
        self.database = database
        self.host = host
        self.port = port
        self.user = user
        self.password = password

        self.mydb = mysql.connector.connect(
            database=database,
            host=host,
            port=port,
            user=user,
            password=password
        )

        # print(mydb)  

    def create_table(self):
        mycursor = self.mydb.cursor()
        mycursor.execute(
            "CREATE TABLE users (name VARCHAR(255) primary key, address VARCHAR(255))")
        mycursor = self.mydb.cursor()
        mycursor.execute("SHOW TABLES")

        for x in mycursor:
            print(x)

    def insert_data(self):
        mycursor = self.mydb.cursor()

        sql = "INSERT INTO users (name, address) VALUES (%s, %s)"
        val = ("John", "Highway 21")
        mycursor.execute(sql, val)

        self.mydb.commit()

        print(mycursor.rowcount, "record inserted.")

    def select(self):
        mycursor = self.mydb.cursor()

        mycursor.execute("SELECT * FROM users")

        myresult = mycursor.fetchall()

        for x in myresult:
            print(x)


DATABASE = "defaultdb"
HOST = "mysql-340ac0bb-heliahashemipour2-3713.aivencloud.com"
PORT = 24306
USER = 'avnadmin'
PASSWORD = 'AVNS_Q8MOa6EQpHFQknCd9JR'

db = database_class(database=DATABASE,
                    host=HOST,
                    port=PORT,
                    user=USER,
                    password=PASSWORD)
