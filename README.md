 # STEM in Yorùbá – Flask + (Groq or Gemini)

A responsive chat application that teaches STEM in Yorùbá with **multi-conversation memory**, **auth**, and **avatars**.

## Features
- 👤 Login/Signup with password hashing
- 🖼️ Profile photo upload at signup (shown next to your messages)
- 🗂️ Multiple chat histories per user (sidebar “+ New”; auto-title; rename endpoint)
- 🤖 AI persona **“Ede”** avatar for model replies
- 🔒 Auth-guarded routes
- 🧠 Memory stored per conversation in SQLite
- 🌐 Bilingual toggle (Yorùbá + optional English recap)
- 📱 Responsive UI (Bootstrap 5)

## Provider
Select one in `.env`: `PROVIDER=groq` (default) or `PROVIDER=gemini`.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env and paste your keys
```

## Run
```bash
python app.py
# open http://127.0.0.1:5000
```

## Endpoints
- `/` – Chat UI (requires login)
- `/signup`, `/login`, `/logout`
- `/conversations` (GET list, POST create)
- `/conversations/<id>/history`
- `/conversations/<id>/rename` (POST with {"title": "..."})
- `/chat` (POST message + conversation_id)
- `/reset_conversation` (POST with {"conversation_id": id})

## Notes
- Avatars saved to `uploads/`.
- DB file `chat.db` is created automatically.
- Change theme in `static/css/style.css`.
