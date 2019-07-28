import sqlite3


class UserModel:
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        conn.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        conn.close()
        return user

    def insert(self):
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()
        query = "INSERT INTO users values (NULL,?,?)"
        cursor.execute(query, (self.name, self.password))
        conn.commit()
        conn.close()
