# Vendor Management System with Performance Metrics

## Objective
Develop a Vendor Management System using Django and Django REST Framework. This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics.

## Setup Instructions

### Prerequisites
- Python 3.x installed on your system.
- pip package manager installed.

### Installation Steps

1. Clone the repository to your local machine:
   git clone https://github.com/TandaleAbhijeet/VendorManagement.git


2. Create a virtual environment to isolate project dependencies:
   python3 -m venv venv

3. Activate the virtual environment:
   - On Windows:
     venv\Scripts\activate
   - On macOS and Linux:
     source venv/bin/activate
     
4. Navigate to the project directory:
   1.cd VendorManagement
   2.cd vendorManagment 

5. Install Django and Django REST Framework using pip:
   pip install django djangorestframework

6. Migrate the database to create necessary tables:
   python manage.py migrate

7. Run the development server:
   python manage.py runserver

8. Access the Vendor Management System in your browser at `http://127.0.0.1:8000/`.

