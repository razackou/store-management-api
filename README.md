# Store Management API

Enterprise-grade Store Management API designed to demonstrate backend architecture, data modeling, and business rule implementation using modern cloud-native principles.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Why this project?](#why-this-project)
3. [Architectural Design Decisions](#architectural-design-decisions)
4. [Business Context](#business-context)
5. [Data Model](#data-model)
6. [Key Features](#key-features)
7. [Architecture](#architecture)
8. [Cloud Deployment Strategy](#cloud-deployment-strategy)
9. [API Endpoints](#api-endpoints)
10. [Environments](#environments)
11. [CI/CD Pipeline](#cicd-pipeline)
12. [Installation and Setup](#installation-and-setup)
13. [Testing](#testing)
14. [Future Improvements](#future-improvements)
15. [In case you clone the repo for future improvements](#in-case-you-clone-the-repo-for-future-improvements)
16. [Target Audience](#target-audience)
17. [License](#license)

---

## Introduction

This project is an enterprise-grade Store Management API designed to showcase **backend architecture, business rules, and cloud-ready design**.

The application follows a data-driven approach inspired by the **MERISE methodology**, from Conceptual Data Model (MCD) to Logical Data Model (MLD), and finally implemented as a **RESTful API** using **FastAPI** and **PostgreSQL**.

Swagger UI (OpenAPI) is used as the primary interface for exploring and testing the API.

The primary objective of this project is **not to deliver a feature-rich frontend**, but to showcase:

- Strong data modeling and relational database design
- Clear separation between API layer, business logic, and persistence
- Realistic enterprise business rules (inventory, orders lifecycle, consistency)
- Environment-based configuration (dev / staging / production)
- CI/CD-ready architecture aligned with cloud best practices

This repository reflects how a backend service would be designed, implemented, and operated in a real-world enterprise or cloud environment.

---

## Why this project?

This project was intentionally designed as a backend-first system.

In real enterprise environments, backend services are often developed independently from frontend applications and consumed by multiple clients (web, mobile, internal tools, integrations).

The focus is therefore placed on:

- API contract clarity (OpenAPI / Swagger)
- Business rule enforcement at the service layer
- Data consistency and transactional integrity
- Scalability and maintainability
- Cloud and DevOps readiness

---

## Architectural Design Decisions

The architecture of this API follows the Clean Architecture principle, ensuring the business logic remains decoupled from external frameworks and database drivers. I chose FastAPI over heavier frameworks like Django because of its asynchronous capabilities and native support for Pydantic validation, which ensures type safety and high performance under load. To maintain data integrity—a critical requirement for retail systems—I opted for a Relational Database (PostgreSQL) to enforce ACID compliance during complex order transactions. The project utilizes the Repository Pattern, allowing for easier unit testing through dependency injection and providing the flexibility to swap the persistence layer (like DataBase migration) with minimal impact on the core business rules.

Non-Goals / Trade-offs:

- Microservices intentionally avoided to reduce operational overhead
- Authentication deferred to keep focus on core domain modeling
- Event-driven architecture postponed until scale justifies it

---

## Business Context

This API simulates the operations of a retail store, including:

- Customer management
- Product catalog and categories
- Order lifecycle and stock management
- Employee assignment for order processing

The design respects realistic enterprise business rules:

- One client can place multiple orders.
- A product can belong to multiple orders.
- Orders are linked to employees optionally.
- Product categories manage product organization.

---

## Data Model

The main entities are:

- **Client**: ID, Name, Email, Phone, Address
- **Product**: ID, Name, Description, Unit Price, Stock
- **Order**: ID, Date, Total Amount, Status
- **Category**: ID, Name
- **Employee**: ID, Name, Position

### Relationships / Associations

- **Placed (Client → Order)**: 1,N
- **Belong (Order → Product)**: N,N with Quantity
- **Appartenir (Product → Category)**: 1,N
- **Sell (Employee → Order)**: 0,N

Below is a **diagram of the database schema (MCD/MLD)**

![Diagram MCD](/assets/mcd.png)

---

## Key Features

- Full **CRUD** operations for all entities
- Business rules enforced at API layer
- **Inventory management**: stock decreases automatically on orders
- **Order lifecycle**: draft, confirmed, shipped, delivered
- Swagger/OpenAPI interactive documentation
- Configurable **environment variables** for dev/staging/prod
- Cloud-ready: containerized, ready for CI/CD deployment

---

## Architecture

![Architecture](/assets/architecture.png)

### Tech Stack

- **Backend**: FastAPI, Python
- **Database**: PostgreSQL
- **ORM / Migrations**: SQLAlchemy, Alembic
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Testing**: Pytest
- **Documentation**: OpenAPI / Swagger UI

### Design Principles

- Separation of **business logic** and **persistence**
- Environment-aware configuration (dev / staging / prod)
- API-first design
- Scalable and maintainable code structure

---

## Cloud Deployment Strategy

While this repository is container-neutral, the intended production architecture leverages cloud-native services to ensure the core architectural pillars.

- Compute: Deployable on Amazon ECS or EKS (Kubernetes) using Helm charts for orchestration. Horizontal Pod Autoscaling (HPA) is triggered based on CPU/Memory metrics to handle traffic spikes.
- Database: Migration from a local container to a managed service like Amazon RDS (PostgreSQL). This enables automated backups, Multi-AZ high availability, and encryption at rest.
- Networking & Edge:
  - Ingress: Managed via an Ingress Controller (Nginx/ALB) with SSL termination via AWS Certificate Manager.
  - CDN: Static documentation and any future frontend assets are served via Amazon CloudFront to reduce latency and egress costs.
- Governance & Compliance (Law 25 (Quebec)/GDPR): In a production scenario, PII (Personally Identifiable Information) in the `Client` entity would be encrypted at the database level and subject to strict data retention policies enforced by cloud-native lifecycle management.

![AWS Deploymement](/assets/aws.png)

---

## API Endpoints

Interactive API documentation is available at:

- `/docs` (Swagger UI)
- `/redoc` (ReDoc)

### Main Endpoints

- `/clients` – manage customers
- `/products` – manage products
- `/categories` – manage categories
- `/orders` – manage orders
- `/employees` – manage employees

Application health is available at:

- `/health`
- `/health/db`

![Endpoints](/assets/endpoints.png)

![Health](/assets/health.png)

---

## Environments

The project is designed with **3 isolated environments**, simulating real enterprise deployment:

| Environment | Database   | API URL                | Swagger              |
| ----------- | ---------- | ---------------------- | -------------------- |
| Development | db-dev     | http://localhost:8000  | Enabled              |
| Staging     | db-staging | http://staging.api.com | Enabled              |
| Production  | db-prod    | http://api.com         | Disabled / Protected |

All environment-specific settings are managed via **environment variables**.

---

## CI/CD Pipeline

The project includes a **CI/CD pipeline** using GitHub Actions:

![CI/CD pipeline](/assets/cicd.png)

### CI (Continuous Integration)

- Linting with `ruff` / `flake8`
- Unit tests with `pytest`
- Build Docker image
- Validation of database migrations

### CD (Continuous Deployment)

- Auto-deployment to dev environment on PR merge
- Staging deployment after approval
- Manual production deployment reflects enterprise change-management and risk-control practices.
- Environment variables injected via secrets / configs

---

## Installation and Setup

1. Clone the repository:

```
git clone https://github.com/razackou/store-management-api.git
cd store-management-api
```

2. Set up a virtual environment and install dependencies:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd backend
```

3. Configure environment variables:

```
DATABASE_URL=postgresql://user:password@localhost:5432/store_db
ENV=dev
DEBUG=True
```

4. Run database migrations:

```
alembic upgrade head
```

5. Start the API:

```
uvicorn main:app --reload
```

6. Access Swagger UI:

```
http://127.0.0.1:8000/docs
```

## Testing

- Run unit tests with:

```
pytest -v
pytest --cov
```

- Integrated into CI pipeline
- Check code coverage and linting as part of CI

## Future Improvements

- Add authentication / Role-Based Access Control
- Multi-store support
- Reporting / analytics endpoints
- Frontend SPA (React / Vue) consuming API
- Integration with cloud managed database services (RDS, Cloud SQL)

## In case you clone the repo for future improvements

in GitHub Secrets — Add these to the repo (Settings > Secrets and variables > Actions):

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION (e.g., us-east-1)
ECR_REPOSITORY (e.g., store-management-api)
ECS_CLUSTER (your cluster name)
ECS_SERVICE (your service name)
```

AWS Setup (one-time):

```
# Create ECR repository
aws ecr create-repository --repository-name store-management-api --region us-east-1

# Create Secrets Manager entries for DB credentials
aws secretsmanager create-secret --name store-management-api/db-url --secret-string "postgresql://..." --region us-east-1
```

Update ecs/taskdef.json file by replacing:

- PLACEHOLDER_IMAGE_URI → your ECR repo URI
- REGION and ACCOUNT placeholders → your AWS details
- IAM role ARNs for executionRoleArn and taskRoleArn

You can now push to GitHub and watch the workflow run automatically!

## Target Audience

- Backend Engineers
- Cloud Engineers
- Cloud / Solution Architects
- Technical interviewers evaluating system design and backend capabilities
- Anyone interested in enterprise-grade API design

## License

This project is licensed under the MIT License.

> Everything should be ok now, try to add the ci/cd pipeline for the deploy on aws
