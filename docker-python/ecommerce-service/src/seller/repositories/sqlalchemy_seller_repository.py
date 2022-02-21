from sqlalchemy import Table, Column, Integer, String, ForeignKey, TIMESTAMP

from src.seller.entities.seller import Seller
    
# Implementación con SQL Alchemy para el repositorio de seller.


class SQLAlchemySellerRepository:

    def __init__(self, sqlalchemy_client, test=False):

        # Mapear la tabla Seller de forma imperativa.
        # Si "test" es true, se le agrega un sufijo al nombre de la tabla,
        # para que las pruebas de integración no sobreescriban los datos existentes.

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "seller"

        if test:
            table_name += "_test"

        self.seller_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("short_description", String(100)),
            Column("seller_user", String(100)),
            Column("address", String(200)),
            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(Seller, self.seller_table)

    def get_sellers(self):
        
        with self.session_factory() as session:
            
            sellers = session.query(Seller).filter_by(deleted_at=None).all()
            return sellers

    def get_seller(self, id):
        
        with self.session_factory() as session:
            seller = session.query(Seller).filter_by(id=id, deleted_at=None).first()
            return seller

    def create_seller(self, seller):

        with self.session_factory() as session:

            session.add(seller)
            session.commit()

            return seller

    def update_seller(self, id, fields):

        # Actualiza sólo los campos de la lista "fields" en el seller especificado.
        # Luego retorna el seller con los nuevos datos.
        
        with self.session_factory() as session:

            session.query(Seller).filter_by(id=id, deleted_at=None).update(fields)
            session.commit()
            
            seller = session.query(Seller).filter_by(id=id, deleted_at=None).first()
            return seller

    def hard_delete_seller(self, id):

        with self.session_factory() as session:

            seller = session.query(Seller).get(id)
            session.delete(seller)
            session.commit()

    def hard_delete_all_seller(self):

        if self.test:

            with self.session_factory() as session:
                
                session.query(Seller).delete()
                session.commit()

    def drop_seller_table(self):

        if self.test:
            self.client.drop_table(self.seller_table)
