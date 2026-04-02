import os
from typing import Any

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


def get_db_config() -> dict[str, Any]:
    """
    Build and return the database connection configuration from environment
    variables.

    Centralizing config creation keeps connection logic consistent and avoids
    hard-coding secrets in source-controlled files.
    """
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "job_tracker"),
    }


def get_connection():
    """
    Create and return a new MySQL connection.

    A dedicated helper makes future route handlers and data-access functions
    simpler and ensures all code paths use the same connection settings.
    """
    config = get_db_config()
    return mysql.connector.connect(**config)