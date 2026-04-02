from flask import Flask, redirect, render_template, request, url_for

from database import (
    create_company,
    delete_company,
    fetch_all_companies,
    fetch_company_by_id,
    get_connection,
    update_company,
)

app = Flask(__name__)


@app.route("/")
def index():
    """
    Render the application landing page.
    """
    return render_template("index.html")


@app.route("/health")
def health_check():
    """
    Confirm that the Flask app is running and can reach the database.
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


@app.route("/companies")
def companies_list():
    """
    Show all companies.
    """
    companies = fetch_all_companies()
    return render_template("companies/list.html", companies=companies)


@app.route("/companies/<int:company_id>")
def companies_detail(company_id: int):
    """
    Show a single company detail page.
    """
    company = fetch_company_by_id(company_id)

    if company is None:
        return render_template("404.html"), 404

    return render_template("companies/detail.html", company=company)


@app.route("/companies/create", methods=["GET", "POST"])
def companies_create():
    """
    Render the create form and handle company creation.

    Basic validation is intentionally explicit here so the application behavior
    is easy to demo and easy to extend later.
    """
    error_message = None

    if request.method == "POST":
        company_name = request.form.get("company_name", "").strip()
        industry = request.form.get("industry", "").strip()
        city = request.form.get("city", "").strip()
        state = request.form.get("state", "").strip()
        notes = request.form.get("notes", "").strip()

        if not company_name:
            error_message = "Company name is required."
        else:
            new_company_id = create_company(
                company_name=company_name,
                industry=industry,
                city=city,
                state=state,
                notes=notes,
            )
            return redirect(url_for("companies_detail", company_id=new_company_id))

    return render_template("companies/create.html", error_message=error_message)


@app.route("/companies/<int:company_id>/edit", methods=["GET", "POST"])
def companies_edit(company_id: int):
    """
    Render the edit form and handle updates for an existing company.
    """
    company = fetch_company_by_id(company_id)
    error_message = None

    if company is None:
        return render_template("404.html"), 404

    if request.method == "POST":
        company_name = request.form.get("company_name", "").strip()
        industry = request.form.get("industry", "").strip()
        city = request.form.get("city", "").strip()
        state = request.form.get("state", "").strip()
        notes = request.form.get("notes", "").strip()

        if not company_name:
            error_message = "Company name is required."
        else:
            update_company(
                company_id=company_id,
                company_name=company_name,
                industry=industry,
                city=city,
                state=state,
                notes=notes,
            )
            return redirect(url_for("companies_detail", company_id=company_id))

    return render_template(
        "companies/edit.html",
        company=company,
        error_message=error_message,
    )


@app.route("/companies/<int:company_id>/delete", methods=["POST"])
def companies_delete(company_id: int):
    """
    Delete a company and return to the list page.
    """
    delete_company(company_id)
    return redirect(url_for("companies_list"))


if __name__ == "__main__":
    app.run(debug=True)