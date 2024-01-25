import sqlalchemy
import databases
from sqlalchemy.pool import StaticPool
# from models import UserModel

DATABASE_URL = "sqlite:///FastAPI_dz6.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('first_name', sqlalchemy.String(80), nullable=False),
    sqlalchemy.Column('last_name', sqlalchemy.String(80), nullable=False),
    sqlalchemy.Column('user_email', sqlalchemy.String(180), nullable=False),
    sqlalchemy.Column('password', sqlalchemy.String(280), nullable=False),
)


products = sqlalchemy.Table(
    'products',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name_product', sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column('description_product', sqlalchemy.String(360), nullable=False),
    sqlalchemy.Column('price_product', sqlalchemy.Integer, nullable=False),
)


orders = sqlalchemy.Table(
    'orders',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('id_user', sqlalchemy.ForeignKey('users.id'), nullable=False),
    sqlalchemy.Column('id_product', sqlalchemy.ForeignKey('products.id'), nullable=False),
    sqlalchemy.Column('data_order', sqlalchemy.Date, nullable=False),
    sqlalchemy.Column('status_order', sqlalchemy.String(20), nullable=False),
)





engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)