
# User Management System Project

This project is designed to manage user information using a MySQL database and a web server.

## Setup Instructions

### Prerequisites:
- Install MySQL on your local computer.

### Steps:

1. **Create Database:**
    - Open your MySQL command line tool and execute the following command to create a new database:
      ```sql
      CREATE DATABASE user_management;
      ```

2. **Configure Database Settings:**
    - Navigate to:
      ```
      User-management/main/database/config.py
      ```
    - Update the `MYSQL_USER` and `MYSQL_PASSWORD` constants to your MySQL credentials.

3. **Initialize Database:**
    - Go to:
      ```
      User-management/main/__init__.py
      ```
    - **Important:** Run this file only once as it will clear all data in the 'user_management' database.

4. **Start the Server:**
    - Navigate to:
      ```
      User-management/main/app.py
      ```
    - Run this file to start the server.

5. **Access the Web Interface:**
    - Visit the following URL in your web browser:
      ```
      http://127.0.0.1:5000
      ```

6. **Local API Usage:**
    - Navigate to:
      ```
      User-management/local/
      ```
    - Here you will find three Python files. You can copy these files to any location on your system and run them as needed for local API usage.

