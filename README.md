# E-Commerce Project

## Description
This project is an E-Commerce platform developed using Django. It allows users to sign up, log in, look for products, add to wishlist and cart, and allows admin users to perform CRUD operations on products.

## Features

### Current Features:
- Add to cart/remove from cart
- Add to wishlist/add to cart from wishlist/remove from wishlist
- Advanced search
- Sorting of products based on rating, popularity, price,etc.
- Social authentication
- Checkout
- Blog integration
- Comment/Reply functionalities in blog posts
- Payment gateway integration
- Send Order details pdf to user on successful payment

### Ongoing:
- Code optimization

### Upcoming:
- Buyer/seller role login functionality

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/SaugatMgr/E-Commerce-Project.git
    ```
2. Navigate to the project directory:
    ```bash
    cd E-Commerce-Project
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
Note: Create a superuser and then add at least two products to the database as this is needed for the home page to display correctly.

A `.env` file needs to be created with the following contents:
```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_URL=postgres://db_user:db_password@localhost:db_port_number/db_name

# Authentication & Payment Gateway

SOCIAL_AUTH_FACEBOOK_KEY=Your Facebook API key
SOCIAL_AUTH_FACEBOOK_SECRET=Your Facebook API secret

KHALTI_PUBLIC_KEY=Your Khalti public key
KHALTI_SECRET_KEY=Your Khalti secret key

ESEWA_MERCHANT_ID=Your eSewa merchant ID
ESEWA_SECRET=Your eSewa secret key

# Celery Configuration

CELERY_BROKER_URL=URL of your message broker (e.g., RabbitMQ, Redis)
CELERY_RESULT_BACKEND=Backend for storing Celery task results
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP=Whether to retry connecting to the broker on startup (True or False)

# Email Configuration

EMAIL_HOST_USER=Your email address for sending emails
EMAIL_HOST_PASSWORD=Your app password
EMAIL_HOST=Email server host (e.g., smtp.gmail.com)
EMAIL_PORT=Port number for the email server (e.g., 465 for SSL)
EMAIL_USE_SSL=Whether to use SSL for the email server connection (True for SSL)
```

Then follow the following steps:
1. **Migrate changes**
   - Run the following command to migrate changes to database:
      ```bash
      python manage.py migrate
      ```
2. **Create a superuser:**
    - Run the following command and follow the prompts:
        ```bash
        python manage.py createsuperuser
        ```
    - Alternatively, you can sign up and log in from the home page.

3. **Run the server:**
    ```bash
    python manage.py runserver
    ```

## Technologies Used

- Django for the web framework
- Jazzmin for the admin panel customization
- Weasyprint for pdf generation

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature/fooBar
    ```
3. Make your changes.
4. Commit your changes:
    ```bash
    git commit -am 'Add some fooBar'
    ```
5. Push to the branch:
    ```bash
    git push origin feature/fooBar
    ```
6. Create a new Pull Request.
