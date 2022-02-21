from flask import Blueprint, request

from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE

from src.seller.http.validation import seller_validatable_fields


# Endpoints para CRUD de seller.


def create_seller_blueprint(manage_seller_usecase):
    blueprint = Blueprint("seller", __name__)

    @blueprint.route("/marketplace/seller", methods=["GET"])
    def get_sellers():
        """Retorna todos los sellers"""

        sellers = manage_seller_usecase.get_sellers()

        data = [seller.serialize() for seller in sellers]
        code = SUCCESS_CODE
        message = "Seller obtained succesfully"
        http_code = 200

        response = {
            "code": code,
            "message": message,
            "data": data,
        }

        return response, http_code

    @blueprint.route("/marketplace/seller/<string:seller_id>", methods=["GET"])
    @blueprint.route("/seller-user/seller/<string:seller_id>", methods=["GET"])
    def get_seller(seller_id):
        """Retorna seller según ID"""

        seller = manage_seller_usecase.get_seller(seller_id)

        if seller:
            data = seller.serialize()
            code = SUCCESS_CODE
            message = "Seller obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = f"Seller of ID {seller_id} does not exist."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.route("/marketplace/seller", methods=["POST"])
    @validate_schema_flask(seller_validatable_fields.SELLER_CREATION_VALIDATABLE_FIELDS)
    def create_seller():
        """Crea un seller"""

        body = request.get_json()

        try:
            seller = manage_seller_usecase.create_seller(body)
            data = seller.serialize()
            code = SUCCESS_CODE
            message = "Seller created succesfully"
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

    @blueprint.route("/marketplace/seller/<string:seller_id>", methods=["PUT"])
    @blueprint.route("/seller-user/seller/<string:seller_id>", methods=["PUT"])
    @validate_schema_flask(seller_validatable_fields.SELLER_UPDATE_VALIDATABLE_FIELDS)
    def update_seller(seller_id):
        """Actualiza informacion del seller"""

        body = request.get_json()

        try:
            seller = manage_seller_usecase.update_seller(seller_id, body)
            data = seller.serialize()
            message = "Seller updated succesfully"
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

    @blueprint.route("/marketplace/seller/<string:seller_id>", methods=["DELETE"])
    def delete_seller(seller_id):
        """Elimina la información del seller"""

        try:
            manage_seller_usecase.delete_seller(seller_id)
            code = SUCCESS_CODE
            message = f"Seller of ID {seller_id} deleted succesfully."
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
