# Codo HRM - Enterprise Backend API

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/paravathsinan/codohrm-backend)
[![Status](https://img.shields.io/badge/status-active-green.svg)]()
[![Django](https://img.shields.io/badge/django-^6.0.4-092e20.svg?logo=django)]()
[![DRF](https://img.shields.io/badge/django--rest--framework-^3.17.1-a30000.svg?logo=django)]()
[![Python](https://img.shields.io/badge/python-^3.10-blue.svg?logo=python)]()

> **The robust, scalable, and secure engine powering the Codo HRM platform. Engineered for high-concurrency enterprise HR operations.**

---

## 📊 Backend Overview

The **Codo HRM Backend** is a high-performance RESTful API built on the Django framework. It manages the complex business logic of enterprise human resources, including multi-level organizational hierarchies, automated attendance tracking, payroll processing, and role-based security.

### Core Capabilities

- 🔐 **JWT Authentication** - Secure, token-based stateless authentication flow.
- 👥 **Employee Lifecycle** - Complete management from onboarding to retirement.
- 📅 **Attendance & Leave Engine** - Automated calculation of work hours and leave balances.
- 💰 **Financial Services** - Payroll processing, reimbursements, and tax compliance.
- 📈 **Performance Tracking** - Standardized review cycles and goal management.
- 🏗️ **Project Management** - Resource allocation and effort pricing.

---

## 🏗️ Architecture & Modules

The system follows a modular Monolith architecture, where each business domain is encapsulated in its own Django app.

### Module Breakdown

| Module | Purpose | Key Models |
|--------|---------|------------|
| **Employees** | Core employee data | `Employee`, `Department`, `Designation` |
| **Attendance** | Time tracking | `AttendanceRecord`, `ClockInLog` |
| **Leaves** | Time off management | `LeaveRequest`, `LeaveBalance` |
| **Finance** | Payroll & Expenses | `Payroll`, `Payslip`, `Reimbursement` |
| **Performance** | Reviews & Goals | `PerformanceReview`, `KPI` |
| **Projects** | Work allocation | `Project`, `TeamAssignment` |
| **Users** | Account security | `User`, `UserRole`, `Permission` |
| **Core** | Shared utilities | `AuditLog`, `SystemConfig` |

---

## 🛠️ Technology Stack

| Technology | Usage |
|------------|-------|
| **Django** | Main application framework |
| **Django REST Framework** | API generation and serialization |
| **SimpleJWT** | Secure token handling |
| **CORS Headers** | Cross-Origin Resource Sharing for Frontend |
| **SQLite / PostgreSQL** | Database management |
| **Python Dotenv** | Configuration management |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **pip** (Python package manager)
- **Virtualenv** (Recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/paravathsinan/codohrm-backend.git
   cd codohrm-backend
   ```

2. **Setup Virtual Environment**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Copy the example environment file and update with your settings:
   ```bash
   cp .env.example .env
   ```

5. **Database Initialization**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```
   The API will be available at: `http://127.0.0.1:8000/api/v1/`

---

## 🔐 API Standards & Security

### Versioning
All API endpoints are versioned to ensure backward compatibility.
- Base URL: `/api/v1/`

### Authentication Flow
1. Client POSTs credentials to `/api/v1/users/login/`.
2. Server returns `access` and `refresh` tokens.
3. Client includes Bearer token in headers: `Authorization: Bearer <token>`.

### Security Features
- ✅ **RBAC (Role-Based Access Control)**: Enforced via custom DRF permission classes.
- ✅ **CORS Management**: Restricted to trusted frontend domains.
- ✅ **Data Validation**: Strict serialization and validation logic.
- ✅ **Environment Isolation**: Secure handling of sensitive keys via `.env`.

---

## 🤝 Contribution Guidelines

Follow the **Codo Lab Premium Engineering Standards**:
- Follow **PEP 8** style guidelines.
- Use **Class-Based Views (APIView/ViewSets)** for all endpoints.
- Keep business logic in services or models, not in serializers.
- Ensure all new migrations are committed.
- Maintain comprehensive audit logs for sensitive data changes.

---

## 📄 License

**Proprietary Software** - CODO AI Innovations © 2026

All rights reserved. Unauthorized copying, distribution, or use is strictly prohibited.

---

<div align="center">

**🚀 Powering Enterprise Intelligence at Scale**

[Back to Top](#codo-hrm---enterprise-backend-api)

</div>
