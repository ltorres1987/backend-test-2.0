from src.user.entities.user import User
from src.utils import utils


# Casos de uso para el manejo de user.


class ManageUserUsecase:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def get_users(self):

        # Retorna una lista de entidades user desde el repositorio.

        return self.user_repository.get_users()

    def get_user(self, user_id):

        # Retorna una instancia de user según la ID recibida.

        return self.user_repository.get_user(user_id)

    def create_user(self, data):

        # Crea una instancia user desde la data recibida, que ya debe venir validada desde afuera,
        # y guarda dicha instancia en el repositorio para finalmente retornarla.

        current_time = utils.get_current_datetime()

        data["created_at"] = current_time
        data["updated_at"] = current_time

        user = User.from_dict(data)
        user = self.user_repository.create_user(user)

        return user

    def update_user(self, user_id, data):

        # Actualiza los datos recibidos y los guarda en el repositorio según la ID recibida.
        # La data no necesariamente debe contener todos los campos de la entidad, sólo
        # los campos que se van a actualizar. Esta data debe venir validada desde afuera.

        user = self.get_user(user_id)

        if user:

            data["updated_at"] = utils.get_current_datetime()
            user = self.user_repository.update_user(user_id, data)

            return user

        else:
            raise ValueError(f"User of ID {user_id} doesn't exist.")

    def delete_user(self, user_id):

        # Realiza un soft-delete del user con la ID especificada, si es que existe.
        # A nivel de repositorio realiza una actualización al campo "deleted_at".

        user = self.get_user(user_id)

        if user:

            data = {
                "deleted_at": utils.get_current_datetime()
            }

            user = self.user_repository.update_user(user_id, data)

        else:
            raise ValueError(f"User of ID {user_id} doesn't exist or is already deleted.")
