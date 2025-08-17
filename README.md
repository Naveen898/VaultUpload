# VaultUpload

VaultUpload is a file sharing application designed to securely upload, share, and manage files with built-in virus scanning and expiration features. The application utilizes JWT tokens for secure access to shared files.

## Features

- **File Upload**: Users can upload files to the server.
- **Virus Scanning**: Uploaded files are scanned for viruses before being stored.
- **JWT Authentication**: Files are protected by JWT tokens, ensuring only authorized users can access them.
- **Expiry Management**: Files can be set to expire after a specified duration, with automatic deletion.
- **Secure Sharing**: Users can share files via secure links that require a valid JWT token for access.

## Project Structure

```
VaultUpload/
├── backend/                  # Backend application
│   ├── main.py               # Entry point of the backend app
│   ├── routes/               # API endpoints
│   ├── services/             # Core business logic
│   ├── utils/                # Helper utilities
│   ├── config/               # Configurations
│   ├── tests/                # Unit & integration tests
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile            # Backend container image
│   └── gunicorn.conf.py      # Production server tuning
├── frontend/                 # Frontend application
│   ├── package.json          # Frontend dependencies
│   ├── vite.config.js        # Vite config
│   ├── src/                  # Source files
│   ├── public/               # Static assets
│   └── Dockerfile            # Frontend container image
├── devops/                   # DevOps configurations
│   ├── docker-compose.yml     # Local Dev setup
│   ├── k8s/                  # Kubernetes manifests
│   ├── terraform/            # Infrastructure as Code
│   └── ansible/              # Configuration management (optional)
├── .gitignore                # Files to ignore in version control
├── README.md                 # Project documentation
└── LICENSE                   # License file
```

## Getting Started

### Prerequisites

- Python 3.x
- Node.js and npm (for frontend)
- Docker (for containerization)
- Kubernetes (for deployment)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/VaultUpload.git
   cd VaultUpload
   ```

2. Set up the backend:
   - Navigate to the `backend` directory.
   - Install dependencies:
     ```
     pip install -r requirements.txt
     ```

3. Set up the frontend:
   - Navigate to the `frontend` directory.
   - Install dependencies:
     ```
     npm install
     ```

### Running the Application

- To run the backend:
  ```
  cd backend
  python main.py
  ```

- To run the frontend:
  ```
  cd frontend
  npm run dev
  ```

### API Documentation

Refer to the API documentation in the `backend/routes` directory for detailed information on available endpoints.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.