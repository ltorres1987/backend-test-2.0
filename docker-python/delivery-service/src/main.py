from src.frameworks.db.sqlalchemy import SQLAlchemyClient
from src.frameworks.http.flask import create_flask_app

from src.shipping_order.http.shipping_order_blueprint import create_shipping_order_blueprint
from src.shipping_order.repositories.sqlalchemy_shipping_order_repository import SQLAlchemyShippingOrderRepository
from src.shipping_order.usecases.manage_shipping_order_usecase import ManageShippingOrderUsecase

from src.login.http.login_blueprint import create_login_blueprint
from src.login.usecases.manage_login_usecase import ManageLoginUsecase

from src.shipping_order_detail.repositories.sqlalchemy_shipping_order_detail_repository import \
    SQLAlchemyShippingOrderDetailRepository

from src.tracking.repositories.sqlalchemy_tracking_repository import SQLAlchemyTrackingRepository

# Instanciar dependencias.

# En el caso de uso de de libros, es es posible pasarle como parámetro el repositorio
# de Firestore o el repositorio con SQL Alchemy, y en ambos casos debería funcionar,
# incluso si el cambio se hace mientras la aplicación está en ejecución.

sqlalchemy_client = SQLAlchemyClient()
sqlalchemy_shipping_order_repository = SQLAlchemyShippingOrderRepository(sqlalchemy_client)
sqlalchemy_shipping_order_detail_repository = SQLAlchemyShippingOrderDetailRepository(sqlalchemy_client)
sqlalchemy_tracking_repository = SQLAlchemyTrackingRepository(sqlalchemy_client)
sqlalchemy_client.create_tables()

manage_shipping_order_usecase = ManageShippingOrderUsecase(sqlalchemy_shipping_order_repository)

manage_login_usecase = ManageLoginUsecase()

blueprints = [
    create_shipping_order_blueprint(manage_shipping_order_usecase),
    create_login_blueprint(manage_login_usecase),
]

# Crear aplicación HTTP con dependencias inyectadas.

app = create_flask_app(blueprints)
