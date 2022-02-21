from flask import Blueprint, request

from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE

from src.product.http.validation import product_validatable_fields


# Endpoints para CRUD de product.


def create_product_blueprint(manage_product_usecase):
    blueprint = Blueprint("product", __name__)

    @blueprint.route("/seller-user/product", methods=["GET"])
    def get_products():
        """Retorna todos los productos"""

        products = manage_product_usecase.get_products()
        data = [product.serialize() for product in products]
        code = SUCCESS_CODE
        message = "product obtained succesfully"
        http_code = 200

        response = {
            "code": code,
            "message": message,
            "data": data,
        }

        return response, http_code

    @blueprint.route("/seller-user/product/<string:product_id>", methods=["GET"])
    def get_product(product_id):
        """Retorna producto según id"""

        product = manage_product_usecase.get_product(product_id)

        if product:
            data = product.serialize()
            code = SUCCESS_CODE
            message = "product obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = f"product of ID {product_id} does not exist."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.route("/seller-user/product", methods=["POST"])
    @validate_schema_flask(product_validatable_fields.PRODUCT_CREATION_VALIDATABLE_FIELDS)
    def create_product():
        """Crea un producto"""

        body = request.get_json()

        try:
            product = manage_product_usecase.create_product(body)
            data = product.serialize()
            code = SUCCESS_CODE
            message = "product created succesfully"
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

    @blueprint.route("/seller-user/product/<string:product_id>", methods=["PUT"])
    @validate_schema_flask(product_validatable_fields.PRODUCT_UPDATE_VALIDATABLE_FIELDS)
    def update_product(product_id):
        """Actualiza información de producto según ID"""

        body = request.get_json()

        try:
            product = manage_product_usecase.update_product(product_id, body)
            data = product.serialize()
            message = "product updated succesfully"
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

    @blueprint.route("/seller-user/product/<string:product_id>", methods=["DELETE"])
    def delete_product(product_id):
        """Elimina información del producto según id"""

        try:
            manage_product_usecase.delete_product(product_id)
            code = SUCCESS_CODE
            message = f"product of ID {product_id} deleted succesfully."
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
