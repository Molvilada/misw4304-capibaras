# Lista negras de emails
## Índice
1. [Estructura](#estructura)
2. [Despliegue en AWS](#despliegue-en-aws)
3. [Despliegue local](#despliegue-local)
4. [Uso](#uso)
5. [Pruebas](#pruebas)
6. [Autores](#autores)

## Estructura
```
├── models # Contiene los modelos de datos de la aplicación. Estos modelos representan las entidades de la base de datos y su estructura.
│
├── tests # Aquí se encuentran las pruebas unitarias de la aplicación.
│
├── views # Contiene los blueprints, que son colecciones de rutas relacionadas en la aplicación.
│   └── util.py # Archivo que contiene funciones auxiliares utilizadas en las vistas u otros componentes de la aplicación.
│
├── .gitignore # Archivo que especifica los archivos y directorios que se ignoran en el control de versiones Git.
│
├── .coveragerc # Archivo que contiene la configuración de coverage.py, la herramienta para la medición de la cobertura de código
|
├── app.py # Archivo principal de la aplicación.
|
├── db.py # Archivo que contiene el objeto DB de SQLAlchemy para ejecutar queries.
|
├── docker-compose.yml # Archivo de configuración para Docker Compose, que define los servicios y redes del entorno Docker.
|
├── Dockerfile # Archivo que contiene instrucciones para construir la imagen de Docker.
|
├── README.md # Usted está aquí
|
└── requirements.txt # Archivo que especifica las dependencias de Python necesarias para ejecutar la aplicación.
```

## Despliegue en AWS
ToDo

## Despliegue local
### Prerrequisitos
Tener instalado:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Postman](https://www.postman.com/)

### Ejecutar microservicios
1. Ubicarse en la carpeta raíz del repositorio.
2. Crear los contenedores:
```bash
docker compose build
```
3. Ejecutar los microservicios con el comando:
```bash
docker compose up
```

El microservicio se ubica en: http://127.0.0.1:8000/

**Nota**: En un entorno de desarrollo la aplicación también puede correr con una base de datos SQLite sin necesidad de tener una base de datos Postgres corriendo. **Este modo no está soportado oficialmente**.
```bash
flask --app "app:create_app('sqlite:///db.sqlite')" run -p 8000
```

## Uso
ToDo

## Pruebas
Para ejecutar las pruebas ejecuta los siguientes comandos:
```bash
coverage run
coverage report
```

Se puede crear un reporte de cobertura en HTML con
```bash
coverage html
```
El reporte está en la carpeta `htmlcov`.

## Autores
| Nombres       | Apellidos        | Correo                      | Usuario de GitHub | 
|---------------|------------------|-----------------------------|-------------------|
| Camilo        | Ramírez Restrepo | c.ramirezr2@uniandes.edu.co | CamiloRamirezR    |
| Leidy Viviana | Osorio Jimenez   | l.osorioj@uniandes.edu.co   | VivianaOj         |
| Laura Daniela | Molina Villar    | ld.molina11@uniandes.edu.co | Molvilada         |
| Tim Ulf       | Pambor           | t.pambor@uniandes.edu.co    | tpambor           |
