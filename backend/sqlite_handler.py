import sqlite3
import threading

class sql:
    def __init__(self):
        # Create a thread-local storage for the connection
        self.local = threading.local()

    def get_connection(self):
        if not hasattr(self.local, 'conn'):
            self.local.conn = sqlite3.connect('database.db')
            self.local.cursor = self.local.conn.cursor()
        return self.local.conn, self.local.cursor

    def create_table(self):
        conn, cursor = self.get_connection()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')
        conn.commit()

    def create_user(self, username, password):
        conn, cursor = self.get_connection()
        cursor.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, password))
        conn.commit()

    def get_user(self, username):
        conn, cursor = self.get_connection()
        cursor.execute('''SELECT * FROM users WHERE username = ?''', (username,))
        return cursor.fetchone()
    
    def find_user(self, username):
        return self.get_user(username)  # Reuse get_user implementation
    
    def close(self):
        if hasattr(self.local, 'conn'):
            self.local.conn.close()
            del self.local.conn
            del self.local.cursor