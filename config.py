from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime
# Configuration for Google Cloud Storage 
BUCKET_NAME = 'challenge-bucket-gb'
PROJECT_ID = '494564794094'

SECRET_ID = "bucket-secret"
VERSION = "1"

# Configuration for Google Cloud SQL
DB_USER = 'root'
DB_PASSWORD = 'db_passwd'
DB_NAME = 'challenge-db'

DEPARTMENTS_PATH = 'departments/departments.csv'
EMPLOYEES_PATH = 'employees/hired_employees.csv'
JOBS_PATH = 'jobs/jobs.csv'

REQUIEREMENT1_QUERY = "SELECT department, job, SUM(CASE WHEN quarter = 'Q1' THEN employees_hired ELSE 0 END) AS Q1, SUM(CASE WHEN quarter = 'Q2' THEN employees_hired ELSE 0 END) AS Q2, SUM(CASE WHEN quarter = 'Q3' THEN employees_hired ELSE 0 END) AS Q3, SUM(CASE WHEN quarter = 'Q4' THEN employees_hired ELSE 0 END) AS Q4 FROM (SELECT d.department AS department, j.job AS job, COUNT(e.id) AS employees_hired, CASE WHEN MONTH(e.datetime) BETWEEN 1 AND 3 THEN 'Q1' WHEN MONTH(e.datetime) BETWEEN 4 AND 6 THEN 'Q2' WHEN MONTH(e.datetime) BETWEEN 7 AND 9 THEN 'Q3' WHEN MONTH(e.datetime) BETWEEN 10 AND 12 THEN 'Q4' END AS quarter FROM employees e INNER JOIN departments d ON e.department_id = d.id INNER JOIN jobs j ON e.job_id = j.id WHERE YEAR(e.datetime) = 2021 GROUP BY department, job, quarter) AS subquery GROUP BY department, job ORDER BY department, job"
REQUIEREMENT2_QUERY = "WITH DepartmentHires AS (SELECT d.id AS department_id, d.department AS department, COUNT(e.id) AS employees_hired FROM employees e INNER JOIN departments d ON e.department_id = d.id WHERE YEAR(e.datetime) = 2021 GROUP BY department_id, department), DepartmentMean AS (SELECT AVG(employees_hired) AS mean_hires FROM DepartmentHires) SELECT dh.department_id, dh.department, dh.employees_hired FROM DepartmentHires dh CROSS JOIN DepartmentMean WHERE dh.employees_hired > DepartmentMean.mean_hires ORDER BY dh.employees_hired DESC"

EMPLOYEES_SCHEMA = Table(
    'employees',
    MetaData(),
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('datetime', DateTime),
    Column('department_id', Integer),
    Column('job_id', Integer)
)

DEPARTMENTS_SCHEMA = Table(
    'departments',
    MetaData(),
    Column('id', Integer, primary_key=True),
    Column('department', String)
)

JOBS_SCHEMA = Table(
    'jobs',
    MetaData(),
    Column('id', Integer, primary_key=True),
    Column('job', String)
)