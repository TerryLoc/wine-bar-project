# Wine Bar Experience

<p>Welcome to the <strong>Wine Bar booking system</strong> a place where technology and tradition come together to create unforgettable wine-tasting moments. Imagine yourself in a cozy restaurant, surrounded by walls that come alive with projections of picturesque vineyards and stunning landscapes from around the world. This application is your gateway to curated wine adventures, right from your screen to the perfect evening under the stars.</p>

## Table of Contents

<ul> 
<li><a href="#about-the-project">About the Project</a></li> <li><a href="#user-stories">User Stories</a></li> 
<li><a href="#features">Features</a></li> 
<li><a href="#setup-and-installation">Setup & Installation</a></li> 
<li><a href="#usage">Usage</a></li> 
<li><a href="#technologies-used">Technologies Used</a></li> 
<li><a href="#contributing">Contributing</a></li> 
<li><a href="#license">License</a></li> </ul>

## About the Project

<p>This is a Django-powered web application that manages the backend operations for booking and managing wine-tasting events. It handles user authentication, event scheduling, and booking management. The backend ensures seamless data flow between the database and the user interface, providing a robust platform for wine enthusiasts to explore and book immersive tasting experiences.</p>

## User Stories

<p>Here’s what we’ve built for you:</p>

### Users

<ul> 
<li><strong>As a User:</strong> I want to create an account so that I can book wine-tasting events.</li> 
<li><strong>As a User:</strong> I want to view all available experiences so I can pick the perfect one.</li> 
<li><strong>As a User:</strong> I want detailed information about each event to make an informed decision.</li> 
<li><strong>As a User:</strong> I want to book events for myself and my friends to enjoy together.</li> 
<li><strong>As a User:</strong> I want the flexibility to cancel or modify my booking if plans change.</li> 
<li><strong>As a User:</strong> I want to receive confirmation emails so I know my booking is secure.</li> 
<li><strong>As a User:</strong> I want to view and update my profile to keep my preferences up-to-date.</li> 
</ul>

### Admin

<ul> 
<li><strong>As an Admin:</strong> I want to create new wine-tasting events to keep the offerings fresh and exciting.</li> 
<li><strong>As an Admin:</strong> I want to update event details like availability and pricing as needed.</li> 
<li><strong>As an Admin:</strong> I want to remove outdated or canceled events to maintain an up-to-date catalog.</li> <li><strong>As an Admin:</strong> I want to view all bookings for specific events to manage attendance effectively.</li> 
</ul>

## Features

<ul>
  <li>
    <strong>Personalized User Registration, Login, and Profile Management:</strong>
    Users can register, log in, and manage their profiles. This functionality is handled by Django's built-in authentication system, with custom views and forms.
  </li>
  <br>
  <li>
    <strong>Curated Selection of Wine-Tasting Events:</strong>
    The application offers a variety of wine-tasting events from regions like Italy, Argentina, and Chile. These events are managed through models, views, and templates for displaying event details.
  </li>
  <br>
  <li>
    <strong>Real-Time Booking System:</strong>
    Users can book wine-tasting events with real-time updates on availability. The booking system is implemented in the `bookings` app, which handles the creation, modification, and cancellation of bookings. The availability of events is dynamically updated using Django signals.
  </li>
  <br>
  <li>
    <strong>Immersive Restaurant Projections:</strong>
    The venue features projections of picturesque vineyards, enhancing the wine-tasting experience. This feature is integrated with the frontend using JavaScript and CSS to create dynamic and immersive visuals.
  </li>
  <br>
  <li>
    <strong>Comprehensive Admin Panel:</strong>
    Admin users have access to a robust admin panel for managing events and user data. This is facilitated by Django's admin interface, with customizations in the `admin.py` files of the `accounts`, `events`, and `bookings` apps to provide a seamless management experience.
  </li>
</ul>

