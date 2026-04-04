from flask import Flask, redirect, render_template, request, url_for

from database import (
    create_company,
    create_job,
    delete_company,
    delete_job,
    fetch_all_companies,
    fetch_all_jobs,
    fetch_company_by_id,
    fetch_company_options,
    fetch_job_by_id,
    format_skills_for_form,
    get_connection,
    normalize_skills_input,
    update_company,
    update_job,
    create_contact,
    delete_contact,
    fetch_all_contacts,
    fetch_contact_by_id,
    update_contact,
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
    
    
@app.route("/jobs")
def jobs_list():
    """
    Show all jobs.
    """
    jobs = fetch_all_jobs()
    return render_template("jobs/list.html", jobs=jobs)


@app.route("/jobs/<int:job_id>")
def jobs_detail(job_id: int):
    """
    Show a single job detail page.
    """
    job = fetch_job_by_id(job_id)

    if job is None:
        return render_template("404.html"), 404

    return render_template("jobs/detail.html", job=job)


@app.route("/jobs/create", methods=["GET", "POST"])
def jobs_create():
    """
    Render the create form and handle job creation.
    """
    company_options = fetch_company_options()
    error_message = None

    if request.method == "POST":
        company_id_raw = request.form.get("company_id", "").strip()
        job_title = request.form.get("job_title", "").strip()
        salary_min_raw = request.form.get("salary_min", "").strip()
        salary_max_raw = request.form.get("salary_max", "").strip()
        job_type = request.form.get("job_type", "").strip()
        job_description = request.form.get("job_description", "").strip()
        skills_text = request.form.get("skills_text", "").strip()
        date_posted = request.form.get("date_posted", "").strip()

        if not company_id_raw or not job_title:
            error_message = "Company and job title are required."
        else:
            company_id = int(company_id_raw)
            salary_min = float(salary_min_raw) if salary_min_raw else None
            salary_max = float(salary_max_raw) if salary_max_raw else None
            required_skills_json = normalize_skills_input(skills_text)

            new_job_id = create_job(
                company_id=company_id,
                job_title=job_title,
                salary_min=salary_min,
                salary_max=salary_max,
                job_type=job_type,
                job_description=job_description,
                required_skills_json=required_skills_json,
                date_posted=date_posted or None,
            )
            return redirect(url_for("jobs_detail", job_id=new_job_id))

    return render_template(
        "jobs/create.html",
        company_options=company_options,
        error_message=error_message,
    )


@app.route("/jobs/<int:job_id>/edit", methods=["GET", "POST"])
def jobs_edit(job_id: int):
    """
    Render the edit form and handle job updates.
    """
    job = fetch_job_by_id(job_id)
    company_options = fetch_company_options()
    error_message = None

    if job is None:
        return render_template("404.html"), 404

    if request.method == "POST":
        company_id_raw = request.form.get("company_id", "").strip()
        job_title = request.form.get("job_title", "").strip()
        salary_min_raw = request.form.get("salary_min", "").strip()
        salary_max_raw = request.form.get("salary_max", "").strip()
        job_type = request.form.get("job_type", "").strip()
        job_description = request.form.get("job_description", "").strip()
        skills_text = request.form.get("skills_text", "").strip()
        date_posted = request.form.get("date_posted", "").strip()

        if not company_id_raw or not job_title:
            error_message = "Company and job title are required."
        else:
            company_id = int(company_id_raw)
            salary_min = float(salary_min_raw) if salary_min_raw else None
            salary_max = float(salary_max_raw) if salary_max_raw else None
            required_skills_json = normalize_skills_input(skills_text)

            update_job(
                job_id=job_id,
                company_id=company_id,
                job_title=job_title,
                salary_min=salary_min,
                salary_max=salary_max,
                job_type=job_type,
                job_description=job_description,
                required_skills_json=required_skills_json,
                date_posted=date_posted or None,
            )
            return redirect(url_for("jobs_detail", job_id=job_id))

    job["skills_text"] = format_skills_for_form(job.get("required_skills_json"))

    return render_template(
        "jobs/edit.html",
        job=job,
        company_options=company_options,
        error_message=error_message,
    )


@app.route("/jobs/<int:job_id>/delete", methods=["POST"])
def jobs_delete(job_id: int):
    """
    Delete a job and return to the jobs list page.
    """
    delete_job(job_id)
    return redirect(url_for("jobs_list"))




@app.route("/contacts")
def contacts_list():
    """
    Show all contacts.
    """
    contacts = fetch_all_contacts()
    return render_template("contacts/list.html", contacts=contacts)


@app.route("/contacts/<int:contact_id>")
def contacts_detail(contact_id: int):
    """
    Show a single contact detail page.
    """
    contact = fetch_contact_by_id(contact_id)

    if contact is None:
        return render_template("404.html"), 404

    return render_template("contacts/detail.html", contact=contact)


@app.route("/contacts/create", methods=["GET", "POST"])
def contacts_create():
    """
    Render the create form and handle contact creation.
    """
    company_options = fetch_company_options()
    error_message = None

    if request.method == "POST":
        company_id_raw = request.form.get("company_id", "").strip()
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        job_title = request.form.get("job_title", "").strip()
        notes = request.form.get("notes", "").strip()

        if not company_id_raw or not first_name or not last_name:
            error_message = "Company, first name, and last name are required."
        else:
            new_contact_id = create_contact(
                company_id=int(company_id_raw),
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                job_title=job_title,
                notes=notes,
            )
            return redirect(url_for("contacts_detail", contact_id=new_contact_id))

    return render_template(
        "contacts/create.html",
        company_options=company_options,
        error_message=error_message,
    )


@app.route("/contacts/<int:contact_id>/edit", methods=["GET", "POST"])
def contacts_edit(contact_id: int):
    """
    Render the edit form and handle updates for an existing contact.
    """
    contact = fetch_contact_by_id(contact_id)
    company_options = fetch_company_options()
    error_message = None

    if contact is None:
        return render_template("404.html"), 404

    if request.method == "POST":
        company_id_raw = request.form.get("company_id", "").strip()
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        job_title = request.form.get("job_title", "").strip()
        notes = request.form.get("notes", "").strip()

        if not company_id_raw or not first_name or not last_name:
            error_message = "Company, first name, and last name are required."
        else:
            update_contact(
                contact_id=contact_id,
                company_id=int(company_id_raw),
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                job_title=job_title,
                notes=notes,
            )
            return redirect(url_for("contacts_detail", contact_id=contact_id))

    return render_template(
        "contacts/edit.html",
        contact=contact,
        company_options=company_options,
        error_message=error_message,
    )


@app.route("/contacts/<int:contact_id>/delete", methods=["POST"])
def contacts_delete(contact_id: int):
    """
    Delete a contact and return to the list page.
    """
    delete_contact(contact_id)
    return redirect(url_for("contacts_list"))