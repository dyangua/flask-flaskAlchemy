from flask_jwt_extended import jwt_optional, get_jwt_identity
from flask_restful import Resource

from models.item import ItemModel


class Items(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        # return {'items': list(map(lambda item: item.json(), ItemModel.query.all()))}
        if user_id:
            return {'items': items}, 200

        return {
                   'items': [item['name'] for item in items],
                   'message': 'More data available if you log in'
               }, 200
