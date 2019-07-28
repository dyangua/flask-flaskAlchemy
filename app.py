from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from datetime import timedelta

# services
from resources.user import UserRegistry
from resources.item import Item
from resources.items import Items

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
jwt = JWT(app, authenticate, identity)

api = Api(app)

# endpoints
api.add_resource(UserRegistry, '/user')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
