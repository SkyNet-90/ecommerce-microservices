
# E-Commerce Microservices Project

## Overview

This project is a comprehensive e-commerce application built using a microservices architecture. It includes several services that handle different aspects of the application, such as user management, product management, and order processing. The application uses Azure Cosmos DB for data storage and integrates with various Azure services for security and secret management.

## Services

### User Service

Handles user registration and authentication. Users are stored in Azure Cosmos DB with hashed passwords for security.

**Endpoints:**
- `GET /user/<username>`: Retrieves user details.
- `POST /user`: Creates a new user.

### Product Service

Manages product information, including adding, retrieving, and deleting products.

**Endpoints:**
- `GET /product/<product_id>`: Retrieves product details.
- `POST /product`: Adds a new product.
- `DELETE /product/<product_id>`: Deletes a product.

### Order Service

Manages orders, including creating and deleting orders. Orders reference products and users.

**Endpoints:**
- `GET /order/<order_id>`: Retrieves order details.
- `POST /order`: Creates a new order.
- `DELETE /order/<order_id>`: Deletes an order.

## Frontend

The frontend application provides a user interface for interacting with the services. It includes pages for adding products, placing orders, and user management.

**Pages:**
- **Add Product**: Allows users to add new products.
- **Add Order**: Allows users to place new orders.
- **Login / Register**: Users can log in or register new accounts.

## Deployment

### Azure DevOps Pipeline

This project utilizes an Azure DevOps pipeline for continuous integration and continuous deployment (CI/CD). The pipeline automates the build, test, and deployment processes, ensuring that changes are smoothly integrated and deployed to production environments.

**Key Features:**
- **Automated Builds**: Triggers builds automatically on code commits.
- **Automated Testing**: Includes unit and integration tests.
- **Continuous Deployment**: Deploys the application to Azure resources.

For details on the pipeline configuration, refer to the `azure-pipelines.yml` file in the repository.

## Terraform Configuration

Terraform is used for managing Azure resources, including:
- Azure Cosmos DB
- Azure Key Vault
- Azure Web Apps

Configuration files are located in the `terraform` directory. 

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Azure SDKs
- Terraform
- Node.js (for frontend development)

### Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/SkyNet-90/ecommerce-microservices.git
   cd ecommerce-microservices
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables:**
   - Set up Azure Key Vault secrets for Cosmos DB credentials.

4. **Run Services:**
   ```bash
   python user_service.py
   python product_service.py
   python order_service.py
   ```

5. **Frontend:**
   - Navigate to the `frontend` directory.
   - Serve the application using a local server or integrate it with your chosen backend.

## Contributing

Contributions are welcome! Please follow the standard Git workflow for making changes and submitting pull requests.

## License

This project is licensed under the MIT License

## Contact

For any questions or feedback, please reach out to me!
