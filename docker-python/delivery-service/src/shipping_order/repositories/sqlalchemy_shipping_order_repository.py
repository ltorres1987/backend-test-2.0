from sqlalchemy import Table, Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from src.shipping_order.entities.shipping_order import ShippingOrder

from src.shipping_order_detail.entities.shipping_order_detail import ShippingOrderDetail

from src.tracking.entities.tracking import Tracking


# Implementación con SQL Alchemy para el repositorio de shipping_order.


class SQLAlchemyShippingOrderRepository:

    def __init__(self, sqlalchemy_client, test=False):

        # Mapear la tabla ShippingOrder de forma imperativa.
        # Si "test" es true, se le agrega un sufijo al nombre de la tabla,
        # para que las pruebas de integración no sobreescriban los datos existentes.

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "shipping_order"

        if test:
            table_name += "_test"

        self.shipping_order_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("date", TIMESTAMP),
            Column("sell_order_id", Integer),
            Column("shipping_origin", String(200)),
            Column("shipping_destination", String(200)),
            Column("client_name", String(100)),
            Column("status", String(50)),
            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(ShippingOrder, self.shipping_order_table, properties={
            'order_detail': relationship(ShippingOrderDetail, backref='sell_order_detail', lazy='joined'),
            'order_tracking': relationship(Tracking, backref='sell_order_tracking', lazy='joined')
        })

    def get_shipping_orders(self):

        with self.session_factory() as session:
            shipping_orders = session.query(ShippingOrder).filter_by(deleted_at=None).all()
            return shipping_orders

    def get_status_change_tracking(self):

        with self.session_factory() as session:
            shipping_orders = session.query(ShippingOrder).filter(
                ShippingOrder.status.not_in(["delivered", "cancelled"]),
                ShippingOrder.deleted_at == None).all()
            return shipping_orders

    def get_shipping_order(self, id):

        with self.session_factory() as session:
            shipping_order = session.query(ShippingOrder).filter_by(id=id, deleted_at=None).first()
            return shipping_order

    def get_status_change_shipping_order(self, sell_order_id):

        with self.session_factory() as session:
            shipping_order = session.query(ShippingOrder).filter_by(sell_order_id=sell_order_id, deleted_at=None).first()
            return shipping_order

    def get_tracking(self, shipping_order_id):

        with self.session_factory() as session:
            shipping_orders = session.query(ShippingOrder).join(Tracking,
                                                                ShippingOrder.id == Tracking.shipping_order_id).filter(
                ShippingOrder.id == shipping_order_id, ShippingOrder.deleted_at == None).all()

            return shipping_orders

    def create_shipping_order(self, shipping_order, shipping_order_detail_dict, shipping_order_tracking):

        with self.session_factory() as session:
            session.add(shipping_order)

            # insert detail
            for shipping_order_detail in shipping_order_detail_dict:
                shipping_order.order_detail.append(shipping_order_detail)

            # insert tracking
            shipping_order.order_tracking.append(shipping_order_tracking)

            session.commit()

            return shipping_order

    def update_status_change_tracking(self, id, fields, tracking):

        # Actualiza sólo los campos de la lista "fields" en el shipping_order especificado.
        # Luego retorna el shipping_order con los nuevos datos.

        with self.session_factory() as session:
            session.query(ShippingOrder).filter_by(id=id, deleted_at=None).update(fields)

            session.add(tracking)

            session.commit()

            shipping_order = session.query(ShippingOrder).filter_by(id=id, deleted_at=None).first()

            return shipping_order

    def update_shipping_order(self, id, fields):

        # Actualiza sólo los campos de la lista "fields" en el shipping_order especificado.
        # Luego retorna el shipping_order con los nuevos datos.

        with self.session_factory() as session:
            session.query(ShippingOrder).filter_by(id=id, deleted_at=None).update(fields)
            session.commit()

            shipping_order = session.query(ShippingOrder).filter_by(id=id, deleted_at=None).first()
            return shipping_order

    def delete_shipping_order(self, id, fields):

        # Actualiza sólo los campos de la lista "fields" en el shipping_order especificado.
        # Luego retorna el shipping_order con los nuevos datos.

        with self.session_factory() as session:
            session.query(ShippingOrder).filter_by(id=id, deleted_at=None).update(fields)
            session.commit()

            shipping_order = session.query(ShippingOrder).filter_by(id=id, deleted_at=None).first()
            return shipping_order

    def hard_delete_shipping_order(self, id):

        with self.session_factory() as session:
            shipping_order = session.query(ShippingOrder).get(id)
            session.delete(shipping_order)
            session.commit()

    def hard_delete_all_shipping_order(self):

        if self.test:
            with self.session_factory() as session:
                session.query(ShippingOrder).delete()
                session.commit()

    def drop_shipping_order_table(self):

        if self.test:
            self.client.drop_table(self.shipping_order_table)
