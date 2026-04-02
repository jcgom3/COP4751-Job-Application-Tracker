# Job Application Tracker

## Overview

This project is a full-stack web application designed to help users track and manage job applications across multiple companies. It supports full CRUD operations for companies, jobs, applications, and contacts, and includes a Job Match feature that calculates how closely a user’s skills align with job requirements.

The application is built using MySQL for data storage, Python with Flask for backend logic, and HTML/CSS for the frontend. The system is structured to reflect real-world backend design principles, including modular database access, parameterized queries, and clear separation of concerns.

---

## Current Project Status

This repository is being built incrementally as part of a course project.

### Milestone 1

Currently implemented:

- Local project setup
- Python virtual environment
- Dependency installation
- Initial Flask application bootstrap
- Base template and home page
- Project folder structure
- Initial documentation and AI usage log

Planned next:

- MySQL connection helper
- Database schema creation
- Full CRUD for companies, jobs, applications, and contacts
- Job Match feature
- Final UI polish and demo video

---

## Features

### Core Functionality

- Create, read, update, and delete (CRUD) operations for:

  - Companies
  - Jobs
  - Applications
  - Contacts

- Relational data model using foreign keys
- Clean navigation across all entities

### Job Match Feature

- Accepts user-entered skills
- Compares against job-required skills
- Calculates match percentage
- Displays:

  - Matched skills
  - Missing skills
  - Overall compatibility score

### Backend Design

- Centralized database logic in `database.py`
- Parameterized SQL queries to prevent SQL injection
- Structured Flask routes with clear responsibility boundaries
- Explicit transaction handling with commit and rollback support

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

## Repository

GitHub repository:

```text
https://github.com/jcgom3/COP4751-Job-Application-Tracker.git
```

Local project folder:

```text
COP4751-Job-Application-Tracker
```

---

## Project Structure

```text
COP4751-Job-Application-Tracker/
├── app.py
├── database.py
├── schema.sql
├── requirements.txt
├── README.md
├── AI_USAGE.md
├── .gitignore
├── .env.example
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
└── docs/
    └── screenshots/
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/jcgom3/COP4751-Job-Application-Tracker.git
cd COP4751-Job-Application-Tracker
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate the environment.

Mac/Linux:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a local `.env` file based on `.env.example`.

Example:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=job_tracker
```

### 5. Set Up MySQL Database

Open MySQL Workbench and run:

```sql
CREATE DATABASE job_tracker;
```

Then load the schema:

```sql
USE job_tracker;
SOURCE schema.sql;
```

### 6. Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

---

## Local Development Workflow

Typical workflow for local development:

```bash
source .venv/bin/activate
python app.py
```

When making updates:

```bash
git status
git add .
git commit -m "Your meaningful commit message"
git push
```

---

## Job Match Feature

The Job Match feature evaluates how well a user’s skills align with a job’s required skills.

### Process

1. Job skills are stored in the database
2. User inputs skills through a form
3. The system compares both sets
4. Match percentage is calculated

### Formula

```text
match_percentage = (matched_skills / total_required_skills) * 100
```

### Output

- Percentage match
- Matching skills
- Missing skills

---

## Database Design

The application uses four relational tables:

### companies

Stores company details.

### jobs

Linked to companies via foreign key. Stores job-specific details and required skills.

### applications

Linked to jobs. Tracks application status and progress.

### contacts

Linked to companies. Stores recruiter or contact information.

---

## Code Quality

- Parameterized queries used throughout
- Clean separation of Flask routes and database logic
- Explicit error handling with rollback support
- Consistent naming conventions
- Readable and maintainable structure
- Incremental commits used throughout development

---

## AI Usage

AI tools were used during development to:

- Generate initial code scaffolding
- Debug SQL and Python issues
- Suggest architecture improvements
- Refine UI and project structure

All AI usage is documented in `AI_USAGE.md`, including:

- prompts used
- generated code
- modifications made
- lessons learned

---

## Demo Video

A 3 to 6 minute demonstration video (`demo.mp4`) will be included showing:

- Application startup
- CRUD operations
- Job Match feature
- Database interaction

---

## Important Notes

- Ensure the MySQL server is running before starting the app
- Verify database credentials are correct before testing
- Do not commit sensitive information such as passwords
- The `.env` file should remain local and should not be committed
- Test the application after a fresh clone to ensure setup instructions are accurate

---

## License

This project is licensed under the MIT License.
