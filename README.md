# CyberBot

CyberBot is a small cybersecurity-awareness chatbot built with Flask and scikit-learn. It classifies a question into one of the topics in the local training dataset and returns practical, topic-specific guidance through a browser-based chat interface.

## What it covers

- Phishing and social engineering
- Malware and safer browsing
- Passwords and multi-factor authentication
- Public Wi-Fi and encryption
- Software updates and incident reporting

The interface includes suggested questions, a responsive conversation view, and a new-chat control. The model runs locally; it does not send prompts to an external AI service.

## Requirements

- Python 3.11 or newer
- `pip`

## Setup and run

Open a terminal in the project directory, then create and activate a virtual environment.

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install Flask scikit-learn
python app.py
```

If PowerShell prevents activation, allow it for the current terminal session and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install Flask scikit-learn
python app.py
```

When Flask reports that it is running, open [http://127.0.0.1:5000/chat](http://127.0.0.1:5000/chat). Stop the development server with `Ctrl+C`.

## Project layout

```text
app.py                     Flask routes and JSON response endpoint
ML/mlScript.py             Intent classifier and topic guidance
dataset/cybersecurity.json Training phrases grouped by intent
templates/index.html       Chat interface and browser-side behavior
static/styles/style.css    Responsive interface styling
```

## How it works

1. The browser sends a question to `/bot/response/`.
2. The scikit-learn pipeline compares the text with example phrases in `dataset/cybersecurity.json` and predicts an intent.
3. Low-confidence predictions receive a clarification message rather than an unrelated topic answer.
4. A reviewed response for the selected topic is returned as JSON.

The classifier is intentionally lightweight and is not a generative AI model. It can misunderstand unusual wording, and its guidance is general rather than a substitute for professional security support. For an active incident, contact your organization's IT/security team or the relevant service provider.

## Customizing the bot

Add representative example questions to the appropriate `patterns` list in `dataset/cybersecurity.json`. Keep examples distinct between topics to reduce ambiguous predictions. Topic guidance is maintained in `TOPIC_RESPONSES` in `ML/mlScript.py`; review advice carefully before changing it. Restart the Flask app after edits so the model reloads the training data.

## Troubleshooting

- **Python command not found on Windows:** install Python and use the `py` launcher (`py -3`), or update the Python installation and PATH settings.
- **Activation is blocked:** use the PowerShell process-scoped execution policy command above, or invoke `.venv\Scripts\python.exe app.py` without activating the environment.
- **Port 5000 is already in use:** stop the other local server or change the port in the `app.run` call in `app.py`.

## Contributing

Contributions are welcome. Please make focused changes, keep training examples representative, and verify the app locally before submitting a pull request.

## Contact

Farhan