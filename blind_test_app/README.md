# Blind Test Backend

Backend service for the Blind Test application, built with FastAPI.

## Features

- **User Management**: Admin, Head, and Judge roles
- **Model Management**: AI/LLM model definitions and lifecycle
- **Question Pools**: Organize and manage question banks
- **Test Management**: Orchestrate blind test workflows
- **Answer Logs**: Persist model responses for evaluation

## Tech Stack

- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- Alembic (migrations)
- JWT Authentication
- Pydantic (validation)

## Setup

### Requirements

- Python 3.11+
- PostgreSQL
- Docker (optional, for local database)

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd blind_test_app
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate    # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create your environment file:
```bash
cp env.example .env
# edit the .env file as needed
```

5. Create the PostgreSQL database:
```sql
CREATE DATABASE blind_test_db;
```

6. Run database migrations:
```bash
alembic upgrade head
```

7. Start the application:
```bash
uvicorn app.main:app --reload
```

### Docker

```bash
docker-compose up --build
```

## API Documentation

Once the app is running:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
blind_test_app/
├── app/
│   ├── api/                 # API routers
│   ├── core/                # Configuration and security
│   ├── db/                  # DB models and CRUD
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Domain services
│   └── main.py              # Application entrypoint
├── alembic/                 # Migration files
├── tests/                   # Test files
└── requirements.txt         # Python dependencies
```

## Database Schema (high level)

Primary tables:
- **users**: User accounts (Admin/Head/Judge)
- **models**: AI/LLM model definitions
- **input_pools**: Question pools
- **questions**: Test questions
- **tests**: Test definitions
- **answer_logs**: Stored model answers

## API Endpoints

Base URL prefix: `/api/v1`

### Health & Root
- `GET /` – Root (service info)
- `GET /health` – Health check

### Authentication (`/auth`)
- `POST /api/v1/auth/signup` – Register user (default role: Judge)
- `POST /api/v1/auth/login` – Login, returns access and refresh tokens
- `POST /api/v1/auth/refresh` – Refresh access token
- `GET /api/v1/auth/me` – Get current user (requires Authorization)

### Users (`/users`) – Admin only unless specified
- `POST /api/v1/users/` – Create user
- `POST /api/v1/users/judges` – Create judge (admin)
- `POST /api/v1/users/judges/head` – Create judge (head role)
- `GET /api/v1/users/` – List users
- `GET /api/v1/users/judges` – List judges
- `GET /api/v1/users/{user_id}` – Get user by ID
- `PUT /api/v1/users/{user_id}` – Update user
- `DELETE /api/v1/users/{user_id}` – Delete user

### Models (`/models`) – Admin only
- `POST /api/v1/models/` – Create model
- `GET /api/v1/models/` – List models
- `GET /api/v1/models/active` – List active models
- `GET /api/v1/models/{model_id}` – Get model by ID
- `PUT /api/v1/models/{model_id}` – Update model
- `DELETE /api/v1/models/{model_id}` – Delete model

### Input Pools (`/input-pools`) – Admin only
- `POST /api/v1/input-pools/` – Create input pool
- `GET /api/v1/input-pools/` – List input pools
- `GET /api/v1/input-pools/{pool_id}` – Get input pool by ID
- `PUT /api/v1/input-pools/{pool_id}` – Update input pool
- `DELETE /api/v1/input-pools/{pool_id}` – Delete input pool

### Questions (`/questions`) – Admin only
- `POST /api/v1/questions/` – Create question
- `GET /api/v1/questions/` – List questions
- `GET /api/v1/questions/pool/{pool_id}` – List by pool
- `GET /api/v1/questions/category/{category}` – List by category
- `GET /api/v1/questions/type/{question_type}` – List by type
- `GET /api/v1/questions/{question_id}` – Get question by ID
- `PUT /api/v1/questions/{question_id}` – Update question
- `DELETE /api/v1/questions/{question_id}` – Delete question

### Tests (`/tests`)
- `POST /api/v1/tests/` – Create test (admin)
- `GET /api/v1/tests/` – List tests (admin)
- `GET /api/v1/tests/active` – List active tests (head)
- `GET /api/v1/tests/active/judge` – List active tests for judge (judge)
- `GET /api/v1/tests/{test_id}/judge` – Get test details for judge (only ACTIVE)
- `GET /api/v1/tests/{test_id}` – Get test by ID (admin)
- `PUT /api/v1/tests/{test_id}` – Update test (admin)
- `DELETE /api/v1/tests/{test_id}` – Delete test (admin)

### Answer Logs (`/answer-logs`)
- `POST /api/v1/answer-logs/` – Create answer log (judge)
- `GET /api/v1/answer-logs/` – List answer logs (admin)
- `GET /api/v1/answer-logs/test/{test_id}` – List by test (admin)
- `GET /api/v1/answer-logs/judge/{judge_id}` – List by judge (admin)
- `GET /api/v1/answer-logs/model/{model_id}` – List by model (admin)
- `GET /api/v1/answer-logs/question/{question_id}` – List by question (admin)
- `GET /api/v1/answer-logs/my` – List current judge's logs (judge)
- `GET /api/v1/answer-logs/my/{log_id}` – Get own log by ID (judge)
- `GET /api/v1/answer-logs/{log_id}` – Get log by ID (admin)
- `PUT /api/v1/answer-logs/{log_id}` – Update log (admin)
- `DELETE /api/v1/answer-logs/{log_id}` – Delete log (admin)

## Development

### Create a migration

```bash
alembic revision --autogenerate -m "Migration description"
alembic upgrade head
```

### Run tests

```bash
pytest
```

## License

This project is licensed under the MIT License.
