from sqlalchemy import Table, Column, Integer, String, ForeignKey, TIMESTAMP

from src.shipping_order_detail.entities.shipping_order_detail import ShippingOrderDetail


# Implementación con SQL Alchemy para el repositorio de shipping_order_detail.


class SQLAlchemyShippingOrderDetailRepository:

    def __init__(self, sqlalchemy_client, test=False):

        # Mapear la tabla ShippingOrderDetail de forma imperativa.
        # Si "test" es true, se le agrega un sufijo al nombre de la tabla,
        # para que las pruebas de integración no sobreescriban los datos existentes.

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "shipping_order_detail"
        table_name_parent = "shipping_order"

        if test:
            table_name += "_test"
            table_name_parent += "_test"

        self.shipping_order_detail_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("shipping_order_id", Integer, ForeignKey(table_name_parent + '.id')),
            Column("sku", Integer),
            Column("name", String(100)),
            Column("qty", Integer),
            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(ShippingOrderDetail, self.shipping_order_detail_table)

    def get_shipping_order_details(self):

        with self.session_factory() as session:
            shipping_order_details = session.query(ShippingOrderDetail).filter_by(deleted_at=None).all()
            return shipping_order_details

    def get_shipping_order_detail(self, id):

        with self.session_factory() as session:
            shipping_order_detail = session.query(ShippingOrderDetail).filter_by(id=id, deleted_at=None).first()
            return shipping_order_detail

    def create_shipping_order_detail(self, shipping_order_detail):

        with self.session_factory() as session:
            session.add(shipping_order_detail)
            session.commit()

            return shipping_order_detail

    def update_shipping_order_detail(self, id, fields):

        # Actualiza sólo los campos de la lista "fields" en el shipping_order_detail especificado.
        # Luego retorna el shipping_order_detail con los nuevos datos.

        with self.session_factory() as session:
            session.query(ShippingOrderDetail).filter_by(id=id, deleted_at=None).update(fields)
            session.commit()

            shipping_order_detail = session.query(ShippingOrderDetail).filter_by(id=id, deleted_at=None).first()
            return shipping_order_detail

    def hard_delete_shipping_order_detail(self, id):

        with self.session_factory() as session:
            shipping_order_detail = session.query(ShippingOrderDetail).get(id)
            session.delete(shipping_order_detail)
            session.commit()

    def hard_delete_all_shipping_order_detail(self):

        if self.test:
            with self.session_factory() as session:
                session.query(ShippingOrderDetail).delete()
                session.commit()

    def drop_shipping_order_detail_table(self):

        if self.test:
            self.client.drop_table(self.shipping_order_detail_table)
