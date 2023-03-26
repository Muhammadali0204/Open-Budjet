import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(
        self,
        sql: str,
        parameters: tuple = None,
        fetchone=False,
        fetchall=False,
        commit=False,
    ):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
                id	INTEGER UNIQUE,
	            ovoz_berganmi	INTEGER,
	            hisob	INTEGER,
                tel	TEXT,
                karta	TEXT
            );
        """
        self.execute(sql, commit=True)

    def create_table_taklifqilganlar(self):
        sql = """
        CREATE TABLE Takliflar (
            id INTEGER UNIQUE,
            taklif_qilgan INTEGER,
            status INTEGER
        );
        """

        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{item} = ?" for item in parameters])
        return sql, tuple(parameters.values())

    def add_user(self, id, ovoz, hisob, tel, karta, karta_egasi):
        self.execute(
            sql="INSERT INTO Users(id, ovoz_berganmi, hisob, tel, karta, karta_egasi) VALUES(?, ?, ?, ?, ?, ?)",
            parameters=(id, ovoz, hisob, tel, karta, karta_egasi),
            commit=True,
        )

    def select_user_by_id(self, id):
        return self.execute(
            "SELECT * FROM Users WHERE id = ?", parameters=(id,), fetchone=True
        )

    def update_ovoz(self, ovoz, id):
        self.execute(
            "UPDATE Users SET ovoz_berganmi = ? WHERE id = ?",
            parameters=(ovoz, id),
            commit=True,
        )

    def update_hisob(self, yangi_hisob, id):
        self.execute(
            "UPDATE Users SET hisob = ? WHERE id = ?",
            parameters=(yangi_hisob, id),
            commit=True,
        )

    def update_tel(self, tel, id):
        self.execute(
            "UPDATE Users SET tel = ? WHERE id = ?", parameters=(tel, id), commit=True
        )

    def update_karta(self, karta, id):
        self.execute(
            "UPDATE Users SET karta = ? WHERE id = ?",
            parameters=(karta, id),
            commit=True,
        )
        
    def update_karta_egasi(self, karta, id):
        self.execute(
            "UPDATE Users SET karta_egasi = ? WHERE id = ?",
            parameters=(karta, id),
            commit=True,
        )

    def add_taklif(self, id, taklif_qilgan):
        self.execute(
            "INSERT INTO Takliflar(id, taklif_qilgan, status) VALUES(?, ?, ?)",
            parameters=(id, taklif_qilgan, 0),
            commit=True,
        )

    def select_takliflar(self, id):
        return self.execute(
            "SELECT * FROM Takliflar WHERE taklif_qilgan = ? AND status = 1", parameters=(id,), fetchall=True
        )
        
    def select_taklif_qilinganmi(self, id):
        return self.execute(
            "SELECT * FROM Takliflar WHERE id = ?", parameters=(id,), fetchone=True
        )
        
    def update_status(self, id):
        self.execute(
            "UPDATE Takliflar SET status = 1 WHERE id = ?",
            parameters=(id,),
            commit=True,
        )
    
        
    def select_users_count(self):
        return self.execute(
            "SELECT COUNT(id) FROM Users ", fetchone=True
        )
        
    
