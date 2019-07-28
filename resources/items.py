import sqlite3
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity


class Items(Resource):
    # @jwt_required()
    def get(self):
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()
        query = 'SELECT * FROM items'
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'id': row[0], 'name': row[1], 'price': row[2]})
        conn.close()
        return {'items': items}
