# Miniature-Engine
Miniature-Engine is a Python-based program that automatically generates AI-driven text content. It offers an upgraded approach compared to modern AI text generators, delivering faster, smarter, and more adaptive text generation for diverse use cases such as writing, coding, and conversational AI.
# Web Spell & Structure Tool (Ready-to-upload)

A small Flask web app that detects spelling mistakes, offers suggestions, and provides simple sentence-structure hints.

## What's included
- `app.py` — Flask backend with an API endpoint `/api/check`
- `suggestions.py` — Spell checking (pyspellchecker) + optional grammar (language-tool-python) + safe fallbacks
- `templates/index.html` — Simple web UI
- `static/css/style.css` and `static/js/main.js` — Frontend assets
- `requirements.txt`, `.gitignore`, `LICENSE`, `Procfile`

## Requirements
- Python 3.8+
- pip
- (Optional, for grammar/structure suggestions) Java (OpenJDK) and `language-tool-python`

## Local setup (recommended)

```bash
# create virtual env
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate    # Windows (PowerShell use: venv\\Scripts\\Activate.ps1)

# install Python dependencies
pip install -r requirements.txt

# if you want grammar suggestions (optional), install Java and then:
# pip install language-tool-python
# On Ubuntu/Debian: sudo apt-get install openjdk-11-jdk -y
# On macOS (with Homebrew): brew install openjdk

# run the app
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Quick test (curl)
```bash
curl -X POST -H "Content-Type: application/json" -d '{"text":"Thiss is a smple sentense with very longsentence that might be splitted and was asked to check."}' http://127.0.0.1:5000/api/check
```

## Upload to GitHub (commands)
Replace `USERNAME` and `REPO` with your GitHub username and desired repo name.

```bash
git init
git branch -M main
git add .
git commit -m "Initial commit — Web Spell & Structure Tool"
# Option A: Create repo on GitHub website, then:
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main

# Option B: Using GitHub CLI (recommended)
# gh auth login
gh repo create USERNAME/REPO --public --source=. --remote=origin --push
```

## Notes & troubleshooting
- If the grammar tool doesn't show suggestions it's usually because Java is missing; install OpenJDK and restart the app.
- If you want to use an LLM (OpenAI) to rewrite sentences, add your API key and update `suggestions.py`. (I can provide that variant if you'd like.)
