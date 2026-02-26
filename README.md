# Intent-to-Executable Software Platform

A full-stack platform that transforms natural language software intent into runnable, verified project artifacts.

## Architecture Plan

### Components
- **Frontend (React + Vite):** Chat interface for intent capture, requirement preview, and artifact download.
- **Backend (FastAPI):** Session management, dialog orchestration, requirement extraction, project generation, and artifact APIs.
- **Project Generator:** Produces runnable starter applications including tests and a machine-readable intent manifest.
- **Sandbox Verifier:** Executes compile and test checks on generated projects.
- **Artifact Store:** Persists generated projects and exposes ZIP download links.

### End-to-End Flow
1. User starts a session.
2. User describes project intent.
3. Backend extracts requirements and asks clarifying questions.
4. User triggers generation.
5. Generator emits source code + tests.
6. Sandbox runs verification checks.
7. User downloads verified artifact.

## Repository Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/routes.py
│   │   ├── core/config.py
│   │   ├── models/schemas.py
│   │   └── services/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── docs/pipeline.md
├── examples/minimal_todo/
├── scripts/bootstrap.sh
├── docker-compose.yml
└── .github/workflows/ci.yml
```

## Local Development

### 1) Bootstrap
```bash
./scripts/bootstrap.sh
```

### 2) Run Backend
```bash
uvicorn app.main:app --app-dir backend --reload --port 8000
```

### 3) Run Frontend
```bash
cd frontend
npm run dev
```

### 4) Run Tests
```bash
PYTHONPATH=backend pytest -q backend/tests
cd frontend && npm run test
```

## API Endpoints
- `POST /api/session` – create chat session
- `POST /api/chat/{session_id}` – submit intent message / get clarification
- `POST /api/generate/{session_id}` – generate and verify software project
- `GET /api/projects/{project_id}/download` – download generated ZIP artifact

## Security & Safety
- User input is sanitized before extraction.
- Generation verification runs via subprocess with timeouts.
- No dynamic code execution in control-plane backend.
- Manifest produced for traceability and debugging.

## Deployment
- **Docker Compose:** `docker compose up --build`
- **CI:** GitHub Actions workflow runs backend tests and frontend build/tests.

## Notes
This implementation is intentionally modular, so `IntentParser` and `ProjectGenerator` can be upgraded to LLM-backed and multi-template engines without API changes.
