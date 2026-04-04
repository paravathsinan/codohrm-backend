# CODO HRM - Backend API 🚀

A modern, high-performance Human Resource Management System backend built with **Django** and **Django REST Framework**.

---

## 🛠 Tech Stack

- **Framework:** Django 6.0.3+
- **API:** Django REST Framework (DRF)
- **Authentication:** SimpleJWT (JWT)
- **Database:** SQLite (Development) / PostgreSQL (Recommended for Production)
- **Environment Management:** python-dotenv

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.13+
- pip

### 2. Setup (Local Development)

```bash
# Clone the repository (if not already done)
cd codohrm-backend

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and set your SECRET_KEY and other variables
```

### 3. Database Initialization

```bash
python manage.py migrate
python manage.py createsuperuser  # Optional: for admin access
```

### 4. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/v1/`

---

## 📂 Project Structure

- `apps/`: Contains all application logic organized by module (users, roles, employees).
- `config/`: Project-wide settings and root URL routing.
- `apps/users/`: Custom User model and authentication logic.
- `apps/roles/`: RBAC (Role Based Access Control) management.
- `apps/employees/`: Employee lifecycle and profile management.

---

## 🔐 Security & Standards

- **JWT Authentication:** Secure stateless session management.
- **CORS Configured:** Restricted to trusted frontend origins.
- **Environment Isolated:** Secrets are handled via `.env` and excluded from Git.

---

## 📝 License

Part of the **CODO AI Innovations** ecosystem. Built according to Codo AI Engineering Standards v2.0.

*Built for speed, reliability, and visual excellence.* 🛡️
