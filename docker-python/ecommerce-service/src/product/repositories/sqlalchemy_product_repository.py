from sqlalchemy import Table, Column, Integer, String, ForeignKey, TIMESTAMP

from src.product.entities.product import Product
    
# Implementación con SQL Alchemy para el repositorio de product.


class SQLAlchemyProductRepository:

    def __init__(self, sqlalchemy_client, test=False):

        # Mapear la tabla product de forma imperativa.
        # Si "test" es true, se le agrega un sufijo al nombre de la tabla,
        # para que las pruebas de integración no sobreescriban los datos existentes.

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "product"

        if test:
            table_name += "_test"

        self.product_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("short_description", String(100)),
            Column("quantity", Integer),
            Column("seller_id", Integer),
            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(Product, self.product_table)

    def get_products(self):
        
        with self.session_factory() as session:
            
            products = session.query(Product).filter_by(deleted_at=None).all()
            return products

    def get_product(self, id):
        
        with self.session_factory() as session:

            product = session.query(Product).filter_by(id=id, deleted_at=None).first()
            return product

    def create_product(self, product):

        with self.session_factory() as session:

            session.add(product)
            session.commit()

            return product

    def update_product(self, id, fields):

        # Actualiza sólo los campos de la lista "fields" en el product especificado.
        # Luego retorna el product con los nuevos datos.
        
        with self.session_factory() as session:
            session.query(Product).filter_by(id=id, deleted_at=None).update(fields)
            session.commit()
            
            product = session.query(Product).filter_by(id=id, deleted_at=None).first()
            return product

    def hard_delete_product(self, id):

        with self.session_factory() as session:

            product = session.query(Product).get(id)
            session.delete(product)
            session.commit()

    def hard_delete_all_product(self):

        if self.test:

            with self.session_factory() as session:
                
                session.query(Product).delete()
                session.commit()

    def drop_product_table(self):

        if self.test:
            self.client.drop_table(self.product_table)
