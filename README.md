# Extracting User Hashes via MySQL UNION-Based Injection Without Column Names

Exploit a real-world inspired SQL injection scenario where you must extract sensitive data from a MySQL database without knowledge of the table's column names, leveraging UNION-based attacks and column indexing.

## Overview

This lab simulates a realistic business environment where you need to extract sensitive information from a database using SQL injection techniques. The challenge focuses on UNION-based SQL injection with the added complexity of obfuscated column names, requiring you to use column indexing rather than relying on known schema information.

## Objectives

- Understand UNION-based SQL injection fundamentals
- Determine the number of columns in a query
- Extract sensitive data using column indexes
- Avoid reliance on known schema or column names

## Difficulty

**Intermediate**

## Estimated Time

1-2 hours

## Prerequisites

- Basic understanding of SQL and web app security
- Familiarity with SQL injection techniques
- Experience with tools like Burp Suite or sqlmap

## Skills Learned

- Detecting and exploiting union-based SQLi
- Column index enumeration and data extraction
- Schema-agnostic data exfiltration in MySQL

## Project Structure

```
├── build/                 # Main application source code
├── deploy/               # Docker deployment files
├── test/                 # Automated tests
├── docs/                 # Documentation
├── README.md            # This file
└── .gitignore           # Git ignore file
```

## Quick Start

### Prerequisites

Docker and Docker Compose installed on your system.

### Installation

1. Clone the repository
2. Run `docker-compose up` in the project folder
3. Access the web application at http://localhost:3206

### Running the Application

```bash
# Start the application
docker-compose up -d

# Check if services are running
docker-compose ps

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Running Tests

```bash
# Install test dependencies
pip install -r test/requirements.txt

# Run all tests
pytest test/test_app.py -v

# Run specific test class
pytest test/test_app.py::TestFinTrackApp -v

# Run vulnerability tests
pytest test/test_app.py::TestSQLInjectionVulnerability -v
```

## Business Context

FinTrack is a mid-sized SaaS provider offering a web-based finance tracker for startups. Their dashboard allows users to search for team members. The application is built internally and uses MySQL as the backend database.

## Technical Setup

The application stack consists of:
- **Frontend**: Flask web application with TailwindCSS
- **Backend**: Python 3.11 with Flask framework
- **Database**: MySQL 5.7 with obfuscated column names
- **Containerization**: Docker and Docker Compose

## Vulnerability Details

The target endpoint is vulnerable to Union-based SQL injection due to unsanitized user input in a GET parameter. Table and column names are obfuscated, but the table structure is based on common templates (users, accounts). Only numeric IDs or indexed references are returned in results; errors are generic.

## Discovery Context

During routine pentesting, the search parameter was fuzzed with single quotes and differential responses were observed. Union-based injection seemed possible, but error-based and Boolean-based techniques revealed little due to error suppression and generic error messages. Brute-forcing table and column names failed as columns are renamed to randomized strings on each deployment. The solution was to guess the number of columns and then extract data by index without knowing column names.

## Challenge Walkthrough

### Step 1: Vulnerability Detection
- Test the search parameter with single quotes
- Observe application responses for SQL injection indicators
- Confirm UNION-based injection is possible

### Step 2: Column Count Enumeration
- Systematically test UNION SELECT with increasing column counts
- Identify the correct number of columns needed for successful injection
- Use payloads like `' UNION SELECT 1--`, `' UNION SELECT 1,2--`, etc.

### Step 3: Data Extraction
- Use column positions to extract sensitive data
- Target the admin user's password hash
- Leverage column indexing: `' UNION SELECT 1,2,3,password_hash,5,6,7 FROM users WHERE username='admin'--`

### Step 4: Verification
- Confirm extracted data appears in the application response
- Map column indexes to visible output fields
- Validate the extracted hash format

## Success Criteria

Successfully extract the 'admin' user's password hash from the users table using only column index in a UNION SELECT injection, without knowing or referencing actual column names.

## Issue Tracker

For issues and questions: https://github.com/FinTrackCTFLabs/extract_data_without_columns_name/issues

## License

This project is for educational purposes only. Use responsibly and only on systems you own or have explicit permission to test. 