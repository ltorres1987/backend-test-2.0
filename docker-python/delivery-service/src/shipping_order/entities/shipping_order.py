from src.utils.utils import format_date


# Entidad representando a un order.


class ShippingOrder:

    def __init__(
            self, id, date, shipping_origin, shipping_destination, sell_order_id, client_name, status,
            order_detail=[None], order_tracking=[None], created_at=None, updated_at=None, deleted_at=None
    ):
        self.id = id
        self.date = date
        self.shipping_origin = shipping_origin
        self.shipping_destination = shipping_destination
        self.sell_order_id = sell_order_id
        self.client_name = client_name
        self.status = status

        if not order_detail:
            self.order_detail = order_detail

        if not order_tracking:
            self.order_tracking = order_tracking

        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):
        # Transforma los campos de este objeto a un diccionario,
        # útil para guardar contenido en los repositorios.

        return {

            "tracking_number": self.id,
            "status": self.status,
            "tracking": [{
                "status": detail_tracking.status,
                "date": detail_tracking.date,
            }
                for detail_tracking in self.order_tracking
            ]
        }

    def serialize(self):
        # Retorna un diccionario serializable a JSON.
        # Es parecido a "to_dict", pero es útil para mostrar datos en el exterior,
        # como por ejemplo retornar una respuesta hacia al usuario desde el endpoint.
        # En este caso no se retorna la fecha "deleted_at", ya que es información
        # privada, y las fechas se transforman a un formato legible.

        data = self.to_dict()

        return data

    def to_dict_detail(self):
        # Transforma los campos de este objeto a un diccionario,
        # útil para guardar contenido en los repositorios.

        return {

            "order":
                {
                    "foreing_order_id": self.sell_order_id,
                    "products": [{
                        "sku": detail_list.sku,
                        "name": detail_list.name,
                        "qty": detail_list.qty,
                    }
                        for detail_list in self.order_detail
                    ]
                },
            "origin": {
                "address": self.shipping_origin
            },
            "destination": {
                "name": self.client_name,
                "address": self.shipping_destination
            },
            "tracking_number": self.id,
            "status": self.status
        }

    def serialize_detail(self):
        # Retorna un diccionario serializable a JSON.
        # Es parecido a "to_dict", pero es útil para mostrar datos en el exterior,
        # como por ejemplo retornar una respuesta hacia al usuario desde el endpoint.
        # En este caso no se retorna la fecha "deleted_at", ya que es información
        # privada, y las fechas se transforman a un formato legible.

        data = self.to_dict_detail()

        return data

    @classmethod
    def from_dict(cls, dict):
        # Retorna una instancia de este objeto desde un diccionario de datos,
        # para no tener que llamar al constructor pasando los datos uno a uno.
        # Si un campo falta en el diccionario, se asume valor None.

        id = dict.get("id")
        date = dict.get("date")
        shipping_origin = dict["origin"]["address"]
        shipping_destination = dict["destination"]["address"]
        sell_order_id = dict["order"]["foreing_order_id"]
        client_name = dict["destination"]["name"]
        status = dict.get("status")
        order_detail = [None]
        order_tracking = [None]

        created_at = dict.get("created_at")
        updated_at = dict.get("updated_at")
        deleted_at = dict.get("deleted_at")

        return ShippingOrder(id=id, date=date, shipping_origin=shipping_origin,
                             shipping_destination=shipping_destination,
                             sell_order_id=sell_order_id, client_name=client_name, status=status,
                             order_detail=order_detail, order_tracking=order_tracking,
                             created_at=created_at, updated_at=updated_at, deleted_at=deleted_at)
