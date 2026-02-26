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
            "import json\n"
            "from http.server import BaseHTTPRequestHandler, HTTPServer\n\n"
            "def health() -> dict[str, str]:\n"
            "    return {'status': 'ok'}\n\n"
            "class Handler(BaseHTTPRequestHandler):\n"
            "    def do_GET(self):\n"
            "        if self.path != '/health':\n"
            "            self.send_response(404)\n"
            "            self.end_headers()\n"
            "            return\n"
            "        payload = json.dumps(health()).encode('utf-8')\n"
            "        self.send_response(200)\n"
            "        self.send_header('Content-Type', 'application/json')\n"
            "        self.send_header('Content-Length', str(len(payload)))\n"
            "        self.end_headers()\n"
            "        self.wfile.write(payload)\n\n"
            "def run() -> None:\n"
            "    server = HTTPServer(('0.0.0.0', 8000), Handler)\n"
            "    server.serve_forever()\n\n"
            "if __name__ == '__main__':\n"
            "    run()\n",
            encoding="utf-8",
        )
        files.append(str(app_py.relative_to(project_root)))

        reqs = project_root / "requirements.txt"
        reqs.write_text("# No third-party dependencies required\n", encoding="utf-8")
        files.append(str(reqs.relative_to(project_root)))

        tests = project_root / "test_app.py"
        tests.write_text(
            "from app import health\n\n"
            "def test_health():\n"
            "    assert health() == {'status': 'ok'}\n",
            encoding="utf-8",
        )
        files.append(str(tests.relative_to(project_root)))

        manifest = project_root / "intent_manifest.json"
        manifest.write_text(json.dumps(requirements, indent=2), encoding="utf-8")
        files.append(str(manifest.relative_to(project_root)))

        return files
