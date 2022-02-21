from src.frameworks.db.sqlalchemy import SQLAlchemyClient
from src.frameworks.http.flask import create_flask_app

from src.seller.http.seller_blueprint import create_seller_blueprint
from src.seller.repositories.sqlalchemy_seller_repository import SQLAlchemySellerRepository
from src.seller.usecases.manage_seller_usecase import ManageSellerUsecase

from src.product.http.product_blueprint import create_product_blueprint
from src.product.repositories.sqlalchemy_product_repository import SQLAlchemyProductRepository
from src.product.usecases.manage_product_usecase import ManageProductUsecase

from src.user.http.user_blueprint import create_user_blueprint
from src.user.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.user.usecases.manage_user_usecase import ManageUserUsecase

from src.sell_order.http.sell_order_blueprint import create_sell_order_blueprint
from src.sell_order.repositories.sqlalchemy_sell_order_repository import SQLAlchemySellOrderRepository
from src.sell_order.usecases.manage_sell_order_usecase import ManageSellOrderUsecase

from src.sell_order_detail.repositories.sqlalchemy_sell_order_detail_repository import \
    SQLAlchemySellOrderDetailRepository

from src.login.http.login_blueprint import create_login_blueprint
from src.login.usecases.manage_login_usecase import ManageLoginUsecase

# Instanciar dependencias.

# En el caso de uso de de libros, es es posible pasarle como parámetro el repositorio
# de Firestore o el repositorio con SQL Alchemy, y en ambos casos debería funcionar,
# incluso si el cambio se hace mientras la aplicación está en ejecución.

sqlalchemy_client = SQLAlchemyClient()
sqlalchemy_seller_repository = SQLAlchemySellerRepository(sqlalchemy_client)
sqlalchemy_product_repository = SQLAlchemyProductRepository(sqlalchemy_client)
sqlalchemy_user_repository = SQLAlchemyUserRepository(sqlalchemy_client)
sqlalchemy_sell_order_repository = SQLAlchemySellOrderRepository(sqlalchemy_client)
sqlalchemy_sell_order_detail_repository = SQLAlchemySellOrderDetailRepository(sqlalchemy_client)
sqlalchemy_client.create_tables()

manage_seller_usecase = ManageSellerUsecase(sqlalchemy_seller_repository)
manage_product_usecase = ManageProductUsecase(sqlalchemy_product_repository)
manage_user_usecase = ManageUserUsecase(sqlalchemy_user_repository)
manage_sell_order_usecase = ManageSellOrderUsecase(sqlalchemy_sell_order_repository, sqlalchemy_product_repository,
                                                   sqlalchemy_user_repository)

manage_login_usecase = ManageLoginUsecase()

blueprints = [
    create_seller_blueprint(manage_seller_usecase),
    create_product_blueprint(manage_product_usecase),
    create_user_blueprint(manage_user_usecase),
    create_sell_order_blueprint(manage_sell_order_usecase),
    create_login_blueprint(manage_login_usecase),
]

# Crear aplicación HTTP con dependencias inyectadas.

app = create_flask_app(blueprints)
