﻿# Django-Fileserver-Project
This platform allows businesses to distribute documents such as wedding cards, admission forms, etc., to various users. User can sign up, log in, search for files, download them and send files via email. Administrators can upload files and view usage statistics
## Key Features
- User registration and authentication with email verification
- Password reset functionality
- File feed page for browsing and downloading files
- Search functionality for files
- Email file sharing
- Admin dashboard for file management and analytics
## Installation Guide
### Prerequisites
- Python 3.x
- Django 3.x
- Sqlite

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/Zamani2025/Django-Fileserver-Project.git
   cd Django-Fileserver-Project
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Apply the migrations:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:

   ```bash
   python manage.py runserver
   ```
### Usage Guide

```markdown
## Usage Guide

### User Registration and Login
1. Sign Up:
   - Go to the registration page and fill in your details.
   - Check your email for a verification link and click it to verify your account.
```
![Screenshot (6)](https://github.com/Zamani2025/Django-Fileserver-Project/assets/73368821/45ee78fe-6ef1-439e-92b9-8c5d01e69a17)
```markdown
2. Log In:
   - Go to the login page and enter your credentials.
```
![Screenshot (4)](https://github.com/Zamani2025/Django-Fileserver-Project/assets/73368821/c9dbe6f0-1d98-4a0d-a590-5d91ce9d59f1)
```markdown
### File Browsing and Downloading
1. Feed Page:
   - After logging in, you will see a list of available files.
   - Click on a file title to view its details and download it.

2. Search Files:
   - Use the search bar on the feed page to search for files by title or description.
```
![Screenshot (7)](https://github.com/Zamani2025/Django-Fileserver-Project/assets/73368821/b62b7dfc-a971-4ab8-943a-c1a4bced25cd)
```markdown
### Email File Sharing
1. Send File via Email:
   - On the file details page, enter the recipient's email address and click send.
   - The recipient will receive an email with a link to download the file.
```
![Screenshot (9)](https://github.com/Zamani2025/Django-Fileserver-Project/assets/73368821/a935adbb-6bdb-48c1-b33b-6f401b2196cb)
```markdown
### Admin Features
1. Upload Files:
   - Log in as an admin.
   - Go to the admin dashboard and upload new files with titles and descriptions.

2. View Analytics:
   - In the admin dashboard, view the number of downloads and emails sent for each file.
```
![Screenshot (10)](https://github.com/Zamani2025/Django-Fileserver-Project/assets/73368821/12882ca8-14c3-413f-9407-618544ca926a)
## Deploy Link
[File Server Live Demo](https://saani.pythonanywhere.com/login/)

## ER DIAGRAM
![my_project_visualized](https://github.com/Zamani2025/Django-Fileserver-Project/assets/73368821/f80c25fb-9e44-4914-92a2-a85b68b750b7)
