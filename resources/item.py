import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help=' This field cannot be blank')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name.upper())
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name.upper()):
            return {'message': "An item with name '{}' already exists".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel('', name, data['price'])
        try:
            item.insert()
        except:
            return {'message', 'An error occurred inserting the item.'}, 500
        return item.json(), 201

    def delete(self, name):
        if ItemModel.find_by_name(name.upper()):
            conn = sqlite3.connect('store.db')
            cursor = conn.cursor()
            query = 'DELETE FROM items WHERE name=?'
            cursor.execute(query, (name.upper(),))
            conn.commit()
            conn.close()
            return {'message': "Item delete '{}'".format(name)}, 201
        return {'message': "An item with name '{}' doesnt exists".format(name)}, 400

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        update_item = ItemModel('',name.upper(), data['price'])
        if item is None:
            update_item.insert()
        else:
            update_item.update()
        return update_item.json()
