from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainTagsSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagsSchema()), dump_only=True)  #relashionship bewtwwn items to create table


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagsSchema()), dump_only=True)

class TagsSchema(PlainTagsSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True) 
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True) #relashionship bewtwwn items to create table


#this is the table
class TagAndItemsSchema(Schema):
    message = fields.Str()
    tags = fields.Nested(TagsSchema) 
    items = fields.Nested(ItemSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)#because we are not going to receive value from client
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)#this is because never is going to being sent to the cient 
