import sqlite3

connection = sqlite3.connect('ustoz_shogirt.db')

cursor = connection.cursor()

def main():
    cursor.execute(
    """CREATE TABLE IF NOT EXISTS ish_joyi_kerak(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ism VARCHAR(20),
        yosh INTEGER,
        texnologiya TEXT,
        telefon_raqam VARCHAR(60),
        hudud VARCHAR(200)
)
"""
)
connection.commit()


def create_user(*args):
    """
    args - bu funksiya qabul qilayotgan foydalanuvchi ma'lumotlar to'plami
    """
    sql = """INSERT INTO ish_joyi_kerak(ism,yosh,texnologiya,telefon_raqam,hudud)
            VALUES(?,?,?,?,?)"""
    cursor.execute(sql,args)
    connection.commit()
    
def info_users():
    return cursor.execute("SELECT ism, telefon_raqam FROM ish_joyi_kerak").fetchall()
    

if __name__ == "__main__":
    main()