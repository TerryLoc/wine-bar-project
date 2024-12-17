
# Wine Bar Experience


<p>An immersive application that offers curated wine-tasting experiences in a restaurant setting. All events feature stunning projections of vineyards and landscapes to create an unforgettable atmosphere.</p>

## Table of Contents

<ul>
  <li><a href="#about-the-project">About the Project</a></li>
  <li><a href="user-stories">User Stories</a></li>
  <li><a href="#features">Features</a></li>
  <li><a href="#setup-and-installation">Setup and Installation</a></li>
  <li><a href="#usage">Usage</a></li>
  <li><a href="#technologies-used">Technologies Used</a></li>
  <li><a href="#contributing">Contributing</a></li>
  <li><a href="#license">License</a></li>
</ul>

## About the Project

<p>This project is a Django-based web application that allows users to explore and book exclusive wine-tasting experiences. 
The events are hosted in a restaurant setting where the walls come alive with stunning projections, creating an immersive atmosphere. 
Users can register, log in, and manage their profiles while enjoying curated wine experiences from around the world.</p>

## User Stories

<P>
** User Stories for the Wine Bar Project: **

User:
- As a User, I want to register and create an account so that I can book wine-tasting experiences.

- As a User, I want to view a list of available wine-tasting experiences so that I can choose one that suits my preferences.

- As a User, I want to see detailed information about a wine-tasting experience so that I can make an informed decision.

- As a User, I want to book a wine-tasting experience for myself and my friends, so that I can enjoy the event.

- As a User, I want to cancel or modify my booking so that I can adjust my plans easily.

- As a User, I want to receive email notifications when my booking is confirmed, so I know it's secured.

 - As a User, I want to view and update my profile information so that I can manage my preferences.
  
Admin:
- As an Admin, I want to create new wine-tasting experiences so that I can keep the offerings fresh and up-to-date.

- As an Admin, I want to update wine-tasting events so that I can modify details like price, availability, and description.

- As an Admin, I want to delete wine-tasting events so that I can remove outdated or canceled experiences.

- As an Admin, I want to see all bookings for a specific wine-tasting event so that I can manage attendance.
</p>

## Features

<ul>
  <li>User registration, login, and profile management</li>
  <li>Curated wine-tasting events from regions like Italy, Argentina, and Chile</li>
  <li>Dynamic booking system with real-time spot updates</li>
  <li>Interactive restaurant projections of vineyards and landscapes</li>
  <li>Admin panel for managing events and user data</li>
</ul>

## Setup and Installation

<ol>
  <li>
    <p>Clone the repository:</p>
    <code>git clone https://github.com/yourusername/wine-bar-experience.git</code>
  </li>
  <li>
    <p>Navigate to the project directory:</p>
    <code>cd wine-bar-experience</code>
  </li>
  <li>
    <p>Create and activate a virtual environment:</p>
    <code>python -m venv venv</code><br>
    <code>source venv/bin/activate</code> (on Mac/Linux)<br>
    <code>venv\Scripts\activate</code> (on Windows)
  </li>
  <li>
    <p>Install the dependencies:</p>
    <code>pip install -r requirements.txt</code>
  </li>
  <li>
    <p>Apply the database migrations:</p>
    <code>python manage.py migrate</code>
  </li>
  <li>
    <p>Create a superuser:</p>
    <code>python manage.py createsuperuser</code>
  </li>
  <li>
    <p>Start the development server:</p>
    <code>python manage.py runserver</code>
  </li>
  <li>
    <p>Access the application at:</p>
    <a href="http://127.0.0.1:8000" target="_blank">http://127.0.0.1:8000</a>
  </li>
</ol>

## Usage

<p>Users can explore available wine experiences, register for events, and manage their bookings through their profiles. 
The admin panel can be accessed by the superuser to manage wine events, users, and bookings.</p>

## Technologies Used

<ul>
  <li><strong>Backend:</strong> Django (Python)</li>
  <li><strong>Frontend:</strong> HTML, CSS, Django Templates</li>
  <li><strong>Database:</strong> SQLite (default)</li>
  <li><strong>Deployment:</strong> Heroku or any WSGI-compatible server</li>
  <li><strong>Version Control:</strong> Git</li>
</ul>

## Contributing

<p>Contributions are welcome! To contribute:</p>
<ol>
  <li>Fork the repository</li>
  <li>Create a new branch (<code>git checkout -b feature-branch</code>)</li>
  <li>Commit your changes (<code>git commit -m "Add a feature"</code>)</li>
  <li>Push to the branch (<code>git push origin feature-branch</code>)</li>
  <li>Open a pull request</li>
</ol>

## License

<p>This project is licensed under the <strong>MIT License</strong>. See the <code>LICENSE</code> file for details.</p>

---

<p>&copy; 2024 Wine Bar Experience. All Rights Reserved.</p>
