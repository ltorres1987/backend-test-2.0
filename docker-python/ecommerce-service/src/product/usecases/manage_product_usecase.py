from src.product.entities.product import Product
from src.utils import utils


# Casos de uso para el manejo de product.


class ManageProductUsecase:

    def __init__(self, product_repository):
        self.product_repository = product_repository

    def get_products(self):

        # Retorna una lista de entidades product desde el repositorio.

        return self.product_repository.get_products()

    def get_product(self, product_id):

        # Retorna una instancia de product según la ID recibida.

        return self.product_repository.get_product(product_id)

    def create_product(self, data):

        # Crea una instancia product desde la data recibida, que ya debe venir validada desde afuera,
        # y guarda dicha instancia en el repositorio para finalmente retornarla.

        current_time = utils.get_current_datetime()

        data["created_at"] = current_time
        data["updated_at"] = current_time

        product = Product.from_dict(data)
        product = self.product_repository.create_product(product)

        return product

    def update_product(self, product_id, data):

        # Actualiza los datos recibidos y los guarda en el repositorio según la ID recibida.
        # La data no necesariamente debe contener todos los campos de la entidad, sólo
        # los campos que se van a actualizar. Esta data debe venir validada desde afuera.

        product = self.get_product(product_id)

        if product:

            data["updated_at"] = utils.get_current_datetime()
            product = self.product_repository.update_product(product_id, data)

            return product

        else:
            raise ValueError(f"product of ID {product_id} doesn't exist.")

    def delete_product(self, product_id):

        # Realiza un soft-delete del product con la ID especificada, si es que existe.
        # A nivel de repositorio realiza una actualización al campo "deleted_at".

        product = self.get_product(product_id)

        if product:

            data = {
                "deleted_at": utils.get_current_datetime()
            }

            product = self.product_repository.update_product(product_id, data)

        else:
            raise ValueError(f"product of ID {product_id} doesn't exist or is already deleted.")
