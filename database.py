import pymysql
import settings

class Database:
    def __init__(self) -> None:
        self.db_user = settings.Db_User
        self.db_pwd = settings.Db_pwd
        self.db_URI = settings.Server_Domain
        self.db_Name = settings.Database_Name

        self.cnx = pymysql.connect(user=self.db_user, password=self.db_pwd,
                      host=self.db_URI, database=self.db_Name)
        self.cursor = self.cnx.cursor()

    def check_if_user_exists(self, username) -> bool:
        query = f'SELECT * FROM user WHERE username = "{username}"'
        self.cursor.execute(query)

        # Ergebnisse abrufen
        if self.cursor.fetchone():
            return True
        else:
            return False

    def check_credentials(self, username, pwd) -> bool:
        query = f'SELECT * FROM user WHERE username = "{username}" and password = "{pwd}"'
        self.cursor.execute(query)
        if self.cursor.fetchone():
            return True
        else: 
            return False


    def close(self)-> bool:
        
        # Cursor und Verbindung schließen
        self.cursor.close()
        self.cnx.close()
        return True

# db = Database()
# db.check_if_user_exists()
# db.close()