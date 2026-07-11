# Cloud-Based Learning Management System (Cloud LMS)

## Project Overview

The Cloud-Based Learning Management System (Cloud LMS) is a web-based application developed using **Flask** and deployed on **Amazon Web Services (AWS)**. It enables students to register, enroll in courses, access study materials, submit assignments, and view announcements. Administrators can manage courses, students, learning materials, and announcements through a secure role-based system.

---

## Technologies Used

- Python
- Flask
- HTML5
- CSS3
- Bootstrap 5
- MariaDB
- Amazon EC2
- Amazon S3
- Amazon CloudWatch
- AWS IAM
- Git
- GitHub

---

## Features

### Student Portal

- Student Registration
- Secure Login
- View Available Courses
- Enroll in Courses
- View My Courses
- Download Course Materials
- Submit Assignments
- View Announcements
- View Profile

### Admin Portal

- Manage Students
- Add Courses
- Edit Courses
- Delete Courses
- Upload Course Materials
- Post Announcements
- Dashboard with Statistics
- Role-Based Access Control

---

## AWS Services Used

### Amazon EC2

Hosts the Flask web application.

### Amazon S3

Stores course materials and assignment files.

### Amazon CloudWatch

Monitors EC2 instance performance and CPU utilization using CloudWatch alarms.

### AWS IAM

Provides secure access control and user permissions.

---

## Project Structure

```text
LMS_Project/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── routes/
│   ├── auth.py
│   ├── courses.py
│   ├── enrollments.py
│   ├── materials.py
│   ├── assignments.py
│   └── announcements.py
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── courses.html
│   ├── add_course.html
│   ├── edit_course.html
│   ├── materials.html
│   ├── upload_material.html
│   ├── assignments.html
│   ├── submit_assignment.html
│   ├── announcements.html
│   ├── add_announcement.html
│   ├── my_courses.html
│   ├── profile.html
│   └── 403.html
│
└── static/
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/cloud-lms.git
```

### Navigate to the Project

```bash
cd LMS_Project
```

### Create a Virtual Environment

```bash
python3 -m venv venv
```

### Activate the Virtual Environment

```bash
source venv/bin/activate
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

The application will be available at:

```
http://localhost:5000
```

---

## AWS Deployment Steps

1. Launch an Amazon EC2 instance.
2. Install Python, Git, and MariaDB.
3. Clone or upload the project to EC2.
4. Create and activate a Python virtual environment.
5. Install project dependencies.
6. Configure the MariaDB database.
7. Configure AWS IAM credentials.
8. Create an Amazon S3 bucket.
9. Upload course materials and assignments to S3.
10. Launch the Flask application.
11. Configure Amazon CloudWatch monitoring and alarms.

---

## Security Features

- Secure Login Authentication
- Session Management
- Role-Based Access Control
- AWS IAM Integration
- Amazon S3 Secure File Storage
- CloudWatch Monitoring

---

## Future Enhancements

- Online Quiz System
- Video Lectures
- Student Attendance Module
- Email Notifications
- Discussion Forum
- Mobile Application
- Online Examination System
- Certificate Generation

---

## Screenshots

Include screenshots of:

- Home Page
- Login Page
- Student Dashboard
- Admin Dashboard
- Course Management
- Material Upload
- Assignment Submission
- Announcements
- Amazon S3 Bucket
- CloudWatch Alarm

---

## Author

**Abhinand P**

Cloud Computing Mini Project

2026

---

## License

This project is developed for academic purposes as part of the Cloud Computing Mini Project.
