from mongoengine import Document,ReferenceField,StringField,IntField,EmailField
class Categorias(db.Document):
   nombre = db.StringField(max_length=50, unique=True)

class Productos(db.Document):
    codigo = db.StringField(required=True)
    nombre = db.StringField(required=True)
    precio = db.IntField(required=True)
    categoria = db.ReferenceField(Categorias)
    foto = db.StringField(required=True)
