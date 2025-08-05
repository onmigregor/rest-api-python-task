# Task Manager FastAPI

API REST modular para gestión de tareas desarrollada con FastAPI, PostgreSQL y Alembic.

## 📋 Requerimientos para Instalación Local

### Software Necesario
- **Python 3.8+** - Lenguaje de programación
- **PostgreSQL 12+** - Base de datos
- **Git** - Control de versiones
- **pip** - Gestor de paquetes de Python

### Herramientas Recomendadas
- **Visual Studio Code** - Editor de código
- **Postman/Insomnia** - Para probar la API
- **pgAdmin** - Administrador de PostgreSQL

## 🚀 Pasos para Levantar el Proyecto

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd rest-api-python-task
```

### 2. Crear y Activar Entorno Virtual
```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En Windows:
.venv\Scripts\activate

# En Linux/Mac:
source .venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
# POSTGRES_USER=postgres
# POSTGRES_PASSWORD=tu_contraseña
# POSTGRES_DB=taskmanager
# POSTGRES_HOST=localhost
# POSTGRES_PORT=5432
# FRONTEND_URL=http://localhost:3000
```

### 5. Crear Base de Datos
```sql
-- Conectarse a PostgreSQL y ejecutar:
CREATE DATABASE taskmanager;
```

## 🗄️ Configuración de Migraciones y Seeders

### Aplicar Migraciones
```bash
# Ejecutar todas las migraciones
alembic -c app/migrations/alembic.ini upgrade head

# Verificar estado de migraciones
alembic -c app/migrations/alembic.ini current
```

### Ejecutar Seeders
```bash
# Opción 1: Script dedicado (Recomendado)
python run_seeder.py

# Opción 2: Ejecutar directamente
python app/migrations/seeders/seed_roles_and_admin.py
```

### Usuarios Creados por el Seeder
- **Admin**: `admin@mail.com` | Contraseña: `12345678`
- **Usuario**: `user@mail.com` | Contraseña: `123456`

### Comandos Útiles de Migraciones
```bash
# Ver historial de migraciones
alembic -c app/migrations/alembic.ini history

# Crear nueva migración
alembic -c app/migrations/alembic.ini revision --autogenerate -m "descripción"

