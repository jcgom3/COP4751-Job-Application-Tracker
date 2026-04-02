from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    """
    Render the landing page for the Job Application Tracker.

    This is intentionally minimal for Milestone 1 so the project can be
    bootstrapped, tested locally, and committed in small increments.
    """
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)