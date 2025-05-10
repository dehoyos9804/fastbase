# FastBase - Backend Base ⚡️ con FastAPI

> Este repositorio sigue el estándar [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/). Por lo tanto, los mensajes de commit deben seguir el formato especificado. De lo contrario, serán rechazados.

## 📌 Descripción

**FastBase** es un **backend base** construido con [**FastAPI**](https://fastapi.tiangolo.com/), optimizado para un desarrollo ágil y eficiente. Su objetivo es permitir a los desarrolladores enfocarse únicamente en la **lógica de negocio**, sin preocuparse por la configuración base del proyecto.

Este sistema cuenta con:
- Estructura modular y mantenible.
- Modelos genéricos usando [**SQLModel**](https://sqlmodel.tiangolo.com/).
- Seguridad integrada con [**SecMec**](https://github.com/your-org/sec-mec) 🔐.
- Backend listo para producción con solo unas pocas líneas de código.

![FastAPI](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)

## ⚙️ Requisitos

- [**Python**](https://www.python.org/downloads/) 3.12.x o superior
- [**virtualenv**](https://virtualenv.pypa.io/en/stable/) (Recomendado)

## 📥 Instalación

Clona este repositorio y ubícalo en un directorio conveniente:

```sh
git clone <url.git.del.fastbase>
```

Se recomienda usar [**virtualenv**](https://virtualenv.pypa.io/en/stable/) para el desarrollo y pruebas.

### 🔧 Activar virtualenv en GNU/Linux y macOS

```sh
$ virtualenv --python python3 env
$ source env/bin/activate
```

### 🖥️ Activar virtualenv en Windows

```sh
python -m venv env
env\Scripts\activate
```

### 📄 Instala las dependencias del proyecto:
```sh
pip install -r requirements.txt
```

## 🚀 Ejecución del Servidor

Inicia el servidor localmente:

```sh
uvicorn main:app --reload
```

Accede a la documentación automática en:

- [**Swagger UI**](http://localhost:8000/api/docs)
- [**Swagger UI**](http://localhost:8000/api/redocs)

## 🛡 Seguridad Integrada con SecMec

FastBase incluye mecanismos de seguridad listos para usarse, como:

- Autenticación basada en JWT
- Validaciones personalizadas
- Módulos de autorización

Estos se gestionan fácilmente desde un sistema de configuración flexible y seguro.

## 📄 Documentación  

🔹 Encuentra toda la información detallada en el siguiente enlace: [Por aquí](https://wiki-fastbase-5a098d.gitlab.io/) 📌  

Si tienes dudas, revisa la documentación para obtener una guía completa. 🚀 

## 🔁 Flujo de Trabajo (Git Workflow)

El flujo de trabajo sigue la metodología **Git Flow** con las siguientes ramas:

- `main` - Contiene la versión estable del proyecto.
- `dev` - Contiene la última versión en desarrollo.
- `feature/**` - Para nuevas funcionalidades.
- `hotfix/**` - Para corrección de errores en producción.

### 📌 Tipos de commits (Conventional Commits)

- 🔧 `feat`: para añadir nuevas funcionalidades
- 🐞 `fix`: para corregir errores en el código
- 📚 `docs`: Para cambios en la documentación
- 🎨 `style`: Para cambios que no afectan la lógica del código (espacios en blanco, formatos, etc)
- 🛠️ `refactor`: Para mejorar el código sin corregir errores ni añadir nuevas funcionalidades
- 🧪 `test`: Para agregar o modificar pruebas
- 🧹 `chore`: Para tareas de mantenimiento y configuración que no afecta el código fuente ni las pruebas
- ⚡ `perf`:Para mejorar el rendimiento.

## 🧪 Pruebas con Pytest

Instala las dependencias de pruebas:

```sh
pip install pytest httpx
```

Ejecuta las pruebas:

```sh
pytest -s
```

Para correr pruebas individuales:

```sh
pytest -s tests/test_model.py::test_function
```
