import mysql.connector

'''
    This class is used to connect to the database and execute queries
    id is the id of the user
    description is the description of the user
    email is the email of the user
    state is the state of the user
    category is the category of the user
'''

create_table_advertisement = '''CREATE TABLE advertisement (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(255),  
    email VARCHAR(30),
    state INT NOT NULL,
    category VARCHAR(255) ,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )'''


# DATABASE = "defaultdb"
# HOST = "mysql-285d668a-heliahashemipour2-3713.aivencloud.com"
# PORT = 24306
# USER = "avnadmin"
# PASSWORD = 'AVNS_Dw1z9L45JL5OCEl7X1G'

class Database_class:
    def __init__(self):
        # self.database =  "defaultdb"
        # self.host = "mysql-285d668a-heliahashemipour2-3713.aivencloud.com"
        # self.port = 24306
        # self.user = "avnadmin"
        # self.password = 'AVNS_Dw1z9L45JL5OCEl7X1G'

        self.mydb = mysql.connector.connect(
            database="defaultdb",
            host="mysql-285d668a-heliahashemipour2-3713.aivencloud.com",
            port=24306,
            user="avnadmin",
            password='AVNS_Dw1z9L45JL5OCEl7X1G'
        )

        # print(mydb)

    def create_table(self):
        mycursor = self.mydb.cursor()
        mycursor.execute(
            "CREATE TABLE advertisement (name VARCHAR(255) primary key, address VARCHAR(255))")
        mycursor.commit()
        # mycursor.execute("SHOW TABLES")

        # for x in mycursor:
        #     print(x)

    def insert_data(self, email, description,extension):
        mycursor = self.mydb.cursor()

        sql = "INSERT INTO advertisement (email, description,state,extension) VALUES (%s, %s, 0, %s)"
        val = (email, description, extension)
        mycursor.execute(sql, val)

        self.mydb.commit()

        print(mycursor.rowcount, "record inserted.")
        return mycursor.lastrowid

    def select(self):
        mycursor = self.mydb.cursor()

        mycursor.execute("SELECT * FROM advertisement")

        myresult = mycursor.fetchall()

    def update(self,id,state,category='None'):
        mycursor = self.mydb.cursor()
        mycursor.execute("UPDATE advertisement SET  state = %s, category = %s WHERE id = %s", (state,category,id))
        self.mydb.commit()
        print(mycursor.rowcount, "record(s) affected")

    def delete(self, name):
        mycursor = self.mydb.cursor()

        sql = f'DROP TABLE {name}'
        mycursor.execute(sql)
        self.mydb.commit()

    def select_all(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("SHOW TABLES")
        # self.mydb.commit()
        for x in mycursor:
            print(x)

    def select_table(self, table_name):
        mycursor = self.mydb.cursor()

        sql = f"SELECT * FROM {table_name}"
        mycursor.execute(sql)
        self.mydb.commit()
        return mycursor.fetchall()
    
    def select_row_by_id(self, table_name, id):
        mycursor = self.mydb.cursor()

        sql = f"SELECT * FROM advertisement WHERE id = {id}"
        mycursor.execute(sql)
        self.mydb.commit()
        myresult=mycursor.fetchall()
        
        for x in myresult:
            print(x)
        return mycursor.fetchall()




# db = Database_class(database=DATABASE,
#                     host=HOST,
#                     port=PORT,
#                     user=USER,
#                     password=PASSWORD)

# db.select_all()

# db = Database_class()
