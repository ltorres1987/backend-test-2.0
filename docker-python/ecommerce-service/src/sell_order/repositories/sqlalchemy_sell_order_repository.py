from sqlalchemy import Table, Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from src.sell_order.entities.sell_order import SellOrder

from src.sell_order_detail.entities.sell_order_detail import SellOrderDetail

from src.product.entities.product import Product

from src.user.entities.user import User


# Implementación con SQL Alchemy para el repositorio de sell_order.


class SQLAlchemySellOrderRepository:

    def __init__(self, sqlalchemy_client, test=False):

        # Mapear la tabla SellOrder de forma imperativa.
        # Si "test" es true, se le agrega un sufijo al nombre de la tabla,
        # para que las pruebas de integración no sobreescriban los datos existentes.

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "sell_order"

        if test:
            table_name += "_test"

        self.sell_order_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("date", TIMESTAMP),
            Column("shipping_origin", String(200)),
            Column("shipping_destination", String(200)),
            Column("seller_user", String(100)),
            Column("user_id", Integer, ForeignKey('user.id')),
            Column("status", String(50)),
            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True)
        )

        sqlalchemy_client.mapper_registry.map_imperatively(SellOrder, self.sell_order_table, properties={
            'order_detail': relationship(SellOrderDetail, backref='order_detail', lazy='joined'),
            'customer_data': relationship(User, backref='customer_data', lazy='joined')
        })

    def get_sell_orders(self):

        with self.session_factory() as session:
            sell_orders = session.query(SellOrder).join(SellOrderDetail,
                                                        SellOrder.id == SellOrderDetail.sell_order_id).filter_by(
                deleted_at=None).all()

            return sell_orders

    def get_sell_order(self, id):

        with self.session_factory() as session:
            sell_order = session.query(SellOrder).join(SellOrderDetail,
                                                       SellOrder.id == SellOrderDetail.sell_order_id).filter(
                SellOrder.id == id, SellOrder.deleted_at == None).all()
            return sell_order

    def get_sell_order_by_seller_user_id(self, seller_user, sell_order_id):

        with self.session_factory() as session:
            sell_orders = session.query(SellOrder).join(SellOrderDetail,
                                                        SellOrder.id == SellOrderDetail.sell_order_id).filter(
                SellOrder.id == sell_order_id, SellOrder.seller_user == seller_user, SellOrder.deleted_at == None).all()

            return sell_orders

    def get_sell_order_by_seller_user(self, seller_user):

        with self.session_factory() as session:
            sell_orders = session.query(SellOrder).join(SellOrderDetail,
                                                        SellOrder.id == SellOrderDetail.sell_order_id).filter(
                SellOrder.seller_user == seller_user, SellOrder.deleted_at == None).all()

            return sell_orders

    def create_sell_order(self, sell_order, sell_order_detail_dict, product_dict):

        with self.session_factory() as session:
            # insert sell_order
            session.add(sell_order)

            # insert detail
            for sell_order_detail in sell_order_detail_dict:
                sell_order.order_detail.append(sell_order_detail)

            # update stock product
            for data_product in product_dict:
                session.query(Product).filter_by(id=data_product["sku"], deleted_at=None).update(data_product["fields"])

            session.commit()

            sell_order = session.query(SellOrder).join(SellOrderDetail,
                                                       SellOrder.id == SellOrderDetail.sell_order_id).filter(
                SellOrder.id == sell_order.id, SellOrder.deleted_at == None).all()

            return sell_order

    def update_sell_order(self, id, fields):

        # Actualiza sólo los campos de la lista "fields" en el sell_order especificado.
        # Luego retorna el sell_order con los nuevos datos.

        with self.session_factory() as session:
            session.query(SellOrder).filter_by(id=id, deleted_at=None).update(fields)
            session.commit()

            # recupera informacion
            sell_order = session.query(SellOrder).join(SellOrderDetail,
                                                       SellOrder.id == SellOrderDetail.sell_order_id).filter(
                SellOrder.id == id, SellOrder.deleted_at == None).all()

            return sell_order

    def update_sell_order_cancelled(self, id, fields, product_dict):

        # Actualiza sólo los campos de la lista "fields" en el sell_order especificado.
        # Luego retorna el sell_order con los nuevos datos.

        with self.session_factory() as session:
            session.query(SellOrder).filter_by(id=id, deleted_at=None).update(fields)

            # update product
            for data_product in product_dict:
                session.query(Product).filter_by(id=data_product["sku"], deleted_at=None).update(data_product["fields"])

            session.commit()

            sell_order = session.query(SellOrder).filter_by(id=id, deleted_at=None).first()
            return sell_order

    def hard_delete_sell_order(self, id):

        with self.session_factory() as session:
            sell_order = session.query(SellOrder).get(id)
            session.delete(sell_order)
            session.commit()

    def hard_delete_all_sell_order(self):

        if self.test:
            with self.session_factory() as session:
                session.query(SellOrder).delete()
                session.commit()

    def drop_sell_order_table(self):

        if self.test:
            self.client.drop_table(self.sell_order_table)
