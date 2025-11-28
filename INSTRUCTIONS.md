# How to Run This Project

This document provides instructions on how to set up and run this Django project locally.

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**
    - **macOS/Linux:**
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```
    - **Windows:**
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file:**
    Create a file named `.env` in the root of the project and add the following content.
    ```env
    SECRET_KEY='your-secret-key'
    DEBUG=True
    ```

5.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser (for accessing the admin panel):**
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create an admin user.

7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

8.  **Access the application:**
    Open your web browser and go to `http://127.0.0.1:8000/`. To access the admin panel, go to `http://127.0.0.1:8000/admin/`.
