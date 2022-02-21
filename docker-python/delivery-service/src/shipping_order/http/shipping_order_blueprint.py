from flask import Blueprint, request

from flask_jwt_extended import jwt_required

from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE

from src.shipping_order.http.validation import shipping_order_validatable_fields


# Endpoints para CRUD de shipping_order.

# Sólo se encarga de recibir las llamadas HTTP y le entrega los datos
# relevantes a los casos de uso correspondientes. Esta capa no debe
# contener lógica de negocio, sólo lo necesario para recibir y entregar
# respuestas válidas al mundo exterior.

# Se realiza la validación de datos de entrada mediante el decorador 
# "@validate_schema_flask", el cual recibe como argumento un diccionario definido
# en el archivo "shipping_order_validatable_fields". No sólo valida que todos los campos
# requeridos vengan en el payload, sino que también que no vengan campos de más.


def create_shipping_order_blueprint(manage_shipping_order_usecase):
    blueprint = Blueprint("shipping_order", __name__)

    @blueprint.route("/shipping_order", methods=["GET"])
    @jwt_required()
    def get_shipping_orders():
        """Con el siguiente enpoint permite la consulta de todos los delivery activos."""

        shipping_orders = manage_shipping_order_usecase.get_shipping_orders()

        data = [shipping_order.serialize_detail() for shipping_order in shipping_orders]
        code = SUCCESS_CODE
        message = "ShippingOrder obtained succesfully"
        http_code = 200

        response = {
            "code": code,
            "message": message,
            "data": data,
        }

        return response, http_code

    @blueprint.route("/shipping_order/<string:shipping_order_id>", methods=["GET"])
    @jwt_required()
    def get_shipping_order(shipping_order_id):
        """Con el siguiente enpoint autentificado permite la consulta de un delivery según un ID."""

        shipping_order = manage_shipping_order_usecase.get_shipping_order(shipping_order_id)

        if shipping_order:
            data = shipping_order.serialize_detail()
            code = SUCCESS_CODE
            message = "ShippingOrder obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = f"ShippingOrder of ID {shipping_order_id} does not exist."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.route("/tracking", methods=["GET"])
    @validate_schema_flask(shipping_order_validatable_fields.TRACKING_UPDATE_VALIDATABLE_FIELDS)
    def get_tracking():
        """Con el siguiente enpoint permite la consulta del traking de un delivery"""

        body = request.get_json()

        shipping_order = manage_shipping_order_usecase.get_tracking(body)

        if shipping_order:
            data = [data_tracking.serialize() for data_tracking in shipping_order]
            code = SUCCESS_CODE
            message = "tracking obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = "there is no tracking."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.route("/shipping_order", methods=["POST"])
    @validate_schema_flask(shipping_order_validatable_fields.SHIPPINGORDER_CREATION_VALIDATABLE_FIELDS)
    @jwt_required()
    def create_shipping_order():
        """Con el siguiente enpoint autenticado permite la creación de un delivery y traking.
        este servicio se consume desde ecommerce cuando el estado se cambie a "dispatched
        """

        body = request.get_json()

        try:
            shipping_order = manage_shipping_order_usecase.create_shipping_order(body)
            data = shipping_order.serialize_detail()
            code = SUCCESS_CODE
            message = "ShippingOrder created succesfully"
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

    @blueprint.route("/status_change_tracking", methods=["PUT"])
    def update_status_change_tracking():
        """permite cambiar el estado de todos los pedidos
        Este endpoint será consumido por un docker crontab cada 30 segundos
        """

        try:
            manage_shipping_order_usecase.update_status_change_tracking()
            message = "Change tracking updated succesfully"
            code = SUCCESS_CODE
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

    @blueprint.route("/shipping_order/<string:shipping_order_id>", methods=["PUT"])
    @validate_schema_flask(shipping_order_validatable_fields.SHIPPINGORDER_UPDATE_VALIDATABLE_FIELDS)
    @jwt_required()
    def update_shipping_order(shipping_order_id):
        """Con el siguiente enpoint autentificado permite la actualizacion de un delivery según un ID."""

        body = request.get_json()

        try:
            shipping_order = manage_shipping_order_usecase.update_shipping_order(shipping_order_id, body)
            data = shipping_order.serialize_detail()
            message = "shipping_order updated succesfully"
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

    @blueprint.route("/status_change_shipping_order/<string:sell_order_id>", methods=["PUT"])
    @jwt_required()
    def status_change_shipping_order(sell_order_id):
        """Actualiza el status delivery desde microservicio ecommerce"""

        body = request.get_json()

        try:
            shipping_order = manage_shipping_order_usecase.status_change_shipping_order(sell_order_id, body)
            data = shipping_order.serialize_detail()
            message = "shipping_order updated succesfully"
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

    @blueprint.route("/shipping_order/<string:shipping_order_id>", methods=["DELETE"])
    @jwt_required()
    def delete_shipping_order(shipping_order_id):
        """Con el siguiente enpoint autentificado permite la eliminación de un delivery según un ID."""

        try:
            manage_shipping_order_usecase.delete_shipping_order(shipping_order_id)
            code = SUCCESS_CODE
            message = f"ShippingOrder of ID {shipping_order_id} deleted succesfully."
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
