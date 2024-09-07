import peewee

db = peewee.SqliteDatabase("database/database.db")


class BaseModel(peewee.Model):
    """ Базовая модель """
    class Meta:
        database = db

# Здесь описываются модели-наследники BaseModel


def create_models():
    db.create_tables(BaseModel.__subclasses__())
