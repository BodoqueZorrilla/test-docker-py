from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from schemas import ItemSchema, ItemUpdateSchema
from db import db
from models import ItemModel

blp = Blueprint("Items", __name__, "Operations on items")

@blp.route("/items/<string:item_id>")
class Store(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(**item_data)
        
        db.session.add(item)
        db.session.commit()

        return item
    
    @jwt_required()
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return { "message": "Item deleted" }

@blp.route("/item")
class ItemList(MethodView):

    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    
    @jwt_required(fresh=True)#use this for changin passwoer or delete account
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        #item_id = uuid.uuid4().hex
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            print(f"Error -> {e}")
            abort(500, "An error occurred while inserting the item.")
        except NotImplementedError as e:
            print(str(e))


        return item
