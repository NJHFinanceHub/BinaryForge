import re
from html import escape

FEATURE_KEYWORDS = [
    "authentication",
    "dashboard",
    "api",
    "payments",
    "notifications",
    "search",
    "admin",
    "analytics",
    "crud",
]


class IntentParser:
    @staticmethod
    def sanitize(text: str) -> str:
        return escape(text.strip())

    def extract(self, text: str, current: dict) -> dict:
        safe = self.sanitize(text).lower()
        updated = dict(current)

        project_name_match = re.search(r"(?:called|named)\s+([a-z0-9\-_ ]{3,40})", safe)
        if project_name_match and not updated.get("project_name"):
            updated["project_name"] = project_name_match.group(1).strip().title().replace(" ", "-")

        if "web app" in safe or "website" in safe:
            updated["app_type"] = "web"
        elif "api" in safe:
            updated["app_type"] = "api"
        elif "cli" in safe:
            updated["app_type"] = "cli"

        detected = [k for k in FEATURE_KEYWORDS if k in safe]
        updated["features"] = sorted(set(updated.get("features", []) + detected))

        if "for" in safe and not updated.get("target_users"):
            frag = safe.split("for", 1)[1][:80]
            updated["target_users"] = frag.strip(" .")

        if "deploy" in safe:
            if "kubernetes" in safe:
                updated["deployment_target"] = "kubernetes"
            elif "docker" in safe:
                updated["deployment_target"] = "docker"
            else:
                updated["deployment_target"] = "vm"

        return updated
