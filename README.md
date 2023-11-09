# REST_API

# Solution Overview:

## 1. CSV Data Ingestion:

  - The Flask application includes endpoints to receive historical data from CSV files.
  - The CSV files are stored in a Google Cloud Storage bucket.

## 2. Database

  - The destination database is a MySQL database.
  - A schema is created in the database to match the data structure defined in the CSV files (departments, jobs, employees).

## 3. CSV Data Migration

  - The CSV files (hired_employees.csv, departments.csv, jobs.csv) are uploaded from Google Cloud Storage to Google Cloud SQL.

## 4. API Endpoints:

  - The API exposes several endpoints to perform various tasks, including the following:
    - Endpoints to receive and upload CSV files.
    - Endpoints to query the database to retrieve specific metrics (number of employees hired for each job and department in 2021 divided by quarter, list of departments hiring more employees than the mean for all departments in 2021).

## 5. Google Cloud Integration:

  - A Google Cloud service key is used to access the Google Cloud services.
  - This service key is used to authenticate with Google Cloud services for necessary operations like (read from Secret Manager, CLoud Storage and write to Cloud SQL).

## 6. Cloud Deployment:

  - Components like SQL database, Blob Storage, Secret Manager are hosted in a Google Cloud Platform.

## 7. Testing:

  - Tests are added to the Flask API using testing libraries (unittest).

## 8. Containerization:

  - The Flask application is containerized using Docker. A Dockerfile is created to package the Flask application and its dependencies into a Docker image.
  - This allows for easy deployment and scaling of the application using container orchestration tools like Docker Compose or Kubernetes.
