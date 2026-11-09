# AI Content Studio

A responsive AI-powered content generator built with **Python, Flask, HTML, CSS, JavaScript, and the Google Gemini API**.

Generate platform-ready:
- Instagram captions
- LinkedIn posts
- Blog introductions

Customize the writing tone, audience, language, length, and keywords. The app returns structured JSON containing a title, content, hashtags, and practical publishing tips.

## Features

- Three content formats: Instagram, LinkedIn, and blog introduction
- Six writing tones
- Short, medium, and long content lengths
- English, Urdu, Roman Urdu, and mixed language options
- Target audience and optional keywords
- Gemini API integration through the official `google-genai` Python SDK
- System instructions and reusable user prompt template
- Structured JSON output using a response schema
- Loading, validation, and API error states
- Copy generated content and hashtags
- Responsive interface for desktop and mobile
- API key stored in `.env`, never in frontend code

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python, Flask |
| AI | Google Gemini API |
| SDK | `google-genai` |
| Configuration | `python-dotenv` |

## Project structure

```text
ai-content-studio/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
└── screenshots/
    └── (add your screenshots here)
```

## 1. Requirements

- Python 3.10 or newer (Python 3.12 recommended)
- Internet connection
- Gemini API key

Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

## 2. Open the project folder

Open this folder in VS Code, then open its integrated terminal.

## 3. Create and activate a virtual environment

### Windows PowerShell

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```cmd
venv\Scripts\activate.bat
```

If you use Git Bash:

```bash
source venv/Scripts/activate
```

## 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Configure your Gemini API key

Create a copy of `.env.example` and name it `.env`.

Open `.env` and replace the placeholder:

```env
GEMINI_API_KEY=your_actual_api_key
GEMINI_MODEL=gemini-2.5-flash
```

Do not add quotation marks around the key. Never upload `.env` to GitHub.

If the configured model is unavailable to your API project, replace `GEMINI_MODEL` with a model currently available in your Google AI Studio account.

## 6. Run the application

```bash
python app.py
```

Open this address in your browser:

```text
http://127.0.0.1:5000
```

Keep the terminal running while using the application. Press `Ctrl + C` to stop the Flask development server.

## 7. How to use

1. Choose Instagram, LinkedIn, or Blog.
2. Enter a topic.
3. Select a writing tone and content length.
4. Add an audience and optional keywords.
5. Choose the output language.
6. Click **Generate content**.
7. Review the generated content, hashtags, and tips.
8. Copy the result and edit it in your own voice before publishing.

## API endpoint

`POST /api/generate`

Example request:

```json
{
  "topic": "My journey learning Python and Generative AI",
  "content_type": "linkedin",
  "tone": "professional",
  "length": "medium",
  "audience": "Students and beginner developers",
  "language": "English",
  "keywords": "learning, consistency, building projects"
}
```

The endpoint returns a JSON object with `result` and `meta` fields. The result contains `title`, `content`, `hashtags`, and `tips`.

Health check:

`GET /api/health`

## Prompt engineering used

- **System instruction:** defines the assistant's role, writing rules, and platform-specific guidance.
- **User prompt template:** inserts the topic, platform, tone, audience, language, length, and keywords.
- **Structured output:** Gemini is configured to return JSON matching a schema. The backend parses the structured response before sending it to the frontend.

## Error handling

The backend validates user input and handles missing API keys, authentication problems, quota/rate errors, unexpected AI responses, and general API failures. The frontend displays loading and error states.

## Screenshots and demo video

After running the project:

1. Capture the initial interface.
2. Generate an Instagram caption.
3. Generate a LinkedIn post with a different tone.
4. Capture the generated result and hashtags.
5. Save screenshots in the `screenshots/` folder.
6. Record a short screen demo showing topic entry, generation, and copy actions.

Suggested demo length: 30–45 seconds.

## GitHub upload

Create a new public repository named `ai-content-studio`.

Before pushing, check that `.env` is not staged or committed:

```bash
git status
git add .
git commit -m "Build AI Content Studio with Gemini API"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ai-content-studio.git
git push -u origin main
```

Replace the remote URL with your own repository URL.

## Important notes

- This is a learning and portfolio project. Review generated content before publishing.
- API availability, quotas, and model access depend on your Google AI Studio account.
- The Flask development server is for local development, not production deployment.
- Never expose API keys in browser JavaScript, screenshots, or public repositories.

## Learning outcomes

This project demonstrates practical use of:
- LLM APIs
- System and user prompts
- Prompt templates
- Structured JSON output
- Python backend development
- Frontend-to-backend API communication
- Input validation and error handling

---

Built as a Generative AI learning project.

**Learn • Build • Create**
