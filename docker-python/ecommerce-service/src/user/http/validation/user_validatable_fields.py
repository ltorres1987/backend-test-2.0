# Constantes que definen el "esquema" del payload que hay que validar
# para el caso de crear o actualizar un libro. Estos esquemas son usados
# en el decorador "validate_schema_flask" usado en los blueprints.

# La diferencia entre el esquema de creación y el de actualización es que
# en este último los campos son opcionales, y en algunos casos algunos campos
# podrían sólo definirse en la creación pero no permitir su actualización.

USER_CREATION_VALIDATABLE_FIELDS = {

    "name": {
        "required": True,
        "type": "string",
        "empty": False,
        "minlength": 1,
        "maxlength": 100,
    },

    "email": {
        "required": True,
        "type": "string",
        "empty": False,
        "minlength": 1,
        "maxlength": 100,
        "regex": "^((\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*)|(\s*))$"
    },

    "city": {
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

USER_UPDATE_VALIDATABLE_FIELDS = {

    "name": {
        "required": False,
        "type": "string",
        "empty": False,
        "minlength": 1,
        "maxlength": 100,
    },

    "email": {
        "required": False,
        "type": "string",
        "empty": False,
        "minlength": 1,
        "maxlength": 100,
        "regex": "^((\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*)|(\s*))$"
    },

    "city": {
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
