DROP DATABASE IF EXISTS job_tracker;
CREATE DATABASE job_tracker;
USE job_tracker;

CREATE TABLE companies (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(150) NOT NULL,
    industry VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE jobs (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    job_title VARCHAR(150) NOT NULL,
    salary_min DECIMAL(10, 2),
    salary_max DECIMAL(10, 2),
    job_type VARCHAR(50),
    job_description TEXT,
    required_skills_json JSON,
    date_posted DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_jobs_company
        FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
        ON DELETE CASCADE
);

CREATE TABLE applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    application_date DATE,
    status VARCHAR(100) NOT NULL,
    resume_version VARCHAR(50),
    cover_letter_sent BOOLEAN DEFAULT FALSE,
    interview_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_applications_job
        FOREIGN KEY (job_id)
        REFERENCES jobs(job_id)
        ON DELETE CASCADE
);

CREATE TABLE contacts (
    contact_id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    phone VARCHAR(30),
    job_title VARCHAR(150),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_contacts_company
        FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
        ON DELETE CASCADE
);



INSERT INTO companies (company_name, industry, city, state, notes)
VALUES
('TechNova', 'Technology', 'Orlando', 'FL', 'Applied for multiple engineering roles.'),
('HealthBridge', 'Healthcare', 'Tampa', 'FL', 'Strong alignment with healthcare background.'),
('CloudAxis', 'Software', 'Austin', 'TX', 'Interesting backend-focused opportunities.');

INSERT INTO jobs (company_id, job_title, salary_min, salary_max, job_type, job_description, required_skills_json, date_posted)
VALUES
(
    1,
    'Backend Software Engineer',
    110000.00,
    145000.00,
    'Full-time',
    'Build and maintain backend services and APIs.',
    JSON_ARRAY('python', 'flask', 'mysql', 'sql', 'git'),
    '2026-04-01'
),
(
    2,
    'Full Stack Engineer',
    100000.00,
    135000.00,
    'Full-time',
    'Work across frontend and backend systems.',
    JSON_ARRAY('python', 'javascript', 'html', 'css', 'mysql'),
    '2026-04-01'
),
(
    3,
    'Data Engineer',
    115000.00,
    150000.00,
    'Full-time',
    'Design data pipelines and platform integrations.',
    JSON_ARRAY('python', 'sql', 'etl', 'mysql', 'aws'),
    '2026-04-01'
);

INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent, interview_date, notes)
VALUES
(1, '2026-04-01', 'Applied', 'v1.0', TRUE, NULL, 'Initial application submitted.'),
(2, '2026-04-02', 'Interview Scheduled', 'v1.1', TRUE, '2026-04-10', 'Phone screen scheduled.'),
(3, '2026-04-03', 'Applied', 'v1.2', FALSE, NULL, 'Need to tailor follow-up.');

INSERT INTO contacts (company_id, first_name, last_name, email, phone, job_title, notes)
VALUES
(1, 'Jordan', 'Lee', 'jordan.lee@technova.com', '555-111-2222', 'Engineering Manager', 'Primary hiring contact.'),
(2, 'Maya', 'Patel', 'maya.patel@healthbridge.com', '555-333-4444', 'Recruiter', 'Reached out after application.'),
(3, 'Andre', 'Kim', 'andre.kim@cloudaxis.com', '555-555-6666', 'Director of Data', 'Potential referral path.');