Kaizen Back


## Setup

Para inciar localmente el servicio de base de datos, se debe instalar MongoDB Community Server V7.0 ([link para MacOS](https://www.mongodb.com/docs/v7.0/tutorial/install-mongodb-on-os-x/)) ([link para Windows](https://www.mongodb.com/docs/v7.0/tutorial/install-mongodb-on-windows/))

`brew services start mongodb-community@7.0`

Una vez inicializado se entra a la consola de mongo y se crea la base de datos

`mongosh`

`use kaizenapp-db` (podría usarse como variable de entorno)

Luego se instala la librería Beanie, un ODM para MongoDB hecho para FastAPI

`pip install beanie` (en verdad esto se soluciona con el pip install requirements)
