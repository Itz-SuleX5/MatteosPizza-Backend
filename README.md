# Matteo's Pizza - Backend

This repository contains the backend service for the Matteo's Pizza web application. It is built with Python and the Django Rest Framework to handle user data, product catalogs, and customer orders.

The frontend for this application is a separate **React** application. You can find its repository here: [Link to Frontend Repo](Is not available at the moment) 

## Features

*   **User Profile Management**: Allows users to view and update their profile information (address, phone).
*   **Product & Order APIs**: Provides endpoints for listing products and placing orders (via the `products` and `orders` apps).
*   **Secure Authentication**: Endpoints are protected using Auth0 for secure, token-based authentication.

## Tech Stack

*   **Python**
*   **Django** & **Django Rest Framework (DRF)**
*   **Auth0** for authentication
*   **SQLite** as the default development database

---

## Getting Started

Follow these instructions to get the project running on your local machine for development and testing.

### Prerequisites

*   Python 3.9+
*   Pip package manager
*   `virtualenv` for environment isolation (recommended)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd backend
    ```

2.  **Create and activate a virtual environment:**
    *   On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install dependencies:**
    Create a `requirements.txt` file by running `pip freeze > requirements.txt` and then install from it.
    ```bash
    pip install -r requirements.txt
    ```
    *Key libraries to include are `django`, `djangorestframework`, `python-jose`, and `requests`.*

4.  **Configure Environment Variables:**
    This project requires Auth0 credentials to be set in `backend/settings.py`. It is highly recommended to use environment variables to manage these secrets.
    
    Make sure your `settings.py` can load the following variables:
    *   `SECRET_KEY`: Your Django secret key.
    *   `AUTH0_DOMAIN`: Your Auth0 domain.
    *   `AUTH0_API_AUDIENCE`: Your Auth0 API audience identifier.

5.  **Apply database migrations:**
    This will set up the initial database schema.
    ```bash
    python manage.py migrate
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000/`.

---

## API Endpoints

All protected endpoints require an `Authorization: Bearer <Your-Access-Token>` header.

*   **User Profile**
    *   `GET /users/profile/`: Retrieves the profile for the currently authenticated user. Creates a profile if one doesn't exist.
    *   `PATCH /users/profile/`: Updates the profile for the currently authenticated user.
        *   **Body**: `{ "address": "123 Pizza Ln", "phone": "555-1234" }`

*   **Products** (Example structure)
    *   `GET /products/`: Lists all available products.

*   **Orders** (Example structure)
    *   `POST /orders/`: Creates a new order for the authenticated user.
    *   `GET /orders/`: Lists all past orders for the authenticated user.
