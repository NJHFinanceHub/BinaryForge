REQUIRED_KEYS = ["project_name", "app_type", "target_users"]


class DialogManager:
    def next_prompt(self, requirements: dict) -> tuple[str, bool]:
        missing = [key for key in REQUIRED_KEYS if not requirements.get(key)]
        if missing:
            questions = {
                "project_name": "What should the project be called?",
                "app_type": "Should this be a web app, API service, or CLI tool?",
                "target_users": "Who are the primary users?",
            }
            first = missing[0]
            return questions[first], False

        if not requirements.get("features"):
            return "List the core features you want (e.g., auth, dashboard, api, search).", False

        return "Great — requirements look complete. Say 'generate' when ready.", True
