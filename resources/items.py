from flask_restful import Resource

from models.item import ItemModel


class Items(Resource):
    def get(self):
        return {'items': list(map(lambda item: item.json(), ItemModel.query.all()))}
