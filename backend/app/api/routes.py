from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from uuid import uuid4
import shutil

from app.core.config import GENERATED_DIR
from app.models.schemas import ChatMessage, ChatResponse, GenerateResponse, SessionCreateResponse
from app.services.dialog_manager import DialogManager
from app.services.intent_parser import IntentParser
from app.services.project_generator import ProjectGenerator
from app.services.sandbox import SandboxRunner
from app.services.session_store import store

router = APIRouter(prefix="/api")
parser = IntentParser()
dialog = DialogManager()
generator = ProjectGenerator()
sandbox = SandboxRunner()


@router.post("/session", response_model=SessionCreateResponse)
def create_session() -> SessionCreateResponse:
    return SessionCreateResponse(session_id=store.create())


@router.post("/chat/{session_id}", response_model=ChatResponse)
def chat(session_id: str, body: ChatMessage) -> ChatResponse:
    try:
        session = store.get(session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    session.messages.append({"role": "user", "content": body.message})
    session.requirements = parser.extract(body.message, session.requirements)
    prompt, ready = dialog.next_prompt(session.requirements)
    session.messages.append({"role": "assistant", "content": prompt})
    return ChatResponse(
        session_id=session_id,
        assistant_message=prompt,
        extracted_requirements=session.requirements,
        ready_to_generate=ready,
    )


@router.post("/generate/{session_id}", response_model=GenerateResponse)
def generate(session_id: str) -> GenerateResponse:
    try:
        session = store.get(session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    if not session.requirements.get("project_name"):
        raise HTTPException(status_code=400, detail="Insufficient requirements")

    project_id = f"{session.requirements['project_name'].lower()}-{uuid4().hex[:8]}"
    project_path = GENERATED_DIR / project_id
    files = generator.generate(project_path, session.requirements)
    verification = sandbox.verify(project_path)
    shutil.make_archive(str(project_path), "zip", root_dir=project_path)

    return GenerateResponse(
        project_id=project_id,
        project_path=str(project_path),
        verification=verification,
        files=files,
    )


@router.get("/projects/{project_id}/download")
def download(project_id: str) -> FileResponse:
    artifact = GENERATED_DIR / f"{project_id}.zip"
    if not artifact.exists():
        raise HTTPException(status_code=404, detail="Artifact not found")
    return FileResponse(artifact, media_type="application/zip", filename=f"{project_id}.zip")
