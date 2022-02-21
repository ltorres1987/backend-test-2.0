from sqlalchemy import Table, Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from src.sell_order_detail.entities.sell_order_detail import SellOrderDetail

from src.product.entities.product import Product

# Implementación con SQL Alchemy para el repositorio de sell_order_detail.


class SQLAlchemySellOrderDetailRepository:

    def __init__(self, sqlalchemy_client, test=False):

        # Mapear la tabla SellOrderDetail de forma imperativa.
        # Si "test" es true, se le agrega un sufijo al nombre de la tabla,
        # para que las pruebas de integración no sobreescriban los datos existentes.

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "sell_order_detail"
        table_name_parent = "sell_order"

        if test:
            table_name += "_test"
            table_name_parent += "_test"

        self.sell_order_detail_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("sell_order_id", Integer, ForeignKey(table_name_parent + '.id')),
            Column("sku", Integer, ForeignKey('product.id')),
            Column("quantity", Integer),
            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True)
        )

        sqlalchemy_client.mapper_registry.map_imperatively(SellOrderDetail, self.sell_order_detail_table, properties={
            'product_detail': relationship(Product, backref='product_detail', lazy='joined')
        })

    def get_sell_order_details(self):

        with self.session_factory() as session:
            sell_order_details = session.query(SellOrderDetail).filter_by(deleted_at=None).all()
            return sell_order_details

    def get_sell_order_detail(self, id):

        with self.session_factory() as session:
            sell_order_detail = session.query(SellOrderDetail).filter_by(id=id, deleted_at=None).first()
            return sell_order_detail

    def create_sell_order_detail(self, sell_order_detail):

        with self.session_factory() as session:
            session.add(sell_order_detail)
            session.commit()

            return sell_order_detail

    def update_sell_order_detail(self, id, fields):

        # Actualiza sólo los campos de la lista "fields" en el sell_order_detail especificado.
        # Luego retorna el sell_order_detail con los nuevos datos.

        with self.session_factory() as session:
            session.query(SellOrderDetail).filter_by(id=id, deleted_at=None).update(fields)
            session.commit()

            sell_order_detail = session.query(SellOrderDetail).filter_by(id=id, deleted_at=None).first()
            return sell_order_detail

    def hard_delete_sell_order_detail(self, id):

        with self.session_factory() as session:
            sell_order_detail = session.query(SellOrderDetail).get(id)
            session.delete(sell_order_detail)
            session.commit()

    def hard_delete_all_sell_order_detail(self):

        if self.test:
            with self.session_factory() as session:
                session.query(SellOrderDetail).delete()
                session.commit()

    def drop_sell_order_detail_table(self):

        if self.test:
            self.client.drop_table(self.sell_order_detail_table)
