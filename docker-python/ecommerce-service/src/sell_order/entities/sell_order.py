from src.utils.utils import format_date


# Entidad representando a un order.


class SellOrder:

    def __init__(
            self, id, date, shipping_origin, shipping_destination, seller_user, user_id, status,
            order_detail=[None], created_at=None, updated_at=None, deleted_at=None
    ):
        self.id = id
        self.date = date
        self.shipping_origin = shipping_origin
        self.shipping_destination = shipping_destination
        self.seller_user = seller_user
        self.user_id = user_id
        self.status = status

        if not order_detail:
            self.order_detail = order_detail

        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):
        # Transforma los campos de este objeto a un diccionario,
        # útil para guardar contenido en los repositorios.

        return {
            "id": self.id,
            "date": self.date,
            "shipping_origin": self.shipping_origin,
            "shipping_destination": self.shipping_destination,
            "seller_user": self.seller_user,
            "user_id": self.user_id,
            "status": self.status,

            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }

    def serialize(self):
        # Retorna un diccionario serializable a JSON.
        # Es parecido a "to_dict", pero es útil para mostrar datos en el exterior,
        # como por ejemplo retornar una respuesta hacia al usuario desde el endpoint.
        # En este caso no se retorna la fecha "deleted_at", ya que es información
        # privada, y las fechas se transforman a un formato legible.

        data = self.to_dict()

        data.pop("deleted_at")

        data["created_at"] = format_date(data["created_at"])
        data["updated_at"] = format_date(data["updated_at"])

        return data

    def to_dict_detail(self):
        # Transforma los campos de este objeto a un diccionario,
        # útil para guardar contenido en los repositorios.

        return {
            "id": self.id,
            "date": self.date,
            "shipping_origin": self.shipping_origin,
            "shipping_destination": self.shipping_destination,
            "seller_user": self.seller_user,
            "user_id": self.user_id,
            "status": self.status,
            "detail": [{
                "sku": detail_list.sku,
                "quantity": detail_list.quantity,
            }
                for detail_list in self.order_detail
            ],

            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }

    def serialize_detail(self):
        # Retorna un diccionario serializable a JSON.
        # Es parecido a "to_dict", pero es útil para mostrar datos en el exterior,
        # como por ejemplo retornar una respuesta hacia al usuario desde el endpoint.
        # En este caso no se retorna la fecha "deleted_at", ya que es información
        # privada, y las fechas se transforman a un formato legible.

        data = self.to_dict_detail()

        data.pop("deleted_at")

        data["created_at"] = format_date(data["created_at"])
        data["updated_at"] = format_date(data["updated_at"])

        return data

    @classmethod
    def from_dict(cls, dict):
        # Retorna una instancia de este objeto desde un diccionario de datos,
        # para no tener que llamar al constructor pasando los datos uno a uno.
        # Si un campo falta en el diccionario, se asume valor None.

        id = dict.get("id")
        date = dict.get("date")
        shipping_origin = dict.get("shipping_origin")
        shipping_destination = dict.get("shipping_destination")
        seller_user = dict.get("seller_user")
        user_id = dict.get("user_id")
        status = dict.get("status")
        order_detail = [None]

        created_at = dict.get("created_at")
        updated_at = dict.get("updated_at")
        deleted_at = dict.get("deleted_at")

        return SellOrder(id=id, date=date, shipping_origin=shipping_origin, shipping_destination=shipping_destination,
                         seller_user=seller_user, user_id=user_id, status=status, order_detail=order_detail,
                         created_at=created_at, updated_at=updated_at, deleted_at=deleted_at)
