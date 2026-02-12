# Store Management API

> Enterprise-grade Store Management API designed to demonstrate backend architecture, data modeling, and business rule implementation using modern cloud-native principles.

Enterprise-grade retail backend system designed to demonstrate enterprise cloud architecture patterns, architectural trade-off analysis (containers vs serverless), event-driven evolution strategy, and governance-aligned AWS deployment.

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
9. [Enterprise Architectural Evolution](#enterprise-architectural-evolution)
10. [C4 Architecture Diagrams](#c4-architecture-diagrams)
11. [API Endpoints](#api-endpoints)
12. [Environments](#environments)
13. [CI/CD Pipeline](#cicd-pipeline)
14. [Installation and Setup](#installation-and-setup)
15. [Testing](#testing)
16. [Future Improvements](#future-improvements)
17. [In case you clone the repo for future improvements](#in-case-you-clone-the-repo-for-future-improvements)
18. [Target Audience](#target-audience)
19. [License](#license)

---

## Introduction

This project is an enterprise-grade retail backend system designed to demonstrate **cloud architecture decision-making, domain-driven design principles, and governance-ready deployment strategies** in an AWS enterprise context.

> This project is an enterprise-grade Store Management API designed to showcase **backend architecture, business rules, and cloud-ready design**.

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

```mermaid
graph LR
    A[Client / Swagger UI] --> B[FastAPI REST API]
    B --> C[Business Logic Layer]
    C --> D[(PostgreSQL Database)]
    B --> E[CI/CD & Monitoring]
```

> ![Architecture](/assets/architecture.png)

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

## Enterprise Architectural Evolution

This project was intentionally designed as a modular, enterprise-ready backend system.  
Beyond its current container-based deployment model, the architecture has been evaluated against alternative enterprise-grade cloud patterns to support long-term scalability, governance, and cost optimization strategies.

The following sections outline how this system could evolve in a real enterprise context.

---

### Alternative Architecture: Serverless-First Design

While the current implementation is container-based (ECS/EKS + RDS), an alternative cloud-native architecture could leverage fully managed serverless services.

#### Serverless Architecture Variant (AWS Example)

- **API Layer:** Amazon API Gateway
- **Compute:** AWS Lambda (stateless functions per bounded context)
- **Database:** Amazon DynamoDB or Aurora Serverless v2
- **Event Bus:** Amazon EventBridge
- **Async Processing:** Amazon SQS
- **Observability:** CloudWatch + X-Ray
- **Security:** IAM fine-grained roles per function

#### When Serverless Becomes Relevant

A serverless-first model would be preferable when:

- Traffic is highly unpredictable or burst-oriented
- Operational overhead must be minimized
- Teams are small and infrastructure management must be abstracted
- Cost optimization at low traffic volumes is critical
- Event-driven integrations are dominant

#### Trade-offs Compared to Container-Based Model

| Criteria                   | Containers (ECS/EKS + RDS) | Serverless (Lambda + DynamoDB) |
| -------------------------- | -------------------------- | ------------------------------ |
| Strong ACID Transactions   | ✅ Native                  | ⚠️ Limited / Complex           |
| Cold Start Impact          | ❌ None                    | ⚠️ Possible                    |
| Operational Control        | ✅ High                    | ⚠️ Abstracted                  |
| Cost (Low Traffic)         | ❌ Higher                  | ✅ Lower                       |
| Cost (High Sustained Load) | ✅ Predictable             | ⚠️ Can Increase                |
| Governance Complexity      | ⚠️ Medium                  | ⚠️ IAM Intensive               |
| Multi-Service Decoupling   | ⚠️ Requires Setup          | ✅ Native                      |

This project demonstrates architectural awareness rather than adherence to a single paradigm.

---

### Event-Driven Evolution Path

In an enterprise context, the system could progressively evolve toward an event-driven architecture to support:

- Cross-domain integrations
- Analytics pipelines
- Notification systems
- Decoupled microservices
- Real-time inventory synchronization

#### Example Event Flow

- `OrderConfirmed` → EventBridge
- `StockUpdated` → SQS queue
- `NotificationService` → Lambda consumer
- `ReportingService` → Asynchronous data projection

This evolution would:

- Reduce tight coupling between services
- Improve scalability of read-heavy workloads
- Enable real-time integrations
- Support future microservices decomposition

The current monolithic backend structure allows controlled evolution without premature complexity.

---

### Architectural Decision Record (ADR) Highlights

The following key decisions were made intentionally:

#### Monolith-First Strategy

Microservices were intentionally avoided to:

- Reduce operational overhead
- Prevent premature distribution complexity
- Maintain transactional integrity

#### Relational Database Choice

PostgreSQL was selected to:

- Ensure ACID compliance
- Support complex order lifecycle transactions
- Enforce referential integrity at database level
- Align with enterprise governance requirements

#### Container-Based Deployment

Containers were chosen to:

- Ensure portability across cloud providers
- Enable Kubernetes-based orchestration
- Support enterprise CI/CD workflows
- Maintain runtime consistency across environments

---

### Governance, Compliance & Enterprise Readiness

In an enterprise deployment scenario, the following controls would apply:

- Encryption at rest (RDS with KMS)
- Encryption in transit (TLS via AWS Certificate Manager)
- IAM least-privilege access policies
- Network isolation (Private Subnets + Security Groups)
- Secrets management (AWS Secrets Manager)
- Audit logging (AWS CloudTrail)
- Data retention lifecycle policies (GDPR / Law 25 alignment)
- Automated backups & Multi-AZ high availability

This ensures the architecture aligns with enterprise regulatory and operational standards.

---

### Infrastructure as Code (Enterprise Extension)

In a production-grade enterprise environment, infrastructure provisioning would be managed using:

- Terraform or AWS CDK
- Version-controlled infrastructure
- Automated environment bootstrapping
- Drift detection
- Policy-as-Code validation

This reinforces reproducibility, compliance, and scalability.

---

### Enterprise Migration Strategy

If business growth justified architectural evolution, the migration path would be:

1. Introduce event-driven components
2. Extract bounded contexts progressively
3. Introduce read-model projections
4. Move selective workloads to serverless
5. Maintain transactional core where required

This reflects a controlled, risk-managed architectural transformation rather than a disruptive rewrite.

---

### Why This Matters for Enterprise Cloud Architecture

This project demonstrates:

- Strategic architectural thinking
- Cloud pattern comparison and justification
- Governance and compliance awareness
- Scalable evolution planning
- Trade-off analysis
- Enterprise-ready DevOps practices

The objective is not to showcase a single cloud trend, but to demonstrate the ability to design systems aligned with business context, regulatory constraints, and long-term operational sustainability.

---

## C4 Architecture Diagrams

The following C4 diagrams illustrate the system at different abstraction levels, following enterprise architecture documentation standards.

### C4 – System Context Diagram

```mermaid
flowchart TB
    Customer["Customer"]
    Employee["Store Employee"]
    ExternalSystem["External Systems<br/>(ERP / Analytics / Notification)"]

    StoreAPI["Store Management API<br/>(Backend System)"]

    Customer -->|Places Orders / Views Products| StoreAPI
    Employee -->|Processes Orders| StoreAPI
    StoreAPI -->|Publishes Events / Shares Data| ExternalSystem
```

This diagram shows the system in its enterprise context, highlighting interactions with users and external systems.

### C4 – Container Diagram (Current Container-Based Architecture)

```mermaid
flowchart TB
    subgraph AWS Cloud
        ALB["Application Load Balancer"]
        ECS["ECS / EKS Cluster<br/>FastAPI Container"]
        RDS["Amazon RDS<br/>PostgreSQL"]
        Secrets["AWS Secrets Manager"]
        CloudWatch["CloudWatch Logs & Metrics"]
    end

    User["Client / Employee"]

    User --> ALB
    ALB --> ECS
    ECS --> RDS
    ECS --> Secrets
    ECS --> CloudWatch
```

Description:

- FastAPI runs in containers (ECS or EKS).
- PostgreSQL is hosted on Amazon RDS.
- Secrets are securely managed via AWS Secrets Manager.
- Observability is handled by CloudWatch.
- The ALB manages traffic routing and SSL termination.

### C4 – Container Diagram (Serverless Architecture Variant)

```mermaid
flowchart TB
    subgraph AWS Cloud
        APIGW["Amazon API Gateway"]
        Lambda["AWS Lambda Functions"]
        Dynamo["DynamoDB / Aurora Serverless"]
        EventBridge["Amazon EventBridge"]
        SQS["Amazon SQS"]
        CloudWatch["CloudWatch & X-Ray"]
    end

    User["Client / Employee"]

    User --> APIGW
    APIGW --> Lambda
    Lambda --> Dynamo
    Lambda --> EventBridge
    EventBridge --> SQS
    Lambda --> CloudWatch
```

Description:

- API Gateway exposes REST endpoints.
- Lambda functions handle business logic.
- DynamoDB (or Aurora Serverless) manages persistence.
- EventBridge enables event-driven integrations.
- SQS handles asynchronous processing.
- CloudWatch & X-Ray provide observability and tracing.

### Architectural Perspective

These diagrams illustrate two valid enterprise deployment strategies:

- Container-based architecture: optimal for strong transactional consistency, predictable workloads, and controlled runtime environments.
- Serverless architecture: optimal for burst traffic, event-driven systems, and reduced operational overhead.
  The project demonstrates architectural flexibility and decision-making aligned with business constraints rather than a one-size-fits-all cloud approach.

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

```mermaid
flowchart LR
    Dev[Code pushed] --> CI[GitHub Actions - Lint & Test]
    CI --> Build[Docker Image Build]
    Build --> Staging[Deploy to Staging Env]
    Staging --> Approval[Manual Approval]
    Approval --> Prod[Deploy to Production]
```

> ![CI/CD pipeline](/assets/cicd.png)

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

- Cloud Architects
- Solution Architects
- Cloud Platform Engineers
- Technical interviewers evaluating system design and architectural decision-making
- Engineers interested in enterprise-grade cloud architecture patterns

## License

This project is licensed under the MIT License.

> Everything should be ok now, try to add the ci/cd pipeline for the deploy on aws
