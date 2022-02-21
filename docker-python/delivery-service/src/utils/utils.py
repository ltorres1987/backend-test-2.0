from datetime import datetime, timezone

# Funciones de utilidad para el sistema completo.

# Si bien no va dentro de ninguna de las carpetas de contexto ("books" o "greeting"),
# estas funciones corresponden a la capa más interna de Clean Architecture, que corresponde
# a la capa Entities. Esta capa no solamente puede contener entidades, sino cualquier código
# que es usado a nivel de aplicación completo.

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def filter_dict(dict, fields):

    # Filtra el diccionario entrante, retornando nuevo diccionario
    # sólo con los campos definidos y descartando los demás.

    filtered_dict = {}

    for key in dict:

        if key in fields:
            filtered_dict[key] = dict[key]

    return filtered_dict

def format_date(datetime):

    # Retorna una representación en String de una fecha/hora dada.

    return datetime.strftime(DATE_FORMAT)

def get_current_datetime():

    # Retorna la fecha actual en UTC-0
    
    return datetime.now(timezone.utc)