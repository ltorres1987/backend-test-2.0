from flask_jwt_extended import create_access_token


class ManageLoginUsecase:

    def __init__(self):
        pass

    def create_login(self, data):
        username = data["username"]
        password = data["password"]

        access_token = create_access_token(identity=username)
        return {
            "access_token": access_token
        }
