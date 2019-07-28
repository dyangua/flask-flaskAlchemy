import sqlite3


class ItemModel:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()
        query = 'SELECT * FROM items  WHERE name=?'
        result = cursor.execute(query, (name.upper(),))
        row = result.fetchone()
        conn.close()

        if row:
            return cls(*row)  # --> cls(row[0],row[1])

    def insert(self):
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()
        query = 'INSERT INTO items VALUES (null,?,?)'
        cursor.execute(query, (self.name.upper(), self.price))
        conn.commit()
        conn.close()

    def update(self):
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()
        query = 'UPDATE items SET price=? WHERE name=?'
        cursor.execute(query, (self.price, self.name))
        conn.commit()
        conn.close()
