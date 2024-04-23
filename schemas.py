from pydantic import BaseModel


class PizzaSchema(BaseModel):
    name: str
    description: str
    price: int

    class Config:
        from_attributes = True


class PizzaAll(BaseModel):
    id: int
    name: str
    description: str
    price: int

    class Config:
        from_attributes = True


class PizzaSchemaWithID(BaseModel):
    id: int
    name: str
    description: str
    price: int

    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True
