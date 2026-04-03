import os
from typing import Any, Dict, List, Optional

import mysql.connector
from dotenv import load_dotenv

import json


load_dotenv()


def get_db_config() -> Dict[str, Any]:
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


def fetch_all_companies() -> List[Dict[str, Any]]:
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


def fetch_company_by_id(company_id: int) -> Optional[Dict[str, Any]]:
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
            
            
def fetch_all_jobs() -> List[Dict[str, Any]]:
    """
    Return all jobs with their parent company names.

    Joining to companies makes the job list immediately useful in the UI and
    avoids forcing templates to perform lookup logic.
    """
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                j.job_id,
                j.company_id,
                c.company_name,
                j.job_title,
                j.salary_min,
                j.salary_max,
                j.job_type,
                j.job_description,
                j.required_skills_json,
                j.date_posted,
                j.created_at
            FROM jobs j
            INNER JOIN companies c
                ON j.company_id = c.company_id
            ORDER BY j.created_at DESC, j.job_title ASC
            """
        )
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def fetch_job_by_id(job_id: int) -> Optional[Dict[str, Any]]:
    """
    Return a single job with parent company information.
    """
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                j.job_id,
                j.company_id,
                c.company_name,
                j.job_title,
                j.salary_min,
                j.salary_max,
                j.job_type,
                j.job_description,
                j.required_skills_json,
                j.date_posted,
                j.created_at
            FROM jobs j
            INNER JOIN companies c
                ON j.company_id = c.company_id
            WHERE j.job_id = %s
            """,
            (job_id,),
        )
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def fetch_company_options() -> List[Dict[str, Any]]:
    """
    Return a lightweight company list for dropdown selections in forms.
    """
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT company_id, company_name
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


def create_job(
    company_id: int,
    job_title: str,
    salary_min: Optional[float],
    salary_max: Optional[float],
    job_type: str,
    job_description: str,
    required_skills_json: str,
    date_posted: str,
) -> int:
    """
    Insert a new job and return its ID.

    Skills are stored in the database as JSON text so they can later support
    the job-match feature without requiring schema changes.
    """
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO jobs (
                company_id,
                job_title,
                salary_min,
                salary_max,
                job_type,
                job_description,
                required_skills_json,
                date_posted
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                company_id,
                job_title,
                salary_min,
                salary_max,
                job_type,
                job_description,
                required_skills_json,
                date_posted,
            ),
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


def update_job(
    job_id: int,
    company_id: int,
    job_title: str,
    salary_min: Optional[float],
    salary_max: Optional[float],
    job_type: str,
    job_description: str,
    required_skills_json: str,
    date_posted: str,
) -> None:
    """
    Update an existing job.
    """
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE jobs
            SET
                company_id = %s,
                job_title = %s,
                salary_min = %s,
                salary_max = %s,
                job_type = %s,
                job_description = %s,
                required_skills_json = %s,
                date_posted = %s
            WHERE job_id = %s
            """,
            (
                company_id,
                job_title,
                salary_min,
                salary_max,
                job_type,
                job_description,
                required_skills_json,
                date_posted,
                job_id,
            ),
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


def delete_job(job_id: int) -> None:
    """
    Delete a job by ID.
    """
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM jobs WHERE job_id = %s", (job_id,))
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


def normalize_skills_input(skills_text: str) -> str:
    """
    Convert a comma-separated skills string into normalized JSON text.

    This keeps the create/edit forms simple while still storing structured data
    in the database for downstream job-match calculations.
    """
    skills = [
        skill.strip().lower()
        for skill in skills_text.split(",")
        if skill.strip()
    ]
    return json.dumps(skills)


def format_skills_for_form(required_skills_json: Any) -> str:
    """
    Convert stored JSON skills into a comma-separated string for form editing.
    """
    if not required_skills_json:
        return ""

    if isinstance(required_skills_json, list):
        return ", ".join(required_skills_json)

    try:
        parsed = json.loads(required_skills_json)
        if isinstance(parsed, list):
            return ", ".join(parsed)
    except Exception:
        pass

    return str(required_skills_json)