import sqlite3

class Database:
    def __init__(self, db_name='database.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)')
        self.conn.commit()

    def insert_user(self, user_id):
        existing_user = self.cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,)).fetchone()
        if existing_user is None:
            self.cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
            self.conn.commit()


    def __del__(self):
        self.cursor.close()
        self.conn.close()