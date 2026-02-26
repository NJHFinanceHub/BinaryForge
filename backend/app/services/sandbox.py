from __future__ import annotations

import subprocess
from pathlib import Path


class SandboxRunner:
    def verify(self, project_root: Path) -> dict:
        checks = []

        py_compile = subprocess.run(
            ["python", "-m", "py_compile", str(project_root / "app.py")],
            capture_output=True,
            text=True,
            timeout=20,
        )
        checks.append(
            {
                "name": "python_compile",
                "passed": py_compile.returncode == 0,
                "stdout": py_compile.stdout,
                "stderr": py_compile.stderr,
            }
        )

        pytest_run = subprocess.run(
            ["pytest", "-q", str(project_root / "test_app.py")],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=project_root,
        )
        checks.append(
            {
                "name": "pytest",
                "passed": pytest_run.returncode == 0,
                "stdout": pytest_run.stdout,
                "stderr": pytest_run.stderr,
            }
        )

        return {
            "passed": all(c["passed"] for c in checks),
            "checks": checks,
        }
