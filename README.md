# Job Application Tracker

## Overview

This project is a full-stack web application designed to help users track and manage job applications across multiple companies. It supports full CRUD operations for companies, jobs, applications, and contacts, and includes a Job Match feature that calculates how closely a user’s skills align with job requirements.

The application is built using MySQL for data storage, Python with Flask for backend logic, and HTML/CSS for the frontend. The system is structured to reflect real-world backend design principles, including modular database access, parameterized queries, and clear separation of concerns.

---

## Features

### Core Functionality

* Create, read, update, and delete (CRUD) operations for:

  * Companies
  * Jobs
  * Applications
  * Contacts
* Relational data model using foreign keys
* Clean navigation across all entities

### Job Match Feature

* Accepts user-entered skills
* Compares against job-required skills
* Calculates match percentage
* Displays:

  * Matched skills
  * Missing skills
  * Overall compatibility score

### Backend Design

* Centralized database logic in `database.py`
* Parameterized SQL queries to prevent SQL injection
* Structured Flask routes with clear responsibility boundaries
* Explicit transaction handling (commit / rollback)

---

## Tech Stack

| Layer      | Technology                          |
| ---------- | ----------------------------------- |
| Backend    | Python 3, Flask                     |
| Database   | MySQL                               |
| Frontend   | HTML, CSS                           |
| DB Driver  | mysql-connector-python              |
| Versioning | Git, GitHub                         |
| AI Tools   | ChatGPT (documented in AI_USAGE.md) |

---

## Project Structure

```
job-application-tracker/
├── app.py
├── database.py
├── schema.sql
├── requirements.txt
├── README.md
├── AI_USAGE.md
├── .gitignore
├── LICENSE
├── demo.mp4
├── static/
│   └── css/
│       └── styles.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── companies/
│   ├── jobs/
│   ├── applications/
│   ├── contacts/
│   └── match/
```

---

## Setup Instructions

### 1. Clone Repository

```
git clone <your-repo-url>
cd job-application-tracker
```

---

### 2. Create Virtual Environment

```
python -m venv .venv
```

Activate environment:

Mac/Linux:

```
source .venv/bin/activate
```

Windows:

```
.\.venv\Scripts\Activate.ps1
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Set Up MySQL Database

Open MySQL Workbench and run:

```
CREATE DATABASE job_tracker;
```

Then load schema:

```
USE job_tracker;
SOURCE schema.sql;
```

---

### 5. Configure Database Connection

Edit `database.py`:

```
config = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_PASSWORD",
    "database": "job_tracker"
}
```

---

### 6. Run Application

```
python app.py
```

Open browser:

```
http://127.0.0.1:5000/
```

---

## Job Match Feature

The Job Match feature evaluates how well a user’s skills align with a job’s required skills.

### Process

1. Job skills are stored in the database
2. User inputs skills through a form
3. System compares both sets
4. Match percentage is calculated

### Formula

```
match_percentage = (matched_skills / total_required_skills) * 100
```

### Output

* Percentage match
* Matching skills
* Missing skills

---

## Database Design

The application uses four relational tables:

### companies

Stores company details

### jobs

Linked to companies via foreign key
Stores job-specific details and required skills

### applications

Linked to jobs
Tracks application status and progress

### contacts

Linked to companies
Stores recruiter or contact information

---

## Code Quality

* Parameterized queries used throughout
* Clean separation of Flask routes and database logic
* Explicit error handling with rollback support
* Consistent naming conventions
* Readable and maintainable structure

---

## AI Usage

AI tools were used during development to:

* Generate initial code scaffolding
* Debug SQL and Python issues
* Suggest architecture improvements
* Refine UI and project structure

All AI usage is documented in `AI_USAGE.md`, including:

* prompts used
* generated code
* modifications made
* lessons learned

---

## Demo Video

A 3–6 minute demonstration video (`demo.mp4`) is included showing:

* Application startup
* CRUD operations
* Job Match feature
* Database interaction

---

## Important Notes

* Ensure MySQL server is running before starting the app
* Verify database credentials are correct
* Do not commit sensitive information such as passwords
* Test application after cloning to ensure full functionality

---

## License

This project is licensed under the MIT License.
