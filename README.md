# Recipe API Project

> A full-featured REST API for managing recipes, ingredients, and tags, built with Django REST Framework and Docker.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Admin Panel](#admin-panel)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

This project is a **Recipe Management API** that allows users to:

- Create and manage recipes with associated tags and ingredients.
- Upload images for recipes.
- Filter recipes by tags or ingredients.
- Secure authentication using a custom email-based user system.
- Generate and manage authentication tokens.
- Full admin management for recipes, ingredients, tags, and users.

The project is **Dockerized** to simplify deployment and development.

---

## Features

- **Custom User System**
  - Email-based authentication
  - Token authentication for API access
  - CRUD operations for user accounts
- **Recipe Management**
  - Create, update, retrieve, and delete recipes
  - Associate tags and ingredients
  - Upload images for recipes
  - Filter recipes by tags and ingredients
- **Admin Panel**
  - Full CRUD for recipes, tags, ingredients, and users
- **API Documentation**
  - OpenAPI / Swagger integration via `drf-spectacular`
- **Dockerized Environment**
  - Run API and Postgres in isolated containers
  - Easy setup for development and testing

---

## Technology Stack

- **Backend:** Python, Django, Django REST Framework
- **Database:** PostgreSQL
- **Containerization:** Docker, Docker Compose
- **Authentication:** Token-based, custom user model
- **Documentation:** drf-spectacular (OpenAPI / Swagger)

---

## Prerequisites

Before you start, make sure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)  
- [Docker Compose](https://docs.docker.com/compose/install/)  
- (Optional) [Python 3.11+](https://www.python.org/downloads/) if you want to run without Docker

---

## Setup Instructions

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/recipe-api.git
cd recipe-api
