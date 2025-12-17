# Tienda de Pods (Flask + MySQL)

Esta es una aplicación web simple construida con Flask (Python) y gestionada a través de Docker Compose.

## Ejecución del Proyecto

Sigue estos pasos para levantar la aplicación:

### 1. Construir y Levantar los Contenedores

Desde la raíz del proyecto (donde se encuentra `docker-compose.yml`), ejecuta el siguiente comando:

```bash
docker-compose up --build -d
```

Este comando realizará lo siguiente:
1.  Construirá la imagen de la aplicación web (`web`).
2.  Creará y levantará el contenedor de la base de datos (`db`), inicializándola con el script `tablas.sql`.
3.  Creará y levantará el contenedor de la aplicación Flask (`web`), esperando a que la base de datos esté lista.

### 2. Acceder a la Aplicación

Una vez que los contenedores estén en funcionamiento (puede tardar unos segundos mientras MySQL se inicializa), la aplicación estará accesible en tu navegador.

**URL de Acceso:**

```
http://localhost:5000
```

La aplicación te redirigirá automáticamente a la página de inicio de sesión (`/login`), favor cree un usuario para ingresar.