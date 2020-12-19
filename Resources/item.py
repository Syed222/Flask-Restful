import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from Models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This string cannot be empty')

    @jwt_required()
    def get(self, name):
        """
        Returns details about the item
        """
        item = ItemModel.find_item_name(name)
        if item:
            # Return item in json format
            return item.json()
        return {"message": "Item {} not found".format(name)}, 404

    def post(self, name):
        """
        Add new item in the database
        """
        # ***** error first approach ****
        if ItemModel.find_item_name(name):
            return {"message": "Item {} already exist".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except:
            return "An error occured", 500  # Internal server error

        return item.json(), 201

    def delete(self, name):
        """
        Deletes the Item
        """
        if ItemModel.find_item_name(name) is None:  # since not importing we can use instance(self) or class(Item)
            return "Item {} not found".format(name)

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return "Item {} deleted successfully".format(name)

    def put(self, name):
        """
        Create or Modify the existing item or new item
        """
        data = Item.parser.parse_args()

        item = ItemModel.find_item_name(name)
        updated_item = ItemModel(name, data['price'])

        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occured while inserting the item"}, 500
        else:
            try:
                updated_item.update()
            except:
                return {"message": "An error occured while updating the item"}, 500

        return updated_item.json()


class ItemList(Resource):
    """
    Class to return the details of all existing items
    """
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return {'items': items}
