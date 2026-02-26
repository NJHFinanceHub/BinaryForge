from __future__ import annotations

from pathlib import Path
import json


class ProjectGenerator:
    def generate(self, project_root: Path, requirements: dict) -> list[str]:
        project_root.mkdir(parents=True, exist_ok=True)
        files: list[str] = []

        readme = project_root / "README.md"
        readme.write_text(
            f"# {requirements['project_name']}\n\n"
            f"Generated project for {requirements['target_users']}.\n\n"
            f"## Features\n" + "\n".join(f"- {f}" for f in requirements['features']) + "\n",
            encoding="utf-8",
        )
        files.append(str(readme.relative_to(project_root)))

        app_py = project_root / "app.py"
        app_py.write_text(
            "from flask import Flask, jsonify\n\n"
            "app = Flask(__name__)\n\n"
            "@app.get('/health')\n"
            "def health():\n"
            "    return jsonify({'status': 'ok'})\n\n"
            "if __name__ == '__main__':\n"
            "    app.run(host='0.0.0.0', port=8000)\n",
            encoding="utf-8",
        )
        files.append(str(app_py.relative_to(project_root)))

        reqs = project_root / "requirements.txt"
        reqs.write_text("flask==3.0.3\n", encoding="utf-8")
        files.append(str(reqs.relative_to(project_root)))

        tests = project_root / "test_app.py"
        tests.write_text(
            "from app import app\n\n"
            "def test_health():\n"
            "    client = app.test_client()\n"
            "    res = client.get('/health')\n"
            "    assert res.status_code == 200\n",
            encoding="utf-8",
        )
        files.append(str(tests.relative_to(project_root)))

        manifest = project_root / "intent_manifest.json"
        manifest.write_text(json.dumps(requirements, indent=2), encoding="utf-8")
        files.append(str(manifest.relative_to(project_root)))

        return files
