from flask import Flask, render_template

from database import get_connection

app = Flask(__name__)


@app.route("/")
def index():
    """
    Render the landing page for the Job Application Tracker.
    """
    return render_template("index.html")


@app.route("/health")
def health_check():
    """
    Basic application health check.

    Confirms that the Flask server is running and that the application can
    establish a database connection successfully.
    """
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1;")
        cursor.fetchone()
        return {
            "status": "ok",
            "app": "running",
            "database": "connected",
        }, 200
    except Exception as exc:
        return {
            "status": "error",
            "app": "running",
            "database": "disconnected",
            "details": str(exc),
        }, 500
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    app.run(debug=True)