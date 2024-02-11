# Vending Machine API

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

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/omarshamkh/vending-machine-api.git
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
    pip install -r requirements.txt
    ```

6. Run database migrations:

    ```bash
    python manage.py migrate
    ```

7. Start the development server:

    ```bash
    python manage.py runserver
    ```

## Usage

1. Ensure the development server is running.
2. Access the API endpoints using tools like Postman or through your web browser.

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
    python manage.py test users products
    ```
### Postman Collection for API Testing

You can find the Postman collection for testing the API endpoints [here](https://github.com/OmarShamkh/vending_machine_api/tree/master/postman_collection_test).

