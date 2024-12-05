My Podcasts Project

Overview

My Podcasts Project is a Django-based web application designed to fetch and display podcast episodes from various RSS feeds. This project aims to provide an easy-to-use interface for users to browse and listen to their favorite podcasts. The application periodically fetches new episodes from specified RSS feeds and updates the database, ensuring that users always have access to the latest content.

Features

RSS Feed Integration: Fetches podcast episodes from multiple RSS feeds, including popular podcasts like "The Daily," "Hardcore History," "Radiolab," "Freakonomics Radio," and "The Tim Ferriss Show."
Episode Details: Displays detailed information about each episode, including the title, description, publication date, and a link to listen to the episode.
Admin Interface: Provides an admin interface for managing podcast episodes, allowing administrators to add, edit, or delete episodes as needed.
Scheduled Tasks: Uses django-apscheduler to periodically fetch new episodes from the RSS feeds, ensuring that the database is always up-to-date.
Responsive Design: Utilizes Bootstrap for a responsive and user-friendly interface, ensuring a seamless experience across different devices.
Installation

Prerequisites

Python 3.6 or higher
Django 3.x or higher
PostgreSQL or SQLite (for development)
Steps

Clone the Repository


git clone https://github.com/ivmakiv/my_podcasts_project.git
cd my_podcasts_project
Create and Activate a Virtual Environment


python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate  # On Windows
Install Dependencies


pip install -r requirements.txt
Set Up the Database

For SQLite (default): No additional setup required.
For PostgreSQL: Update DATABASES setting in settings.py and create the database.
Apply Migrations


python manage.py makemigrations
python manage.py migrate
Create a Superuser


python manage.py createsuperuser
Run the Development Server


python manage.py runserver
Access the Application

Open your web browser and navigate to http://localhost:8000.

Usage

Admin Interface: Access the admin interface at http://localhost:8000/admin and log in with the superuser credentials.
View Podcasts: The main page displays a list of podcast episodes fetched from various RSS feeds.
Scheduled Tasks: The application uses django-apscheduler to periodically fetch new episodes from the RSS feeds.
