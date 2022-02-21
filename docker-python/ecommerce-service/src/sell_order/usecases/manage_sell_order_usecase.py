import os

from src.sell_order.entities.sell_order import SellOrder

from src.sell_order_detail.entities.sell_order_detail import SellOrderDetail

from src.utils import utils

import requests


# Casos de uso para el manejo de sell_order.


class ManageSellOrderUsecase:

    def __init__(self, sell_order_repository, product_repository, user_repository):
        self.sell_order_repository = sell_order_repository
        self.product_repository = product_repository
        self.user_repository = user_repository

    def get_sell_orders(self):

        # Retorna una lista de entidades sell_order desde el repositorio.

        return self.sell_order_repository.get_sell_orders()

    def get_sell_order(self, sell_order_id):

        # Retorna una instancia de sell_order según la ID recibida.

        return self.sell_order_repository.get_sell_order(sell_order_id)

    def get_sell_order_by_seller_user_id(self, seller_user, sell_order_id):

        # Permite la consulta de todos las ordenes de venta activas de un usuario vendedor según ID

        return self.sell_order_repository.get_sell_order_by_seller_user_id(seller_user, sell_order_id)

    def get_sell_order_by_seller_user(self, seller_user):

        # permite la consulta de todos las ordenes de venta activas de un usuario vendedor

        return self.sell_order_repository.get_sell_order_by_seller_user(seller_user)

    def create_sell_order(self, data):

        # Crea una orden de venta

        current_time = utils.get_current_datetime()

        data["date"] = current_time
        data["status"] = "created"
        data["created_at"] = current_time
        data["updated_at"] = current_time

        sell_order = SellOrder.from_dict(data)

        sell_order_detail_dict = []
        product_dict = []
        msg_err = []

        # valida si existe usuario cliente
        user = self.user_repository.get_user(data["user_id"])

        if not user:
            msg_err.append(f"user of ID: {data['user_id']} doesnt exist.")

        # valida detalles
        for data_detail in data["detail"]:

            product = self.product_repository.get_product(data_detail["sku"])

            # valida si existe producto
            if product:

                # validate stock
                if data_detail["quantity"] <= product.quantity:

                    # informacion de la cabecera sell order
                    data_detail["created_at"] = current_time
                    data_detail["updated_at"] = current_time
                    sell_order_detail_dict.append(SellOrderDetail.from_dict(data_detail))

                    # actualizacion de stock
                    data_product = {
                        "sku": data_detail["sku"],
                        "fields": {
                            "quantity": product.quantity - data_detail["quantity"],
                            "updated_at": utils.get_current_datetime()
                        }
                    }

                    product_dict.append(data_product)

                else:
                    msg_err.append(
                        f"product of ID: {data_detail['sku']} is out of stock. available: {product.quantity}")

            else:
                msg_err.append(f"product of ID: {data_detail['sku']} doesnt exist.")

        # valida errores
        if msg_err:
            raise ValueError(msg_err)

        else:
            sell_order = self.sell_order_repository.create_sell_order(sell_order,
                                                                      sell_order_detail_dict,
                                                                      product_dict)

        return sell_order

    def update_sell_order_by_seller_user(self, seller_user, sell_order_id, data):
        """Permite la actualización de estado de una orden de venta activa de un usuario vendedor según ID.
        Puede cambiar de:
        "created" a "confirmed"
        "confirmed" a "dispatched"
        El servicio solo acepta los siguientes estados:
        "confirmed"
        "dispatched"
        Si envia el estado "dispatched" el servicio realizara la entrega de la información al
        endpoint del service delivery"
        """

        # parametros de consumo
        username = os.environ["JWT_USER"]
        password = os.environ["JWT_PASS"]
        base_url = os.environ["DELIVERY_BASE_URL"]

        sell_order = self.get_sell_order_by_seller_user_id(seller_user, sell_order_id)

        # valida que exista sell order
        if sell_order:

           # valida estados
            if (sell_order[0].status == "created" and data["status"] == "confirmed") or (
                    sell_order[0].status == "confirmed" and data["status"] == "dispatched"):

                # guarda el estado orden de venta
                data["updated_at"] = utils.get_current_datetime()
                sell_order = self.sell_order_repository.update_sell_order(sell_order_id, data)

                # Consume servicio entrega
                if data["status"] == "dispatched":

                    # consume servicios de entrega
                    try:

                        # Arma respuesta

                        body = {

                            "order":
                                {
                                    "foreing_order_id": sell_order[0].id,
                                    "products": [{
                                        "sku": detail.sku,
                                        "name": detail.product_detail.name,
                                        "qty": detail.quantity,
                                    }
                                        for detail in sell_order[0].order_detail
                                    ]
                                },
                            "origin": {
                                "address": sell_order[0].shipping_origin
                            },
                            "destination": {
                                "name": sell_order[0].customer_data.name,
                                "address": sell_order[0].shipping_destination,
                            }
                        }

                        # solicita token de acceso
                        url = f"{base_url}/login/access-token"
                        res = requests.post(url, json={'username': username, "password": password})

                        access_token_body = res.json()
                        token = f"Bearer {access_token_body['data']['access_token']}"

                        # consume el servicio de delivery
                        url = f"{base_url}/shipping_order"
                        res = requests.post(url, json=body, headers={"Authorization": token})

                        if res:
                            print('Response OK')
                        else:
                            print('Response Failed')
                            # Reversa el estado de la orden de venta
                            self.update_sell_order_reverse(sell_order_id, data)

                    except requests.exceptions.RequestException as e:
                        # Reversa el estado de la orden de venta
                        self.update_sell_order_reverse(sell_order_id, data)

                return sell_order
            else:

                if data["status"] == "confirmed":
                    raise ValueError(f"The sales order status is different from created")
                else:
                    raise ValueError("The sales order status is different from confirmed")

        else:
            raise ValueError(f"SellOrder of ID {sell_order_id} doesn't exist.")

    def update_sell_order_reverse(self, sell_order_id, data):
        """Reversa el estado de la orden de venta si falla la comunicación del servicio delivery """

        if data["status"] == "confirmed":
            data["status"] = "created"
        else:
            data["status"] = "confirmed"

        sell_order = self.sell_order_repository.update_sell_order_by_seller_user(sell_order_id, data)

        raise ValueError("There was an error in communication with the delivery service")

    def update_sell_order_cancelled(self, sell_order_id):
        """Con el siguiente enpoint puede "cancelar" un pedido solo si el estado es "created" o "confirmed".
        En caso de cancelación de un pedido se deberá aumentar el stock disponible de los productos.
        """

        # parametros de consumo
        username = os.environ["JWT_USER"]
        password = os.environ["JWT_PASS"]
        base_url = os.environ["DELIVERY_BASE_URL"]

        sell_order = self.get_sell_order(sell_order_id)

        product_dict = []
        if sell_order:

            if sell_order[0].status == "created" or sell_order[0].status == "confirmed":

                data = {
                    "status": "cancelled",
                    "updated_at": utils.get_current_datetime()
                }

                # determina los productos alimentar nuevamente el stock
                for product_detail in sell_order[0].order_detail:
                    product = self.product_repository.get_product(product_detail.sku)

                    data_product = {
                        "sku": product_detail.sku,
                        "fields": {
                            "quantity": product_detail.quantity + product.quantity,
                            "updated_at": utils.get_current_datetime()
                        }
                    }
                    product_dict.append(data_product)

                sell_order = self.sell_order_repository.update_sell_order_cancelled(sell_order_id, data, product_dict)

                # Notifica al servicio delivery el cambio de estatus
                # consume servicios de ecommerce
                try:
                    # solicita token de acceso
                    url = f"{base_url}/login/access-token"
                    res = requests.post(url, json={'username': username, "password": password})

                    access_token_body = res.json()
                    token = f"Bearer {access_token_body['data']['access_token']}"

                    # consume el servicio de ecommerce
                    url = f"{base_url}/status_change_shipping_order/{sell_order_id}"
                    res = requests.put(url, headers={"Authorization": token})

                    if res:
                        print('Response OK')
                    else:
                        print('Response Failed')


                except requests.exceptions.RequestException as e:
                    print("There was an error in communication with the ecommerce service")

                return sell_order
            else:
                raise ValueError("Sales order status is not confirmed or created")
        else:
            raise ValueError(f"SellOrder of ID {sell_order_id} doesn't exist.")

    def update_sell_order_status_delivered(self, sell_order_id):
        """Actualiza estado de la orden de venta a - delivered"""

        sell_order = self.get_sell_order(sell_order_id)

        if sell_order:

            data = {
                "status": "delivered",
                "updated_at": utils.get_current_datetime()
            }

            sell_order = self.sell_order_repository.update_sell_order(sell_order_id, data)

        else:
            raise ValueError(f"SellOrder of ID {sell_order_id} doesn't exist or is already update.")
