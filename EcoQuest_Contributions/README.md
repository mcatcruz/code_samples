# EcoQuest: A Women Who Code Hackathon for Social Good 2023 Project - Code Sample

This document is an overview of the code I authored as part of EcoQuest, an entry for the Women Who Code Hackathon for Social Good 2023. It highlights my contributions and explains their functionality.

## Table of Contents

- [Overview](#overview)
- [Code Contributions](#code-contributions)

## Overview

EcoQuest is a web application whose goal is to help users adopt eco-friendly practices through gamification and progress tracking. 

## Code Contributions

My contributions are for backend functionality of plant-based meal tracking. These include processing POST and GET requests from the frontend as well as calculating the amount of carbon dioxide emissions saved by eating a plant-based meal. See below for additional information on the specific files.

### ecomeals_models.py

This model stores information about eco-conscious meal choices made by users.Each instance represents a specific meal choice, including breakfast, lunch, or dinner, and tracks metrics such as reduced carbon dioxide emissions and earned points earned from tracking meals. 

### ecomeals_serializer.py

This serializer is used to convert EcoMeals model instances into a structured format that can be easily rendered into JSON or other content types. It includes an additional field 'meal_type' to represent the type of meal choice made, which can be 'Breakfast,' 'Lunch,' or 'Dinner' based on the eco-conscious selections.

### ecomeals_views.py

These views allow users to retrieve a list of all EcoMeals activities recorded and create new EcoMeals instances for the current user.