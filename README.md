# Product Review System

A RESTful API for a Product Review System built with Django and Django REST Framework.

## Features

- User authentication with JWT (JSON Web Tokens)
- Role-based access control (Admin and Regular users)
- Product management (CRUD operations for admin users)
- Product reviews and ratings
- Product search functionality
- API documentation with Swagger/OpenAPI

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- SQLite (included with Python)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd product_review_system
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (admin):
   ```bash
   python manage.py createsuperadmin
   ```
   Follow the prompts to create an admin user.

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Documentation

Once the server is running, you can access the following URLs:

- **API Documentation (Swagger UI)**: http://127.0.0.1:8000/swagger/
- **API Documentation (ReDoc)**: http://127.0.0.1:8000/redoc/
- **Admin Interface**: http://127.0.0.1:8000/admin/

## API Endpoints

### Authentication

- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/token/refresh/` - Refresh access token
- `POST /api/auth/logout/` - Logout (invalidate refresh token)
- `GET /api/auth/profile/` - Get or update user profile

### Products

- `GET /api/products/` - List all products (search with `?search=<query>`)
- `POST /api/products/` - Create a new product (admin only)
- `GET /api/products/<id>/` - Get product details with reviews
- `PUT /api/products/<id>/` - Update a product (admin only)
- `DELETE /api/products/<id>/` - Delete a product (admin only)
- `GET /api/products/<id>/reviews/` - Get all reviews for a product
- `POST /api/products/<id>/reviews/` - Add a review to a product (authenticated users)
- `GET /api/products/<id>/stats/` - Get statistics for a product's reviews

### Reviews

- `GET /api/products/<product_id>/reviews/<id>/` - Get review details
- `PUT /api/products/<product_id>/reviews/<id>/` - Update a review (review owner only)
- `DELETE /api/products/<product_id>/reviews/<id>/` - Delete a review (review owner or admin)

## Testing

To run the test suite:

```bash
python manage.py test
```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
DEBUG=True
SECRET_KEY=your-secret-key-here
```
## Image
https://github.com/jith101/Back_End_Developer_Assignment/blob/master/lastscnshot.png?raw=true
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
