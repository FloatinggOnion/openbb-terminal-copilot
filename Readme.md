# OpenBB Copilot For Terminal

This is a submission for the OpenBB 2024 Hacktoberfest event.

### About
I built this integration of Google Gemini into the copilot, including streaming responses.

### Setup and Installation
- Clone/fork the repository
- Install the requirements
    - `pip install -r requirements.txt` with pip, or...
    - `pipenv install` if you're using pipenv
- Run the app: `fastapi dev`

### Files
- `main.py`: Main entry way into the app. FastAPI application
- `prompt.py`: Contains the `SYSTEM_PROMPT` template
- `models.py`: Contains the models used for the API
- `utils.py`: Contains helper functions for the API