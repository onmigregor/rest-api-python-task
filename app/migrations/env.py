import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Permitir imports relativos desde el proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.config.database import Base
from app.modules.user.Models.user import User
from app.modules.category.Models.category import Category
# Agrega aquí otros modelos:
# from app.modules.task.Models.task import Task

# Configuración Alembic
config = context.config

# Construir URL de base de datos desde variables de entorno
def get_database_url():
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "123456")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB", "taskmanager")
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"

# Establecer la URL de la base de datos
config.set_main_option("sqlalchemy.url", get_database_url())

fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
