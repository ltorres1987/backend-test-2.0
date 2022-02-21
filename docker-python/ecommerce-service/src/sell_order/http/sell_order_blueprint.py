from flask import Blueprint, request

from flask_jwt_extended import jwt_required

from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE

from src.sell_order.http.validation import sell_order_validatable_fields


# Endpoints para CRUD de sell_order.


def create_sell_order_blueprint(manage_sell_order_usecase):
    blueprint = Blueprint("sell-order", __name__)

    @blueprint.route("/marketplace/sell-order", methods=["GET"])
    def get_sell_orders():
        """Con el siguiente enpoint permite la consulta de todas ordenes de venta activas."""

        sell_orders = manage_sell_order_usecase.get_sell_orders()

        data = [sell_order_data.serialize_detail() for sell_order_data in sell_orders]
        code = SUCCESS_CODE
        message = "SellOrder obtained succesfully"
        http_code = 200

        response = {
            "code": code,
            "message": message,
            "data": data,
        }

        return response, http_code

    @blueprint.route("/sell-order/<string:sell_order_id>", methods=["GET"])
    @blueprint.route("/marketplace/sell-order/<string:sell_order_id>", methods=["GET"])
    def get_sell_order(sell_order_id):
        """Con el siguiente enpoint permite la consulta de las ordenes de venta según un ID."""

        sell_order = manage_sell_order_usecase.get_sell_order(sell_order_id)

        if sell_order:
            data = [sell_order_data.serialize_detail() for sell_order_data in sell_order]
            code = SUCCESS_CODE
            message = "SellOrder obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = f"SellOrder of ID {sell_order_id} does not exist."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.route("/seller-user/<string:seller_user>/sell-order/<string:sell_order_id>", methods=["GET"])
    def get_sell_order_by_seller_user_id(seller_user, sell_order_id):
        """Permite la consulta de todos las ordenes de venta activas de un usuario vendedor según ID"""

        sell_order = manage_sell_order_usecase.get_sell_order_by_seller_user_id(seller_user, sell_order_id)

        if sell_order:
            data = [sell_order_data.serialize_detail() for sell_order_data in sell_order]
            code = SUCCESS_CODE
            message = "SellOrder obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = f"SellOrder of seller_user: {seller_user} does not exist."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.route("/seller-user/<string:seller_user>/sell-order", methods=["GET"])
    def get_sell_order_by_seller_user(seller_user):
        """permite la consulta de todos las ordenes de venta activas de un usuario vendedor"""

        sell_order = manage_sell_order_usecase.get_sell_order_by_seller_user(seller_user)

        if sell_order:
            data = [sell_order_data.serialize_detail() for sell_order_data in sell_order]
            code = SUCCESS_CODE
            message = "SellOrder obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = f"SellOrder of seller_user: {seller_user} does not exist."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.route("/marketplace-user/sell-order", methods=["POST"])
    @validate_schema_flask(sell_order_validatable_fields.SELLORDER_CREATION_VALIDATABLE_FIELDS)
    def create_sell_order():
        """Crea una orden de venta"""

        body = request.get_json()

        try:
            sell_order = manage_sell_order_usecase.create_sell_order(body)
            data = [sell_order_data.serialize_detail() for sell_order_data in sell_order]

            code = SUCCESS_CODE
            message = "SellOrder created succesfully"
            http_code = 201

        except ValueError as e:
            data = None
            code = FAIL_CODE
            message = str(e)
            http_code = 400

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.route("/seller-user/<string:seller_user>/sell-order/<string:sell_order_id>", methods=["PUT"])
    @validate_schema_flask(sell_order_validatable_fields.SELLORDER_SELLER_USER_UPDATE_VALIDATABLE_FIELDS)
    def update_sell_order_by_seller_user(seller_user, sell_order_id):
        """Permite la actualización de estado de una orden de venta activa de un usuario vendedor según ID
        Puede cambiar de:
        "created" a "confirmed"
        "confirmed" a "dispatched"
        """

        body = request.get_json()

        try:
            sell_order = manage_sell_order_usecase.update_sell_order_by_seller_user(seller_user, sell_order_id, body)
            data = [sell_order_data.serialize_detail() for sell_order_data in sell_order]
            message = "SellOrder updated succesfully"
            code = SUCCESS_CODE
            http_code = 200

        except ValueError as e:
            data = None
            code = FAIL_CODE
            message = str(e)
            http_code = 400

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.route("/marketplace-user/sell-order/<string:sell_order_id>", methods=["PUT"])
    @blueprint.route("/marketplace/sell-order/<string:sell_order_id>", methods=["PUT"])
    def update_sell_order_cancelled(sell_order_id):
        """Con el siguiente enpoint puede "cancelar" un pedido solo si el estado es "created" o "confirmed".
        En caso de cancelación de un pedido se deberá aumentar el stock disponible de los productos.
        """

        try:
            sell_order = manage_sell_order_usecase.update_sell_order_cancelled(sell_order_id)
            data = sell_order.serialize()
            message = "SellOrder updated succesfully"
            code = SUCCESS_CODE
            http_code = 200

        except ValueError as e:
            data = None
            code = FAIL_CODE
            message = str(e)
            http_code = 400

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.route("/sell-order/<string:sell_order_id>", methods=["PUT"])
    @jwt_required()
    def update_sell_order_status_delivered(sell_order_id):
        """Endpoint consume desde delivery una vez que el crontab marca como el estado como entregado"""

        try:
            manage_sell_order_usecase.update_sell_order_status_delivered(sell_order_id)
            code = SUCCESS_CODE
            message = f"SellOrder of ID {sell_order_id} updated succesfully."
            http_code = 200

        except ValueError as e:
            code = FAIL_CODE
            message = str(e)
            http_code = 400

        response = {
            "code": code,
            "message": message,
        }

        return response, http_code

    return blueprint
