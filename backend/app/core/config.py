from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
GENERATED_DIR = BASE_DIR / "generated_projects"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)
