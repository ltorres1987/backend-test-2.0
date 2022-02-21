from flask import Blueprint, request

from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE

from src.user.http.validation import user_validatable_fields


# Endpoints para CRUD de user.


def create_user_blueprint(manage_user_usecase):
    blueprint = Blueprint("user", __name__)

    @blueprint.route("/internet-user/user", methods=["GET"])
    def get_users():
        """Retorna todos los users"""

        users = manage_user_usecase.get_users()
        data = [user.serialize() for user in users]
        code = SUCCESS_CODE
        message = "User obtained succesfully"
        http_code = 200

        response = {
            "code": code,
            "message": message,
            "data": data,
        }

        return response, http_code

    @blueprint.route("/internet-user/user/<string:user_id>", methods=["GET"])
    def get_user(user_id):
        """Retorna un user según ID"""

        user = manage_user_usecase.get_user(user_id)

        if user:
            data = user.serialize()
            code = SUCCESS_CODE
            message = "User obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = f"User of ID {user_id} does not exist."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.route("/internet-user/user", methods=["POST"])
    @validate_schema_flask(user_validatable_fields.USER_CREATION_VALIDATABLE_FIELDS)
    def create_user():
        """Crea un user"""

        body = request.get_json()

        try:
            user = manage_user_usecase.create_user(body)
            data = user.serialize()
            code = SUCCESS_CODE
            message = "User created succesfully"
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

    @blueprint.route("/internet-user/user/<string:user_id>", methods=["PUT"])
    @validate_schema_flask(user_validatable_fields.USER_UPDATE_VALIDATABLE_FIELDS)
    def update_user(user_id):
        """Actualiza user según ID"""

        body = request.get_json()

        try:
            user = manage_user_usecase.update_user(user_id, body)
            data = user.serialize()
            message = "User updated succesfully"
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

    @blueprint.route("/internet-user/user/<string:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        """Elimina user según ID"""

        try:
            manage_user_usecase.delete_user(user_id)
            code = SUCCESS_CODE
            message = f"User of ID {user_id} deleted succesfully."
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
