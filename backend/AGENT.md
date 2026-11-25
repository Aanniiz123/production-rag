# Backend Agent Guide

## Project purpose

Build a production-grade RAG platform using FastAPI.

The backend contains an API gateway and independent auth, ingestion,
notification, and RAG engine services. External HTTP traffic enters through
the API gateway.

## Technology stack

- Python 3.13
- FastAPI
- Pydantic v2
- PostgreSQL
- asyncpg
- SQLAlchemy
- Alembic
- Docker Compose
- HTTPX
- OAuth 2.0/OpenID Connect
- JWT
- GROQ API

## Repository structure

src/
  api_gateway/
    app.py
    router/
    dependencies/
    clients/
  auth/
    models/
    services/
  ingestion/
  rag_engine/
  notification/
core/
  config.py
  database.py
main.py
docker-compose.yml
requirements.txt
alembic/

## Architecture rules

- The API gateway is the only public HTTP entry point.
- `src/api_gateway/app.py` creates and configures the FastAPI application.
- Gateway routers should only handle HTTP concerns and delegate domain logic.
- Auth, ingestion, RAG, and notification code must remain separated.
- Use asynchronous database operations and HTTP calls.
- Return Pydantic models for stable API responses.
- Use `/api/v1` route prefixes.
- Access data only with a tenant ID derived from authentication.
- Never trust client-provided user or tenant identity headers.
- Notifications and ingestion should use events or queues for asynchronous work.
- Do not make a notification or RAG call hidden inside a document-upload transaction.

## Authentication rules

- Use OAuth 2.0 Authorization Code flow with PKCE for browser users.
- Store refresh tokens only in Secure, HttpOnly, SameSite cookies.
- Never store OAuth secrets or access tokens in local storage.
- Validate JWTs using provider JWKS keys.
- Verify signature, expiry, issuer, audience, and not-before values.
- Cache JWKS keys and support key rotation.
- Keep access tokens short-lived.
- Separate OAuth scopes from application roles and permissions.
- Gateway authentication dependencies belong under
  `src/api_gateway/dependencies/`.
- Provider communication belongs under `src/auth/services/`.

## PostgreSQL rules

- Use `DATABASE_URL` from environment variables.
- For a FastAPI process outside Docker:
  `postgresql+asyncpg://postgres:postgres@localhost:5432/production_rag`
- For FastAPI inside Docker Compose:
  `postgresql+asyncpg://postgres:postgres@postgres:5432/production_rag`
- Use SQLAlchemy sessions through FastAPI dependencies.
- Use Alembic for every database schema change.
- Never execute raw DDL at application startup.
- Always add migration downgrade operations.

## Configuration rules

- Use `pydantic-settings` and `BaseSettings`.
- `.env` must remain untracked.
- Add `.env.example` with placeholder values.
- Never print secrets or include secrets in responses and logs.
- Revoke credentials immediately if they are exposed.
- Use Docker secrets or an external secret manager in production.

## API conventions

- Use `401` for missing or invalid authentication.
- Use `403` for an authenticated user lacking permission.
- Use `404` for a resource not found within the current tenant.
- Use `202 Accepted` for queued ingestion work.
- Use Pydantic input and output models.
- Add a correlation ID to every request and downstream call.
- Add `GET /health/live` and `GET /health/ready` endpoints.

## Error handling

- Use FastAPI `HTTPException` for expected API errors.
- Map downstream HTTP and timeout failures to stable gateway responses.
- Log exceptions with correlation IDs.
- Do not expose stack traces or internal URLs to clients.

## Testing requirements

Add tests for:

- JWT verification
- Expired and invalid JWT rejection
- Missing permissions
- Cross-tenant access prevention
- Auth callback handling
- Database migrations
- RAG and ingestion route behavior
- Downstream timeout behavior

Run the smallest relevant test suite first.

## Commands

Start PostgreSQL:

```powershell
docker compose up -d postgres
docker compose ps