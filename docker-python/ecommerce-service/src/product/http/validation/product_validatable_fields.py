# Constantes que definen el "esquema" del payload que hay que validar
# para el caso de crear o actualizar un libro. Estos esquemas son usados
# en el decorador "validate_schema_flask" usado en los blueprints.

# La diferencia entre el esquema de creación y el de actualización es que
# en este último los campos son opcionales, y en algunos casos algunos campos
# podrían sólo definirse en la creación pero no permitir su actualización.

PRODUCT_CREATION_VALIDATABLE_FIELDS = {

    "name": {
        "required": True,
        "type": "string",
        "empty": False,
        "minlength": 1,
        "maxlength": 100,
    },

    "short_description": {
        "required": True,
        "type": "string",
        "empty": False,
        "minlength": 1,
        "maxlength": 100,
    },

    "quantity": {
        "required": True,
        "type": "integer",
        "empty": False,
        "min": 1,
    },

    "seller_id": {
        "required": True,
        "type": "integer",
        "empty": False,
        "min": 1,
    },

}

PRODUCT_UPDATE_VALIDATABLE_FIELDS = {

    "name": {
        "required": False,
        "type": "string",
        "empty": False,
        "minlength": 1,
        "maxlength": 100,
    },

    "short_description": {
        "required": False,
        "type": "string",
        "empty": False,
        "minlength": 1,
        "maxlength": 100,
    },

    "quantity": {
        "required": False,
        "type": "integer",
        "empty": False,
        "min": 1,
    },

    "seller_id": {
        "required": False,
        "type": "integer",
        "empty": False,
        "min": 1,
    },

}