# Revertir última migración
alembic -c app/migrations/alembic.ini downgrade -1
```

## 🏃‍♂️ Comando para Levantar Proyecto en Desarrollo

### Comando Principal
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Opciones del Comando
- `--reload`: Recarga automática al detectar cambios
- `--host 0.0.0.0`: Permite conexiones desde cualquier IP
- `--port 8000`: Puerto donde se ejecutará la API

### Verificar que Funciona
- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc

## 📁 Estructura General del Proyecto

```
rest-api-python-task/
├── app/                           # Aplicación principal
│   ├── __init__.py
│   ├── main.py                    # Punto de entrada FastAPI
│   │
│   ├── config/                    # Configuraciones
│   │   ├── database.py            # Configuración de BD
│   │   └── route.py               # Configuración de rutas
│   │
│   ├── core/                      # Funcionalidades centrales
│   │   ├── database.py            # Core de base de datos
│   │   └── ExceptionValidator/    # Validadores de excepciones
│   │       └── index.py
│   │
│   ├── common/                    # Utilidades compartidas
│   │   ├── pagination.py          # Paginación
│   │   └── security.py            # Seguridad
│   │
│   ├── migrations/                # Migraciones de Alembic
│   │   ├── alembic.ini            # Configuración Alembic
│   │   ├── env.py                 # Entorno de migraciones
│   │   ├── versions/              # Archivos de migración
│   │   └── seeders/               # Datos iniciales
│   │       └── seed_roles_and_admin.py
│   │
│   └── modules/                   # Módulos de la aplicación
│       ├── auth/                  # Autenticación
│       │   ├── Controller/        # Controladores
│       │   ├── Dependencies/      # Dependencias JWT
│       │   ├── Models/            # Modelos (Role, UserRole, etc.)
│       │   ├── Requests/          # Validaciones de entrada
│       │   ├── Routes/            # Rutas de la API
│       │   └── Service/           # Lógica de negocio
│       │
│       ├── user/                  # Gestión de usuarios
│       │   ├── Controller/        # Controladores de usuario
│       │   ├── Models/            # Modelo User
│       │   ├── Requests/          # Validaciones
│       │   ├── Routes/            # Rutas de usuarios
│       │   ├── Schemas/           # Esquemas de respuesta
│       │   └── Service/           # Servicios de usuario
│       │
│       ├── category/              # Gestión de categorías
│       │   ├── Controller/        # Controladores
│       │   ├── Models/            # Modelo Category
│       │   ├── Requests/          # Validaciones
│       │   ├── Routes/            # Rutas de categorías
│       │   ├── Schemas/           # Esquemas
│       │   └── Service/           # Servicios
│       │
│       └── task/                  # Gestión de tareas
│           ├── Controller/        # Controladores
│           ├── Models/            # Modelo Task
│           ├── Requests/          # Validaciones
│           ├── Resource/          # Recursos de respuesta
│           ├── Routes/            # Rutas de tareas
│           ├── Schemas/           # Esquemas
│           └── Service/           # Servicios
│
├── .env.example                   # Plantilla de variables de entorno
├── .gitignore                     # Archivos ignorados por Git
├── requirements.txt               # Dependencias Python
├── run_seeder.py                  # Script para ejecutar seeders
└── README.md                      # Este archivo
```

## 🔧 Arquitectura del Proyecto

### Patrón de Diseño
- **Arquitectura Modular**: Cada funcionalidad en su propio módulo
- **Separación de Responsabilidades**: Controller → Service → Model
- **Inyección de Dependencias**: Para base de datos y autenticación

### Módulos Principales
- **Auth**: Autenticación JWT, roles y permisos
- **User**: Gestión de usuarios y perfiles
- **Category**: Categorización de tareas
- **Task**: CRUD completo de tareas

## 🛣️ Endpoints Principales

### Autenticación
- `POST /auth/login` - Iniciar sesión
- `POST /auth/register` - Registrar usuario
- `POST /auth/logout` - Cerrar sesión

### Usuarios
- `GET /users` - Listar usuarios
- `GET /users/{id}` - Obtener usuario
- `PUT /users/{id}` - Actualizar usuario
- `DELETE /users/{id}` - Eliminar usuario

### Categorías
- `GET /categories` - Listar categorías
- `POST /categories` - Crear categoría
- `PUT /categories/{id}` - Actualizar categoría
- `DELETE /categories/{id}` - Eliminar categoría

### Tareas
- `GET /tasks` - Listar tareas
- `POST /tasks` - Crear tarea
- `GET /tasks/{id}` - Obtener tarea
- `PUT /tasks/{id}` - Actualizar tarea
- `DELETE /tasks/{id}` - Eliminar tarea

## 🚨 Solución de Problemas

### Error de Conexión a PostgreSQL
```bash
# Verificar que PostgreSQL esté ejecutándose
# Comprobar credenciales en .env
# Verificar que la base de datos existe
```

### Error de Migraciones
```bash
# Resetear migraciones (¡CUIDADO!)
alembic -c app/migrations/alembic.ini stamp base
alembic -c app/migrations/alembic.ini upgrade head
```

### Puerto 8000 Ocupado
```bash
# Usar puerto diferente
uvicorn app.main:app --reload --port 8001
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -am 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## 📝 Notas Importantes

- **Seguridad**: Contraseñas hasheadas con bcrypt
- **CORS**: Configurado para frontend en puerto 3000
- **Validación**: Pydantic para validación de datos
- **Documentación**: Swagger UI automática en `/docs`

---

¡Tu API Task Manager está lista para usar! 🎉

Para más información, visita la documentación en: http://localhost:8000/docs
