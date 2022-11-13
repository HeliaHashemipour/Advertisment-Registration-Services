import mysql.connector

create_table_advertisement = '''CREATE TABLE advertisement (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(255),  
    email VARCHAR(255),
    state INT NOT NULL,
    category VARCHAR(255) ,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )'''


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
            "CREATE TABLE advertisement (name VARCHAR(255) primary key, address VARCHAR(255))")
        mycursor = self.mydb.cursor()
        mycursor.execute("SHOW TABLES")

        for x in mycursor:
            print(x)

    def insert_data(self, email, description):
        mycursor = self.mydb.cursor()

        sql = "INSERT INTO advertisement (email, description,state) VALUES (%s, %s,%d)"
        val = (email, description, 0)
        mycursor.execute(sql, val)

        self.mydb.commit()

        print(mycursor.rowcount, "record inserted.")
        return mycursor.lastrowid

    def select(self):
        mycursor = self.mydb.cursor()

        mycursor.execute("SELECT * FROM users")

        myresult = mycursor.fetchall()

        for x in myresult:
            print(x)

    def update(self):
        mycursor = self.mydb.cursor()

        sql = "UPDATE advertisement SET (state,category) = (%s,%s) WHERE id = %d"

        mycursor.execute(sql)

        self.mydb.commit()

        print(mycursor.rowcount, "record(s) affected")


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
