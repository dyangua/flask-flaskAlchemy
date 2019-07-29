from datetime import timedelta

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

# services
from resources.item import Item
from resources.items import Items
from resources.store import Store, StoreList
from resources.user import UserRegistry
# security
from security import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
jwt = JWT(app, authenticate, identity)

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


# endpoints
api.add_resource(UserRegistry, '/user')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
