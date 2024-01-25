from datetime import datetime
from pydantic import BaseModel, Field


#работа с имеющийся записью в БД
class ChangeUser(BaseModel):
    id: int
    first_name: str = Field(max_length=80)
    last_name: str = Field(max_length=80)
    user_email: str = Field(max_length=180)
    password: str = Field(max_length=280)

class ChangeOrder(BaseModel):
    id: int
    id_user: int
    id_product: int
    data_order: datetime = Field(datetime.now())
    status_order: str = Field(20)


class ChangeProduct(BaseModel):
    id: int
    name_product: str = Field(max_length=100)
    description_product: str = Field(max_length=360)
    price_product: int = Field(default=0)


#добавление в БД
class AddUser(BaseModel):
    first_name: str = Field(max_length=80)
    last_name: str = Field(max_length=80)
    user_email: str = Field(max_length=180)
    password: str = Field(max_length=280)


class AddOrder(BaseModel):
    id_user: int
    id_product: int
    data_order: datetime = Field(datetime.now())
    status_order: str = Field(20)


class AddProduct(BaseModel):
    name_product: str = Field(max_length=100)
    description_product: str = Field(max_length=360)
    price_product: int = Field(default=0)

