from sqlalchemy import Table, Column, Integer, String, ForeignKey, TIMESTAMP

from src.tracking.entities.tracking import Tracking


# Implementación con SQL Alchemy para el repositorio de tracking.


class SQLAlchemyTrackingRepository:

    def __init__(self, sqlalchemy_client, test=False):

        # Mapear la tabla Tracking de forma imperativa.
        # Si "test" es true, se le agrega un sufijo al nombre de la tabla,
        # para que las pruebas de integración no sobreescriban los datos existentes.

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "tracking"
        table_name_parent = "shipping_order"

        if test:
            table_name += "_test"
            table_name_parent += "_test"

        self.tracking_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("shipping_order_id", Integer, ForeignKey(table_name_parent + '.id')),
            Column("date", TIMESTAMP),
            Column("status", String(50)),
            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(Tracking, self.tracking_table)

    def get_trackings(self):

        with self.session_factory() as session:
            trackings = session.query(Tracking).filter_by(deleted_at=None).all()
            return trackings

    def get_tracking(self, id):

        with self.session_factory() as session:
            tracking = session.query(Tracking).filter_by(id=id, deleted_at=None).first()
            return tracking

    def create_tracking(self, tracking):

        with self.session_factory() as session:
            session.add(tracking)
            session.commit()

            return tracking

    def update_tracking(self, id, fields):

        # Actualiza sólo los campos de la lista "fields" en el tracking especificado.
        # Luego retorna el tracking con los nuevos datos.

        with self.session_factory() as session:
            session.query(Tracking).filter_by(id=id, deleted_at=None).update(fields)
            session.commit()

            tracking = session.query(Tracking).filter_by(id=id, deleted_at=None).first()
            return tracking

    def hard_delete_tracking(self, id):

        with self.session_factory() as session:
            tracking = session.query(Tracking).get(id)
            session.delete(tracking)
            session.commit()

    def hard_delete_all_tracking(self):

        if self.test:
            with self.session_factory() as session:
                session.query(Tracking).delete()
                session.commit()

    def drop_tracking_table(self):

        if self.test:
            self.client.drop_table(self.tracking_table)
