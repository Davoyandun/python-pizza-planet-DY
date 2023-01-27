from ipaddress import summarize_address_range
from typing import Any, List, Optional, Sequence

from sqlalchemy.sql import text, column, func

from .models import Ingredient, Order, OrderDetail, Size, Beverage, db
from .serializers import (IngredientSerializer, OrderSerializer,
                          SizeSerializer, BeverageSerializer, ma)


class BaseManager:
    model: Optional[db.Model] = None
    serializer: Optional[ma.SQLAlchemyAutoSchema] = None
    session = db.session

    @classmethod
    def get_all(cls):
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.all()
        result = serializer.dump(_objects)
        return result

    @classmethod
    def get_by_id(cls, _id: Any):
        entry = cls.model.query.get(_id)
        return cls.serializer().dump(entry)

    @classmethod
    def create(cls, entry: dict):
        serializer = cls.serializer()
        new_entry = serializer.load(entry)
        cls.session.add(new_entry)
        cls.session.commit()
        return serializer.dump(new_entry)

    @classmethod
    def update(cls, _id: Any, new_values: dict):
        cls.session.query(cls.model).filter_by(_id=_id).update(new_values)
        cls.session.commit()
        return cls.get_by_id(_id)


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer


class IngredientManager(BaseManager):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []


class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []


class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(cls, order_data: dict, ingredients: List[Ingredient], beverages: List[Beverage]):
        new_order = cls.model(**order_data)
        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)
        cls.session.add_all((OrderDetail(order_id=new_order._id, ingredient_id=ingredient._id, ingredient_price=ingredient.price)
                             for ingredient in ingredients))
        cls.session.add_all((OrderDetail(order_id=new_order._id, beverage_id=beverage._id, beverage_price=beverage.price)
                             for beverage in beverages))
        cls.session.commit()
        return cls.serializer().dump(new_order)

    @classmethod
    def update(cls):
        raise NotImplementedError(f'Method not suported for {cls.__name__}')


class IndexManager(BaseManager):

    @classmethod
    def test_connection(cls):
        cls.session.query(column('1')).from_statement(text('SELECT 1')).all()


class ReportManager:
    session = db.session

    @classmethod
    def get_top_ingredient(cls):
        ingredient =  (
            cls.session.query(OrderDetail, func.count(OrderDetail.ingredient_id))
            .group_by(OrderDetail.ingredient_id)
            .order_by(func.sum(OrderDetail.ingredient_id).desc())
            .limit(1)
            .all()
            or []
        )
        ingredient_dict = [{"id": i.ingredient_id, "count": c} for i, c in ingredient]
        ingredient_name = (cls.session.query(Ingredient).filter(Ingredient._id == ingredient_dict[0]["id"]).first()).name
        ingredient_dict[0]["name"] = ingredient_name
        return ingredient_dict
    
    @classmethod
    def get_top_beverage(cls):
        beverage= (
            cls.session.query(OrderDetail, func.count(OrderDetail.beverage_id))
            .group_by(OrderDetail.beverage_id)
            .order_by(func.sum(OrderDetail.beverage_id).desc())
            .limit(1)
            .all()
            or []
        )

        beverage_dict = [{"id": i.beverage_id, "count": c} for i, c in beverage]
        beverage_name = (cls.session.query(Beverage).filter(Beverage._id == beverage_dict[0]["id"]).first()).name
        beverage_dict[0]["name"] = beverage_name 
        return beverage_dict

    @classmethod
    def get_top3_clients(cls):
        clients=  (
            cls.session.query(Order, func.count(Order.client_dni))
            .group_by(Order.client_dni)
            .order_by(func.count(Order.client_dni).desc())
            .limit(3)
            .all()
            or []
        )
        clients_dict = [{"dni": i.client_dni, "count": c, "name": i.client_name} for i, c in clients]
        return clients_dict

   

    @classmethod
    def get_top_month(cls):
        return (
            cls.session.query(Order.date, func.count(Order._id))
            .group_by(Order.date)
            .order_by(func.count(Order.total_price).desc())
            .limit(1)
            .all()
        )[0].date.month

    @classmethod
    def get_report(cls):
        top_ingredient = cls.get_top_ingredient()[0]
        top_beverage = cls.get_top_beverage()[0]
        top3_clients = cls.get_top3_clients()
        top_month = cls.get_top_month()
        return {
           'top_ingredient': top_ingredient,
           'top_beverage': top_beverage,
           'top3_clients': top3_clients,
            'top_month': top_month,
        }
        
