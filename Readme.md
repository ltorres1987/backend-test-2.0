# Project Name: Desafío para postulación backend

### Descripción

Este proyecto fue desarrollado con el objetivo de participar para el puesto de backend en Envíame

### Construcción 🛠️
* **Language:** Python 3
* **Framework:** Flask, SQL Alchemy

## Requerimientos
- Docker
- Git
- Terminal(Cmder,cmd)

## Instalación

De forma predeterminada, los microservicios se ejecutarán en los siguientes puertos:
- ecommerce-service: 8000
- delivery-service: 8001

Es necesario tener disponible los puertos mencionados

Pasos:

1. Clone el proyecto.
2. Ejecute ```docker-compose``` dentro de la carpeta **docker-python**.
3. Construya las imagenes: ```docker-compose build```
4. Inicie contenedores: ```docker-compose up -d```
5. Reinicie delivery : ```docker restart delivery-service```
6. Reinicie ecommerce: ```docker restart ecommerce-service```
7. Para ejecutar las pruebas: ```docker exec ecommerce-service python -m pytest -rP```

En caso que requiera detener los docker ejecute el siguiente comando:
- Detener docker: ```docker-compose down```

## Ejecución

Para su ejecución es necesario acceder al siguiente link que contiene la documentación de la api.

https://documenter.getpostman.com/view/10015938/UVkjwy9P
