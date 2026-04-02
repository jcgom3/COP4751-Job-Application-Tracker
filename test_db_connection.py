from database import get_connection


def main() -> None:
    """
    Validate that the application can connect to MySQL and reach the expected
    database.

    This script is intentionally small so connectivity can be tested in
    isolation before CRUD logic is introduced.
    """
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        current_db = cursor.fetchone()[0]

        print("Database connection successful.")
        print(f"Connected database: {current_db}")

    except Exception as exc:
        print("Database connection failed.")
        print(f"Error: {exc}")

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print("Connection closed.")


if __name__ == "__main__":
    main()