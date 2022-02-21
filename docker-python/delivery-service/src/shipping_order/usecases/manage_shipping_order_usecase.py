import random
import os
import requests

from src.shipping_order.entities.shipping_order import ShippingOrder

from src.utils import utils

from src.shipping_order_detail.entities.shipping_order_detail import ShippingOrderDetail

from src.tracking.entities.tracking import Tracking


# Casos de uso para el manejo de shipping_order.

# Recibe en el constructor el repositorio a utilizar. Da igual si recibe el repositorio
# de SQL o de Firestore, el caso de uso debe funcionar independientemente de su implementación.


class ManageShippingOrderUsecase:

    def __init__(self, shipping_order_repository):
        self.shipping_order_repository = shipping_order_repository

    def get_shipping_orders(self):

        # Retorna una lista de entidades shipping_order desde el repositorio.

        return self.shipping_order_repository.get_shipping_orders()

    def get_shipping_order(self, shipping_order_id):

        # Retorna una instancia de shipping_order según la ID recibida.

        return self.shipping_order_repository.get_shipping_order(shipping_order_id)

    def get_tracking(self, data):

        """Con el siguiente enpoint permite la consulta del traking de un delivery"""

        shipping_order_id = data["foreing_order_id"]

        return self.shipping_order_repository.get_tracking(shipping_order_id)

    def create_shipping_order(self, data):

        """Con el siguiente enpoint autenticado permite la creación de un delivery y traking.
        este servicio se consume desde ecommerce cuando el estado se cambie a "dispatched
        """

        current_time = utils.get_current_datetime()

        data["status"] = "dispatched"
        data["date"] = current_time
        data["created_at"] = current_time
        data["updated_at"] = current_time

        shipping_order = ShippingOrder.from_dict(data)

        # prepara productos
        shipping_order_detail_dict = []
        for product_list in data["order"]["products"]:
            data_product = {
                "sku": product_list["sku"],
                "name": product_list["name"],
                "qty": product_list["qty"],
                "created_at": current_time,
                "updated_at": current_time
            }

            shipping_order_detail_dict.append(ShippingOrderDetail.from_dict(data_product))

        # tracking
        data_tracking = {
            "status": "READY_FOR_PICK_UP",
            "date": current_time,
            "created_at": current_time,
            "updated_at": current_time
        }

        shipping_order_tracking = Tracking.from_dict(data_tracking)

        # registra delivery y traking
        shipping_order = self.shipping_order_repository.create_shipping_order(shipping_order,
                                                                              shipping_order_detail_dict,
                                                                              shipping_order_tracking)

        return shipping_order

    def update_status_change_tracking(self):

        """permite cambiar el estado de todos los pedidos
        Este endpoint será consumido por un docker crontab cada 30 segundos
        """

        # parametros de consumo
        username = os.environ["JWT_USER"]
        password = os.environ["JWT_PASS"]
        base_url = os.environ["ECOMMERCE_BASE_URL"]

        current_time = utils.get_current_datetime()
        shipping_orders = self.shipping_order_repository.get_status_change_tracking()

        # recorre las entregas
        for shipping_order in shipping_orders:

            # obtiene el valor mayor de la lista tracking con su status
            max_value, status_tracking = max([[i.id, i.status] for i in shipping_order.order_tracking],
                                             key=lambda item: item[0])

            if status_tracking == "READY_FOR_PICK_UP":
                status = "AT_ORIGIN"

            if status_tracking == "AT_ORIGIN":
                status = "EN_ROUTE_OF_DELIVERY"

            if status_tracking == "EN_ROUTE_OF_DELIVERY":

                if random.randrange(1, 3) == 1:
                    status = "NOT_DELIVERED"
                else:
                    status = "DELIVERED"

            if status_tracking == "NOT_DELIVERED":
                status = "EN_ROUTE_OF_DELIVERY"

            # si la entrega se encuentra en estatus "DELIVERED" marco la cabecera
            if status == "DELIVERED":
                data = {
                    "status": "delivered",
                    "updated_at": current_time
                }
            else:
                data = {
                    "status": shipping_order.status,
                    "updated_at": current_time
                }

            # tracking
            data_tracking = {
                "shipping_order_id": shipping_order.id,
                "status": status,
                "date": current_time,
                "created_at": current_time,
                "updated_at": current_time
            }

            tracking = Tracking.from_dict(data_tracking)

            shipping_order = self.shipping_order_repository.update_status_change_tracking(shipping_order.id, data,
                                                                                          tracking)

            # Notifica al servicio ecommerce la entrega de los productos
            if data["status"] == "delivered":

                # consume servicios de ecommerce
                try:
                    # solicita token de acceso
                    url = f"{base_url}/login/access-token"
                    res = requests.post(url, json={'username': username, "password": password})

                    access_token_body = res.json()
                    token = f"Bearer {access_token_body['data']['access_token']}"

                    # consume el servicio de ecommerce
                    url = f"{base_url}/sell-order/{shipping_order.id}"
                    res = requests.put(url, headers={"Authorization": token})

                    if res:
                        print('Response OK')
                    else:
                        print('Response Failed')


                except requests.exceptions.RequestException as e:
                    print("There was an error in communication with the ecommerce service")

    def update_shipping_order(self, shipping_order_id, body):

        # Actualiza los datos recibidos y los guarda en el repositorio según la ID recibida.
        # La data no necesariamente debe contener todos los campos de la entidad, sólo
        # los campos que se van a actualizar. Esta data debe venir validada desde afuera.

        current_time = utils.get_current_datetime()
        data = {}
        shipping_order = self.get_shipping_order(shipping_order_id)

        if shipping_order:

            data["sell_order_id"] = body["order"]["foreing_order_id"]
            data["shipping_origin"] = body["origin"]["address"]
            data["shipping_destination"] = body["destination"]["address"]
            data["client_name"] = body["destination"]["name"]
            data["updated_at"] = current_time

            shipping_order = self.shipping_order_repository.update_shipping_order(shipping_order_id, data)

            return shipping_order

        else:
            raise ValueError(f"Seller of ID {shipping_order_id} doesn't exist.")

    def status_change_shipping_order(self, sell_order_id, data):
        """Actualiza el status delivery desde microservicio ecommerce"""

        current_time = utils.get_current_datetime()
        shipping_order = self.shipping_order_repository.get_status_change_shipping_order(sell_order_id)

        if shipping_order:

            data["updated_at"] = current_time

            shipping_order = self.shipping_order_repository.update_shipping_order(shipping_order.id, data)

            return shipping_order

        else:
            raise ValueError(f"shipping_order of ID {sell_order_id} doesn't exist.")

    def delete_shipping_order(self, shipping_order_id):

        # Realiza un soft-delete del shipping_order con la ID especificada, si es que existe.
        # A nivel de repositorio realiza una actualización al campo "deleted_at".

        shipping_order = self.get_shipping_order(shipping_order_id)

        if shipping_order:

            data = {
                "deleted_at": utils.get_current_datetime()
            }

            shipping_order = self.shipping_order_repository.delete_shipping_order(shipping_order_id, data)

        else:
            raise ValueError(f"Seller of ID {shipping_order_id} doesn't exist or is already deleted.")
