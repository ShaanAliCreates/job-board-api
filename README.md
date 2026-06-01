# Job-board-api

Production grade job listing platform built with FastAPI + PostgrSQL. Build within 14 days.

First request after sleep takes 30-60 seconds (cold start)
## Live demo
- API: https://job-board-api-1-0ry8.onrender.com
- DOCS: https://job-board-api-1-0ry8.onrender.com/docs

**Layer rules enforced:**
- Routes: parse request, call service, return — zero SQL
- Services: business logic + SQL — zero HTTP code
- Typed exceptions in services, HTTP handlers in main.py

---

## Tech Stack

|Layer | Technology |

| API | FastAPI + Pydantic v2 |
| DB driver | asyncpg (async, no ORM) |
| Database | PostgreSQL 16 |
| Migrations | Alembic |
| Local dev | Docker Compose |
| Deploy | Render.com| 

### Run locally (2 commands)

git clone https://github.com/ShaanAliCreates/job-board-api

cd job-board-api

docker compose up --build

- API: http://localhost:8000
- DOCS: http://localhost:8000/docs
- DB: localhost:5433 (user:postgres,db:jobboard)

requirements: DOCKER + DOCKER COMPOSE

Migartion run automatically on first start.
Data remain persistent across restart. 'docker compose down -v ' for wiping data.

## Features

- Job CRUD with many-to-many skills (ON CONFLICT upsert)
- Company registration with FK-linked jobs
- Application state machine: applied → screening → interview → offer
- Dynamic job filtering: location, salary range, skills, remote, status
- Cursor-based pagination (O(log n) vs offset O(n))
- Analytics endpoints: hiring velocity, top skills, application funnel
- Window functions: RANK() OVER, SUM() OVER, CTEs
- Request logging middleware with duration
- Global exception handlers with typed errors




## Key Engineering Decisions

# Pagination Design

This api implements cursor based pagination method for job feed
('/job/cursor') instead of tradation offset method.

Why Cursor based Pagination over offset?

Problem with Offset Pagination is for page 1500 with each page contain 10 items it scan 15010 items and then it return 10. Although it seem like it's skipping the 15000 rows but internally it read 15000 and skip then to reach required 10 rows.

~Offset pagination
[]Get slow with depth
[]with insert and delete it produce inconsistent ouput like duplicated row or skip a row

~Cursor Based Pagination
[] it limit is 10 Read exactly 10+1 rows
[] Use the last fetched row as reference and further continue from that point
[] with insert and delete it produce consistent result
[] It does not slowed even with big bulky data


o Supported by the idx_jobs_created_at 
o explain analyze verified time complexity O(log n) for cursor based pagination and O(n) for offset based pagination

Trade off : It cannot jumps on particular rows so good for infinite scroll,feeds.
for admin dashboards requiring page no. so offset is appropriate

In of ('/jobs/cursor') I return{
    "items":items,
    "next_cursor":next_cursor,
    "has_more":has_more

}


### asyncpg over SQLAlchemy ORM
Raw asyncpg gives full SQL control. Every query is intentional.
Connection pooling: min=2, max=10. Context manager pattern prevents leaks.

### Transactions for multi-step writes
Job creation (insert job + link skills) wrapped in a transaction.
Partial failure impossible — either all succeed or none do.

### Composite indexes
```sql
CREATE INDEX idx_jobs_status_created ON jobs(status, created_at DESC);
```
Covers both the status filter and created_at ordering in a single index scan.


## Project Structure

```
job-board-api/
├── main.py          # app, middleware, exception handlers
├── db.py            # asyncpg connection pool
├── models.py        # Pydantic request/response schemas
├── exceptions.py    # typed domain exceptions
├── dependencies.py  # FastAPI Depends() providers
├── services/        # business logic + SQL (no HTTP)
│   ├── jobs.py
│   ├── companies.py
│   ├── applications.py
│   └── analytics.py
├── routes/          # thin HTTP handlers (no SQL)
│   ├── jobs.py
│   ├── companies.py
│   ├── applications.py
│   └── analytics.py
└── migrations/      # Alembic migration files
```