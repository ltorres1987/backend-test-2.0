# Constantes que definen el "esquema" del payload que hay que validar
# para el caso de crear o actualizar un libro. Estos esquemas son usados
# en el decorador "validate_schema_flask" usado en los blueprints.

# La diferencia entre el esquema de creación y el de actualización es que
# en este último los campos son opcionales, y en algunos casos algunos campos
# podrían sólo definirse en la creación pero no permitir su actualización.

SELLORDER_CREATION_VALIDATABLE_FIELDS = {

    "user_id": {
        "required": True,
        "type": "integer",
        "empty": False,
        "min": 1,
    },

    "shipping_destination": {
        "required": True,
        "type": "string",
        "empty": False,
        "minlength": 1,
        "maxlength": 200,
    },

    "shipping_origin": {
        "required": True,
        "type": "string",
        "empty": False,
        "minlength": 1,
        "maxlength": 200,
    },

    "seller_user": {
        "required": True,
        "type": "string",
        "empty": False,
        "minlength": 1,
        "maxlength": 100,
    },

    'detail': {
        "required": True,
        "type": "list",
        "empty": False,

        'schema': {
            "required": True,
            'type': 'dict',
            "empty": False,

            'schema': {
                "sku": {
                    "required": True,
                    "type": "integer",
                    "empty": False,
                    "min": 1,
                },
                "quantity": {
                    "required": True,
                    "type": "integer",
                    "empty": False,
                    "min": 1,
                },
            }
        }
    }
}

SELLORDER_SELLER_USER_UPDATE_VALIDATABLE_FIELDS = {

    "status": {
        "required": True,
        "type": 'string',
        "empty": False,
        "allowed": ['confirmed', 'dispatched']
    },

}
