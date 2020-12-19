from flask import Flask
from flask_restful import Api
from security import authenticate, security
from flask_jwt import JWT
from Resources.user import UserRegister
from Resources.item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, security)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=4999, debug=True)
