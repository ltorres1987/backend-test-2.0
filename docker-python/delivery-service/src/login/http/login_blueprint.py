from flask import Blueprint, request

from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE

from src.login.http.validation import login_validatable_fields


# Endpoints


def create_login_blueprint(manage_login_usecase):
    blueprint = Blueprint("login", __name__)

    @blueprint.route("/login/access-token", methods=["POST"])
    @validate_schema_flask(login_validatable_fields.LOGIN_CREATION_VALIDATABLE_FIELDS)
    def create_login():

        body = request.get_json()

        try:
            login = manage_login_usecase.create_login(body)
            data = login
            code = SUCCESS_CODE
            message = "Jwt created succesfully"
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

    return blueprint
