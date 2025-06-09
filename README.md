# Kaizen Backend
Este README explica cómo configurar y ejecutar el backend de Kaizen de forma local.

## Prerrequisitos

- Python 3.10+ instalado en tu sistema.
- MongoDB corriendo localmente (puede ser MongoDB Community).
- Git para clonar el repositorio.

## Setup

Para inciar localmente el servicio de base de datos, se debe instalar MongoDB Community Server V7.0 ([link para MacOS](https://www.mongodb.com/docs/v7.0/tutorial/install-mongodb-on-os-x/)) ([link para Windows](https://www.mongodb.com/docs/v7.0/tutorial/install-mongodb-on-windows/))

`brew services start mongodb-community@7.0`

## 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd BACK_Kaizen
```

## 2. Crear y activar entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate    # (Linux/Mac)
# o en Windows:
# venv\\Scripts\\activate
```

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 4. Configurar variables de entorno

1. Crea un archivo llamado `.env` en la raíz del proyecto.
2. Define al menos estas variables (ejemplo):

```
MONGODB_URI=mongodb://localhost:27017
MONGO_DB_NAME=kaizen_db
JWT_SECRET_KEY=clave_secreta_jwt
GEMINI_API=token_de_gemini_api
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

3. Guarda el archivo.

## 5. Iniciar la aplicación

```bash
cd src
uvicorn app.main:app --reload
```

- La opción `--reload` permite recargar automáticamente el servidor cuando cambias código.
- Por defecto la API quedará escuchando en http://127.0.0.1:8000

## 6. Probar endpoints

Puedes usar curl, Postman o Insomnia para probar:

- Registro de usuario:

  ```bash
  curl -X POST http://localhost:8000/auth/register \
    -H "Content-Type: application/json" \
    -d '{"email":"user@example.com","password":"MiPass123"}'
  ```

- Login:

  ```bash
  curl -X POST http://localhost:8000/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"user@example.com","password":"MiPass123"}'
  ```

- Crear hábito (requiere token):

  ```bash
  curl -X POST http://localhost:8000/habits/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer <TOKEN>" \
    -d '{"title":"Meditar","icon":"meditation","color":"blue","type":"personal","goal_period":"daily","goal_value":10,"goal_value_unit":"minutes","task_days":"Mon,Tue,Wed","reminders":"07:00","ikigai_category":"Health"}'
  ```

## 7. Detener el servidor

Presiona `Ctrl+C` en la terminal donde corre `uvicorn`.

