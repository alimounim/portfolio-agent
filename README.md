# Portfolio AI Agent

A personal portfolio site with a built-in AI chat agent. Visitors (recruiters, hiring managers, collaborators) can ask about my background, experience, projects, and skills, and the agent answers in my voice, grounded only in the information I've given it.

Built with Python, Flask, and the Anthropic Claude API.

## Features

- **Conversational agent** that answers questions in first person, using a curated bio as its only source of truth, so it says "I don't know" instead of inventing details
- **Per-visitor conversation memory**: each browser session gets its own history, so follow-up questions work and visitors never see each other's chats
- **Multi-page site** (Home/Chat, Projects, Certifications, Research) using Jinja2 template inheritance
- **Project cards** that expand on hover and link to each project's GitHub repo
- **Markdown rendering** of agent replies (via marked.js), so lists and formatting display cleanly
- **Resume download** and social links on the home page

## Tech Stack

| Layer | Tools |
|---|---|
| Backend | Python, Flask, Gunicorn |
| AI | Anthropic Claude API (`anthropic` SDK) |
| Frontend | HTML, CSS, JavaScript, Jinja2, marked.js |
| Config | python-dotenv |
| Deployment | Render (`Procfile`) |

## Project Structure

```
portfolio-agent/
├── app.py              # Flask app: page routes + /chat endpoint
├── about_ali.py        # BIO: the agent's knowledge base
├── test_agent.py       # Early terminal version of the agent
├── templates/          # base.html + one template per page
├── static/
│   ├── files/          # resume.pdf
│   └── images/         # avatar
├── requirements.txt
├── Procfile            # web: gunicorn app:app
└── JOURNAL.md          # Build log: what I did, why, and what I learned
```

## How It Works

1. The visitor sends a message from the chat page to the `/chat` endpoint.
2. Flask assigns the visitor a session ID and looks up their conversation history.
3. The app sends the full history to Claude, along with a system prompt made of the bio in `about_ali.py` plus guidelines on tone and honesty.
4. The reply is saved to that visitor's history and returned to the page, where it is rendered as Markdown.

## Running Locally

1. Clone the repo and create a virtual environment:

   ```bash
   git clone https://github.com/alimounim/portfolio-agent.git
   cd portfolio-agent
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root with your Anthropic API key:

   ```
   ANTHROPIC_API_KEY=your-key-here
   ```

3. Start the app:

   ```bash
   python app.py
   ```

   Then open http://localhost:5000.

## Deployment

The app is deployed on Render and run with Gunicorn (see `Procfile`). The API key is set as an environment variable in Render, not committed to the repo.

## Build Journal

See [JOURNAL.md](JOURNAL.md) for a dated log of how this project came together, including the bugs I hit and what I learned from each step.
