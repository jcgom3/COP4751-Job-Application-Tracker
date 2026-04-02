import os
from typing import Any

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


def get_db_config() -> dict[str, Any]:
    """
    Build database connection configuration from environment variables.

    Keeping configuration in one place avoids duplicating connection settings
    and keeps secrets out of source-controlled files.
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
    """
    return mysql.connector.connect(**get_db_config())


def fetch_all_companies() -> list[dict[str, Any]]:
    """
    Return all companies ordered alphabetically.

    Dictionary cursors make templates and route handlers easier to read because
    fields can be accessed by column name instead of tuple position.
    """
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                company_id,
                company_name,
                industry,
                city,
                state,
                notes,
                created_at
            FROM companies
            ORDER BY company_name ASC
            """
        )
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def fetch_company_by_id(company_id: int) -> dict[str, Any] | None:
    """
    Return a single company by ID, or None if the company does not exist.
    """
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                company_id,
                company_name,
                industry,
                city,
                state,
                notes,
                created_at
            FROM companies
            WHERE company_id = %s
            """,
            (company_id,),
        )
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def create_company(
    company_name: str,
    industry: str,
    city: str,
    state: str,
    notes: str,
) -> int:
    """
    Insert a new company and return the new company ID.
    """
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO companies (company_name, industry, city, state, notes)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (company_name, industry, city, state, notes),
        )
        connection.commit()
        return cursor.lastrowid
    except Exception:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def update_company(
    company_id: int,
    company_name: str,
    industry: str,
    city: str,
    state: str,
    notes: str,
) -> None:
    """
    Update an existing company.

    All editable fields are updated explicitly so the application behavior stays
    predictable and easy to reason about.
    """
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE companies
            SET
                company_name = %s,
                industry = %s,
                city = %s,
                state = %s,
                notes = %s
            WHERE company_id = %s
            """,
            (company_name, industry, city, state, notes, company_id),
        )
        connection.commit()
    except Exception:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def delete_company(company_id: int) -> None:
    """
    Delete a company by ID.

    Because the schema uses ON DELETE CASCADE, related child rows are also
    removed automatically when appropriate.
    """
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM companies WHERE company_id = %s",
            (company_id,),
        )
        connection.commit()
    except Exception:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()