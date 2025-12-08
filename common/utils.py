from sqlalchemy import inspect
from common.db import engine

def get_schema_info():
    inspector = inspect(engine)
    schema = {}
    for table_name in inspector.get_table_names():
        columns = [col["name"] for col in inspector.get_columns(table_name)]
        schema[table_name] = columns
    return schema
