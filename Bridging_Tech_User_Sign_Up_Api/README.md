# Bridging Tech: User Sign-Up API for K-12 Educational Platform - Code Sample

## Overview
This document provides an overview of the API endpoint I developed for Bridging Tech, a non-profit organization dedicated to providing laptops to youth experiencing housing insecurity. The goal of the Bridging Tech Ed platform is to teach school-aged children how to effectively use computers and the internet.

## Code Contribution
The contribution highlighted in this code sample focuses on the user sign-up API endpoint, which handles user registration within the application. This functionality includes processing POST requests from the frontend, validating and storing user information, and generating a corresponding points history record in the database.

## Key Features
User Information Validation: The API checks for existing usernames and emails to ensure they are unique, providing clear feedback if they are already in use. <br>
Secure Password Handling: User passwords are securely hashed using bcrypt before being stored in the database. <br>
Parental Consent Management: The endpoint supports collecting parental consent for users under a certain age, with logic that distinguishes between parent and user emails based on age. <br>
Database Interaction: Upon successful user creation, a new row is automatically generated in the users_points_history table to track user engagement and rewards within the platform. <br>
Data Formatting: The API handles date formatting to ensure compatibility with PostgreSQL, converting user-provided date of birth data into the correct format.

## API Endpoint
Endpoint: /api/signup <br>
Method: POST <br>
Response: Returns a status code and message indicating the success or failure of the user creation process.
