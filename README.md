# E-Commerce Project

## Description
This project is an E-Commerce platform developed using Django. It allows users to sign up, log in, look for products, add to wishlist and cart, and allows admin users to perform CRUD operations on products.

## Features

### Current Features:
- Add to cart/remove from cart
- Add to wishlist/add to cart from wishlist/remove from wishlist

### Ongoing:
- Checkout

### Upcoming:
- Social authentication
- Anonymous user add to cart functionality
- Payment gateway integration
- Buyer/seller role login functionality
- Advanced search
- Sorting of products on the shop page
- Blog integration

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

A `.env` file needs to be created with the following contents:
```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_URL=postgres://db_user:db_password@localhost:db_port_number/db_name
```
Note: Create a superuser and then add at least two products to the database as this is needed for the home page to display correctly.

## Technologies Used

- Django for the web framework
- Jazzmin for the admin panel customization

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
