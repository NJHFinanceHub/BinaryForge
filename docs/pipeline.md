# Intent-to-Software Pipeline

1. **Intent Capture**: User submits natural language requirements in the web UI.
2. **Dialog Refinement**: Backend extracts structured fields and asks targeted follow-up questions.
3. **Requirement Snapshot**: The current requirement state is persisted in-memory per session.
4. **Project Generation**: A scaffolded runnable project is generated with app code, tests, and manifest.
5. **Verification**: Sandbox runner compiles and tests generated software, then returns pass/fail details.
6. **Artifact Delivery**: Generated project is zipped and made available through the download API.

## Extensibility Points
- Swap `IntentParser` for LLM-backed extraction.
- Add provider adapters for multi-language project templates.
- Replace local subprocess execution with isolated Docker/Kubernetes jobs.
