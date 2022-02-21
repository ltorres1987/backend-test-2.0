from src.seller.entities.seller import Seller
from src.utils import utils


# Casos de uso para el manejo de seller.


class ManageSellerUsecase:

    def __init__(self, seller_repository):
        self.seller_repository = seller_repository

    def get_sellers(self):

        # Retorna una lista de entidades seller desde el repositorio.

        return self.seller_repository.get_sellers()

    def get_seller(self, seller_id):

        # Retorna una instancia de seller según la ID recibida.

        return self.seller_repository.get_seller(seller_id)

    def create_seller(self, data):

        # Crea una instancia seller desde la data recibida, que ya debe venir validada desde afuera,
        # y guarda dicha instancia en el repositorio para finalmente retornarla.

        current_time = utils.get_current_datetime()

        data["created_at"] = current_time
        data["updated_at"] = current_time

        seller = Seller.from_dict(data)
        seller = self.seller_repository.create_seller(seller)

        return seller

    def update_seller(self, seller_id, data):

        # Actualiza los datos recibidos y los guarda en el repositorio según la ID recibida.
        # La data no necesariamente debe contener todos los campos de la entidad, sólo
        # los campos que se van a actualizar. Esta data debe venir validada desde afuera.

        seller = self.get_seller(seller_id)

        if seller:

            data["updated_at"] = utils.get_current_datetime()
            seller = self.seller_repository.update_seller(seller_id, data)

            return seller

        else:
            raise ValueError(f"Seller of ID {seller_id} doesn't exist.")

    def delete_seller(self, seller_id):

        # Realiza un soft-delete del seller con la ID especificada, si es que existe.
        # A nivel de repositorio realiza una actualización al campo "deleted_at".

        seller = self.get_seller(seller_id)

        if seller:

            data = {
                "deleted_at": utils.get_current_datetime()
            }

            seller = self.seller_repository.update_seller(seller_id, data)

        else:
            raise ValueError(f"Seller of ID {seller_id} doesn't exist or is already deleted.")
