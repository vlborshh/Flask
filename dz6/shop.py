import datetime
from fastapi import FastAPI, HTTPException
import dz6.database as db
from passlib.context import CryptContext
from asyncio import run
from typing import List
from dz6.tools import get_password_hash
from dz6.models import ChangeUser, ChangeOrder, ChangeProduct, AddUser, AddOrder, AddProduct
from random import randint



shop = FastAPI(title='Домашняя работа №6')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@shop.get("/users/", response_model=List[ChangeUser])
async def read_users():
    query = db.users.select()
    users = await db.database.fetch_all(query)
    if users:
        return users
    raise HTTPException(status_code=404, detail="Не найдено ни одного пользователя")

@shop.get("/users/{id_user}", response_model=ChangeUser)
async def read_users_id(id_user: int):
    query = db.users.select().where(db.users.c.id == id_user)
    user = await db.database.fetch_one(query)
    if user:
        return user
    raise HTTPException(status_code=404, detail="Не найдено ни одного пользователя")


@shop.get("/products/", response_model=List[ChangeProduct])
async def read_products():
    query = db.products.select()
    products = await db.database.fetch_all(query)
    if products:
        return products
    raise HTTPException(status_code=404, detail="Не найдено ни одного продукта")


@shop.get("/products/{id_product}", response_model=ChangeProduct)
async def read_products_id(id_product: int):
    query = db.products.select().where(db.products.c.id == id_product)
    product = await db.database.fetch_one(query)
    if product:
        return product
    raise HTTPException(status_code=404, detail="Не найдено ни одного продукта")


@shop.get("/orders/", response_model=List[ChangeOrder])
async def change_users():
    query = db.orders.select()
    orders = await db.database.fetch_all(query)
    if orders:
        return orders
    raise HTTPException(status_code=404, detail="Не найдено ни одного заказа")


@shop.get("/orders/{id_orders}", response_model=ChangeOrder)
async def read_products_id(id_orders: int):
    query = db.orders.select().where(db.orders.c.id == id_orders)
    order = await db.database.fetch_one(query)
    if order:
        return order
    raise HTTPException(status_code=404, detail="Не найдено ни одного заказа")

@shop.put("/users/{id_user}", response_model=AddUser)
async def user_update(id_user: int, new_user: AddUser):
    hashed_password = await get_password_hash(new_user.password)
    new_user = new_user.dict()
    new_user['password'] = hashed_password
    query = db.users.update().where(db.users.c.id == id_user).values(**new_user)
    await db.database.execute(query)
    return {**new_user, "id": id_user}


@shop.put("/products/{id_product}", response_model=AddProduct)
async def product_update(id_product: int, new_product: AddProduct):
    query = db.products.update().where(db.products.c.id == id_product).values(**new_product.dict())
    await db.database.execute(query)
    return {**new_product.dict(), "id": id_product}


@shop.put("/orders/{id_orders}", response_model=AddOrder)
async def order_update(id_orders: int, new_order: AddOrder):
    query = db.orders.update().where(db.orders.c.id == id_orders).values(**new_order.dict())
    await db.database.execute(query)
    return {**new_order.dict(), "id": id_orders}


@shop.delete("/users/{id_user}")
async def user_delete(id_user: int):
    query = db.users.delete().where(db.users.c.id == id_user)
    user = await db.database.execute(query)
    if user:
        return {'message': 'Пользователь удален'}
    raise HTTPException(status_code=404, detail="Не найдено пользователя")


@shop.delete("/products/{id_product}")
async def product_delete(id_product: int):
    query = db.products.delete().where(db.products.c.id == id_product)
    product = await db.database.execute(query)
    if product:
        return {'message': 'Продукт удален'}
    raise HTTPException(status_code=404, detail="Не найдено продукта")


@shop.delete("/orders/{id_orders}")
async def order_delete(id_orders: int):
    query = db.orders.delete().where(db.orders.c.id == id_orders)
    order = await db.database.execute(query)
    if order:
        return {'message': 'Заказ удален'}
    raise HTTPException(status_code=404, detail="Не найдено заказа")

@shop.post('/users/', response_model=AddUser)
async def user_add(new_user: AddUser):
    hashed_password = await get_password_hash(new_user.password)
    new_user = new_user.dict()
    query = db.users.insert().values(first_name=new_user['first_name'],
                                     last_name=new_user['last_name'],
                                     user_email=new_user['user_email'],
                                     password=hashed_password)
    await db.database.execute(query)
    return {**new_user}


@shop.post('/products/', response_model=AddProduct)
async def product_add(new_product: AddProduct):
    new_product = new_product.dict()
    query = db.products.insert().values(name_product=new_product['name_product'],
                                        description_product=new_product['description_product'],
                                        price_product=new_product['price_product'])
    await db.database.execute(query)
    return {**new_product}


@shop.post('/orders/', response_model=AddOrder)
async def order_add(new_order: AddOrder):
    new_order = new_order.dict()
    query = db.orders.insert().values(id_user=new_order['id_user'],
                                      id_product=new_order['id_product'],
                                      data_order=datetime.datetime.now(),
                                      status_order=new_order['status_order'])
    await db.database.execute(query)
    return {**new_order}


if __name__ == '__main__':
    import asyncio

    async def create_user(count: int):
        for i in range(1, count + 1):
            password = pwd_context.hash(f'password{i}')
            query = db.users.insert().values(first_name=f'Имя {i}', last_name=f'Фамилия {i}', user_email=f'mail{i}@mail.ru',
                                             password=password)
            await db.database.execute(query)
        return {'message': f'Создано {count} тестовых записей'}


    async def create_product(count: int):
        for i in range(1, count + 1):
            query = db.products.insert().values(name_product=f'Продукт {i}',
                                                description_product=f'Информация о продукте {i}',
                                                price_product=randint(1, 100000))
            await db.database.execute(query)
        return {'message': f'Создано {count} тестовых записей'}


    async def create_order(count: int):
        for i in range(1, count + 1):
            query = db.orders.insert().values(id_user=randint(1, 20),
                                              id_product=randint(1, 20),
                                              status_order=f"Статус заказа {randint(1, 13)}",
                                              data_order=datetime.datetime.now())
            await db.database.execute(query)
        return {'message': f'Создано {count} тестовых записей'}

    asyncio.run(create_user(10))
    asyncio.run(create_product(30))
    asyncio.run(create_order(15))
