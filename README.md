# Vending Machine API
(FlapKap’s Backend challenge!)
This repository contains the source code for a RESTful API for managing a vending machine system. The API allows users to perform various operations such as user authentication, product management, depositing funds, purchasing products, and resetting deposits.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)

## Features

- User authentication with JWT tokens
- CRUD operations for users and products
- Deposit funds into user accounts
- Purchase products with deposited funds
- Reset user deposits

## Technologies Used

- Django: Web framework for building the API
- Django REST Framework: Toolkit for building Web APIs
- SQLite: Database management system
- Postman: API development and testing environment


## Django project structure

- `vending_machine_api/`: Main project directory
    - `users/`: App for managing user operations
        - `migrations/`: Database migration files
        - `tests/`: Test cases for user operations
        - `__init__.py`: Initialization file for the app
        - `admin.py`: Admin configurations for user models
        - `models.py`: User model definitions
        - `serializers.py`: Serializers for user models
        - `urls.py`: URL configurations for user API endpoints
        - `views.py`: Views for handling user operations
    - `products/`: App for managing product operations
        - `migrations/`: Database migration files
        - `tests/`: Test cases for product operations
        - `__init__.py`: Initialization file for the app
        - `admin.py`: Admin configurations for product models
        - `models.py`: Product model definitions
        - `serializers.py`: Serializers for product models
        - `urls.py`: URL configurations for product API endpoints
        - `views.py`: Views for handling product operations
    - `manage.py`: Django command-line utility for administrative tasks
    - `requirements.txt`: List of Python dependencies

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/OmarShamkh/vending_machine_api.git
    ```

2. Navigate to the project directory:

    ```bash
    cd vending-machine-api
    ```

3. Create a virtual environment:

    ```bash
    python3 -m venv venv
    ```

4. Activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```

5. Install dependencies:

    ```bash
    pip3 install -r requirements.txt
    ```

6. Generate a SECRET_KEY for the Django application. You can use a random string generator tool or generate one manually. Replace the placeholder `YOUR_SECRET_KEY_HERE` in the `.env.example` file with your generated secret key.
    
    ```bash
    mv .env.example .env
    ```

7. Run database migrations:

    ```bash
    python3 manage.py migrate
    ```

8. Start the development server:

    ```bash
    python3 manage.py runserver
    ```

## Usage

1. Ensure the development server is running.
2. Access the API endpoints from http://localhost:8000/api/docs/

## API Endpoints

### Users

- `GET /api/users/`: Retrieve a list of users.
- `POST /api/users/`: Create a new user.
- `GET /api/users/{id}/`: Retrieve details of a specific user.
- `PUT /api/users/{id}/`: Update details of a specific user.
- `DELETE /api/users/{id}/`: Delete a specific user.
- `POST /api/users/login/`: Authenticat user.
- `POST /api/users/logout/`: Logout user.

### Products

- `GET /api/products/`: Retrieve a list of products.
- `POST /api/products/`: Create a new product.
- `GET /api/products/{id}/`: Retrieve details of a specific product.
- `PUT /api/products/{id}/`: Update details of a specific product.
- `DELETE /api/products/{id}/`: Delete a specific product.

### Deposit

- `POST /api/users/deposit/`: Deposit funds into the user's account.

### Buy

- `POST /api/users/buy/`: Buying products using deposited funds.

### Reset Deposit

- `POST /api/users/reset-deposit/`: Reset the user's deposit amount.

## Testing

1. Ensure the development server is running.
2. Run the tests using:

    ```bash
    python3 manage.py test users products
    ```
### Swagger Documentation
you can access the swagger documentation from the following link:
http://localhost:8000/api/docs/

