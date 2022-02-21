# Constantes que definen el "esquema" del payload que hay que validar
# para el caso de crear o actualizar un libro. Estos esquemas son usados
# en el decorador "validate_schema_flask" usado en los blueprints.

# La diferencia entre el esquema de creación y el de actualización es que
# en este último los campos son opcionales, y en algunos casos algunos campos
# podrían sólo definirse en la creación pero no permitir su actualización.

SHIPPINGORDER_CREATION_VALIDATABLE_FIELDS = {

    "order": {
        'schema': {

            "foreing_order_id": {
                "required": True,
                "type": "integer",
                "empty": False,
                "min": 1,
            },

            'products': {
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

                        "name": {
                            "required": True,
                            "type": "string",
                            "empty": False,
                            "minlength": 1,
                            "maxlength": 100,
                        },

                        "qty": {
                            "required": True,
                            "type": "integer",
                            "empty": False,
                            "min": 1,
                        },
                    }
                }
            }
        }
    },

    "origin": {
        'schema': {
            "address": {
                "required": True,
                "type": "string",
                "empty": False,
                "minlength": 1,
                "maxlength": 200,
            },
        }
    },

    "destination": {
        'schema': {
            "name": {
                "required": True,
                "type": "string",
                "empty": False,
                "minlength": 1,
                "maxlength": 100,
            },
            "address": {
                "required": True,
                "type": "string",
                "empty": False,
                "minlength": 1,
                "maxlength": 200,
            },
        }
    },

}

TRACKING_UPDATE_VALIDATABLE_FIELDS = {

    "foreing_order_id": {
        "required": True,
        "type": "integer",
        "empty": False,
        "min": 1,
    },

    "tracking_number": {
        "required": True,
        "type": "integer",
        "empty": False,
        "min": 1,
    },

}

SHIPPINGORDER_UPDATE_VALIDATABLE_FIELDS = {

    "order": {
        'schema': {

            "foreing_order_id": {
                "required": False,
                "type": "integer",
                "empty": False,
                "min": 1,
            },

            'products': {
                "required": False,
                "type": "list",
                "empty": False,

                'schema': {
                    "required": False,
                    'type': 'dict',
                    "empty": False,

                    'schema': {
                        "sku": {
                            "required": False,
                            "type": "integer",
                            "empty": False,
                            "min": 1,
                        },

                        "name": {
                            "required": False,
                            "type": "string",
                            "empty": False,
                            "minlength": 1,
                            "maxlength": 100,
                        },

                        "qty": {
                            "required": False,
                            "type": "integer",
                            "empty": False,
                            "min": 1,
                        },
                    }
                }
            }
        }
    },

    "origin": {
        'schema': {
            "address": {
                "required": False,
                "type": "string",
                "empty": False,
                "minlength": 1,
                "maxlength": 200,
            },
        }
    },

    "destination": {
        'schema': {
            "name": {
                "required": False,
                "type": "string",
                "empty": False,
                "minlength": 1,
                "maxlength": 100,
            },
            "address": {
                "required": False,
                "type": "string",
                "empty": False,
                "minlength": 1,
                "maxlength": 200,
            },
        }
    },

}
