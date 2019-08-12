from flask_jwt_extended import jwt_required, get_jwt_claims, fresh_jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be blank')
    parser.add_argument('store_id', type=int, required=True, help='Every item need store id')

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name.upper())
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required
    def post(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin priviledge required'}, 401
        _nameU = name.upper()
        if ItemModel.find_by_name(_nameU):
            return {'message': "An item with name '{}' already exists".format(_nameU)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(None, _nameU, data['price'], data['store_id'])
        try:
            item.insert()
        except:
            return {'message', 'An error occurred inserting the item.'}, 500
        return item.json(), 201

    @fresh_jwt_required
    def delete(self, name):
        _nameU = name.upper()
        item = ItemModel.find_by_name(name.upper())
        if item:
            item.delete()
            return {'message': "Item delete '{}'".format(_nameU)}, 201
        return {'message': "An item with name '{}' doesnt exists".format(_nameU)}, 400

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name.upper())

        if item is None:
            item = ItemModel(None, name.upper(), **data)  # -> **data =  data['price'], data['store_id']
        else:
            item.price = data['price']
        item.insert()
        return item.json()
