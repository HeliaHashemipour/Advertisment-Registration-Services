import mysql.connector

'''
    This class is used to connect to the database and execute queries
    id is the id of the user
    description is the description of the user
    email is the email of the user
    state is the  state of the user
    category is the category of the user
    image_type is the image type of the user
'''


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
            host=,
            port=,
            user="avnadmin",
            password=
        )

        # print(mydb)

    def create_table(self):
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute(
            '''CREATE TABLE advertisement (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            description VARCHAR(255),  
                            email VARCHAR(30) NOT NULL,
                            state INT NOT NULL,
                            category VARCHAR(255) ,
                            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                            )''')

        self.mydb.commit()
        # mycursor.execute("SHOW TABLES")

        # for x in mycursor:
        #     print(x)

    def insert(self, email, description, image_type):
        mycursor = self.mydb.cursor(buffered=True)
        val = (description,email, image_type)
        mycursor.execute("INSERT INTO advertisement (description, email, image_type, state) VALUES (%s, %s, %s, 2)", val)

        self.mydb.commit()

        print(mycursor.rowcount, "record inserted.")
        return mycursor.lastrowid

    # def select(self):
        # mycursor = self.mydb.cursor()

        # mycursor.execute("SELECT * FROM advertisement")

        # myresult = mycursor.fetchall()

    def update(self,id,state,category=''):
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute(f"UPDATE advertisement SET  state = {state}, category = '{category}' WHERE id = {id}")
        self.mydb.commit()
        print(mycursor.rowcount, "record(s) affected")

    def delete(self, name):
        mycursor = self.mydb.cursor(buffered=True)

        sql = f'DROP TABLE {name}'
        mycursor.execute(sql)
        self.mydb.commit()

    def select_all(self):
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute("SHOW TABLES")
        # self.mydb.commit()
        for x in mycursor:
            print(x)

    def select_table(self, table_name):
        mycursor = self.mydb.cursor(buffered=True)

        mycursor.execute(f"SELECT * FROM {table_name}")
        self.mydb.commit()
        return mycursor.fetchall()
    
    def select_row_by_id(self, id):
        mycursor = self.mydb.cursor(buffered=True)

        # sql = f"SELECT * FROM advertisement WHERE id = {id}"
        mycursor.execute(f"SELECT * FROM advertisement WHERE id = {id}")
        self.mydb.commit()
        myresult=mycursor.fetchall()
        
        for x in myresult:
            print(x)
            
        return myresult
    
    def recieve_email(self,id):
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute(f"SELECT email FROM advertisement WHERE id = {id}")
        myresult = mycursor.fetchall()
        # for x in myresult:
        #     print(x)
        return myresult[0][0]

    def get_column_names(self):
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute("SELECT * FROM advertisement")
        return [i[0] for i in mycursor.description]
        
    def alter_image_type(self):
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute(f"ALTER TABLE advertisement ADD image_type varchar(10)")
        self.mydb.commit()
        
    def show_tables(self):
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute("SHOW TABLES")
        self.mydb.commit()
        return mycursor.fetchall()
    def get_row(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM advertisement")
        self.mydb.commit()
        return mycursor.fetchall()
    
    def Number_of_rows(self):
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute("SELECT COUNT(*) FROM advertisement")
        self.mydb.commit()
        return mycursor.fetchall()
    
    def delete_row(self,id):
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute(f"DELETE FROM advertisement WHERE id = {id}")
        self.mydb.commit()
        print(mycursor.rowcount, "record(s) deleted")




#checked 

# db = Database_class(database=DATABASE,
#                     host=HOST,
#                     port=PORT,
#                     user=USER,
#                     password=PASSWORD)

# db.select_all()

# db = Database_class()
# (Database_class().select_row_by_id(55))

# create_table_advertisement = '''CREATE TABLE advertisement (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     description VARCHAR(255),  
#     email VARCHAR(30),
#     state INT NOT NULL,
#     category VARCHAR(255) ,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP
#     )'''