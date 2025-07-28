import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from sqlalchemy import Table, Column, Integer, String, MetaData
from app.config.database import engine

metadata = MetaData()

from sqlalchemy import DateTime, func

user_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
    Column("email", String(100), unique=True, nullable=False),  
    Column("password", String(128), nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
    Column("updated_at", DateTime, nullable=False, server_default=func.now(), onupdate=func.now()),
    Column("delete_at", DateTime, nullable=True)
)

if __name__ == "__main__":
    metadata.create_all(engine)
    print("Tabla users creada correctamente.")
