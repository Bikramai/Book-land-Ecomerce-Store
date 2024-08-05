# Social Media E-commerce Web App

Welcome to the Social Media E-commerce BOOK LAND

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction
This web application is designed to combine the best aspects of social media and e-commerce for book lovers. Users can browse products, make purchases, and share their favorite items with friends and followers.

## Features
- User authentication and authorization
- Product listings and detailed views
- Shopping cart and checkout process
- Social media integration (Wishlist, Comments)
- Admin dashboard for product and order management

## Technologies Used
**Frontend:**
- HTML, CSS, JavaScript
- DTL (JINJA)
- Bootstrap

**Backend:**
- Python
- Django

**Database:**
- PostgreSQL

## Installation

### Prerequisites
- Python 3.8+
- Django

### Steps
1. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
2. **INSTALLATION:**
   ```bash
    pip install -r requirements.txt
    python manage.py makemigrations accounts
    python manage.py migrate accounts
    
    python manage.py makemigrations admins
    python manage.py migrate admins
    
    python manage.py makemigrations website
    python manage.py migrate website
    
    python manage.py migrate

3. **RUN:**
   ```bash
   python manage.py createsuperuser
   python manage.py runserver




4. **SITE:**

    Navigate to http://localhost:8000 to access the backend admin panel.
    Navigate to http://localhost:3000 to access the frontend user interface.