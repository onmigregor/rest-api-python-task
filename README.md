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
# Desde la raíz del proyecto
python -m app.migrations.seeders.seed_roles_and_admin

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
uvicorn app.main:app --reload --port 8000
```

### Opciones del Comando

- `--reload`: Recarga automática al detectar cambios
- `--port 8000`: Puerto donde se ejecutará la API

### Verificar que Funciona

- **API**: <http://localhost:8000>
- **Documentación Swagger**: <http://localhost:8000/docs>
- **Documentación ReDoc**: <http://localhost:8000/redoc>

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

- `GET /users/roles` - Obtener roles disponibles

```json
GET /users/roles
{
  "message": "success",
  "data": [
    {"id": 1, "name": "Admin"},
    {"id": 2, "name": "Single user"}
  ]
}
```

- `GET /users/all` - Obtener todos los usuarios del sistema

```json
GET /users/all
{
  "message": "success",
  "data": [
    {
      "id": 1,
      "name": "Admin",
      "email": "admin@mail.com",
      "roles": [{"id": 1, "name": "Admin"}]
    },
    {
      "id": 2,
      "name": "Juan Pérez",
      "email": "juan@example.com",
      "roles": [{"id": 2, "name": "Single user"}]
    }
  ]
}
```

- `GET /users` - Listar usuarios paginados (con roles)
- `GET /users/{id}` - Obtener usuario (con roles)
- `POST /users` - Crear usuario (requiere role_id)
- `PUT /users/{id}` - Actualizar usuario (puede incluir role_id)
- `DELETE /users/{id}` - Eliminar usuario

### Categorías

- `GET /categories` - Listar categorías
- `POST /categories` - Crear categoría
- `PUT /categories/{id}` - Actualizar categoría
- `DELETE /categories/{id}` - Eliminar categoría

### Tareas

- `GET /tasks` - Listar tareas paginadas (con page y limit)
- `POST /tasks` - Crear tarea
- `GET /tasks/{id}` - Obtener tarea
- `PUT /tasks/{id}` - Actualizar tarea
- `DELETE /tasks/{id}` - Eliminar tarea

## 👥 Sistema de Roles y Permisos

### Roles Disponibles

El sistema incluye los siguientes roles predefinidos:

- **Admin**: Acceso completo a todas las funcionalidades
- **Single user**: Acceso limitado a funcionalidades básicas

### Gestión de Roles

#### Crear Usuario con Rol

```json
POST /users
{
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "password": "password123",
  "confirm_pass": "password123",
  "role_id": 1
}
```

#### Obtener Roles Disponibles

```json
GET /users/roles
{
  "message": "success",
  "data": [
    {"id": 1, "name": "Admin"},
    {"id": 2, "name": "Single user"}
  ]
}
```

#### Obtener Todos los Usuarios

```json
GET /users/all
{
  "message": "success",
  "data": [
    {
      "id": 1,
      "name": "Admin",
      "email": "admin@mail.com",
      "roles": [{"id": 1, "name": "Admin"}]
    },
    {
      "id": 2,
      "name": "Juan Pérez",
      "email": "juan@example.com",
      "roles": [{"id": 2, "name": "Single user"}]
    }
  ]
}
```

#### Respuesta de Usuario con Roles

```json
{
  "id": 1,
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "roles": [
    {"id": 1, "name": "Admin"}
  ]
}
```

#### Actualizar Rol de Usuario

```json
PUT /users/{id}
{
  "role_id": 2
}
```

#### Ejemplo de Respuesta Paginada de Tareas

```json
GET /tasks?page=1&limit=10
{
  "message": "success",
  "data": {
    "page": 1,
    "per_page": 10,
    "total_pages": 3,
    "total_items": 25,
    "tasks": [
      {
        "id": 1,
        "title": "Implementar API de usuarios",
        "description": "Crear endpoints CRUD para usuarios",
        "completed": false,
        "due_date": "2024-01-15T10:00:00",
        "priority": "high",
        "category": {
          "id": 1,
          "name": "Desarrollo"
        },
        "created_by": {
          "id": 1,
          "name": "Admin"
        },
        "assigned_to": {
          "id": 2,
          "name": "Juan Pérez"
        },
        "created_at": "2024-01-01T08:00:00",
        "updated_at": "2024-01-01T08:00:00"
      }
    ]
  }
}
```

### Validaciones de Roles

- ✅ **Validación de existencia**: El `role_id` debe existir en la base de datos
- ✅ **Validación de formato**: El `role_id` debe ser un entero positivo
- ✅ **Seguridad**: Solo usuarios Admin pueden gestionar roles
- ✅ **Integridad**: Relación many-to-many entre usuarios y roles

### Estructura de Base de Datos

```sql
-- Tabla de roles
roles (id, name)

-- Tabla de usuarios
users (id, name, email, password, created_at, updated_at, delete_at)

-- Tabla de relación usuario-rol
user_roles (user_id, role_id)
```

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
- **Roles**: Sistema de roles implementado con validación automática
- **Permisos**: Control de acceso basado en roles (RBAC)
- **Base de Datos**: Relaciones many-to-many entre usuarios y roles
- **Endpoints**: `/users/all` para obtener todos los usuarios sin paginación

---

¡Tu API Task Manager está lista para usar! 🎉

Para más información, visita la documentación en: <http://localhost:8000/docs>
