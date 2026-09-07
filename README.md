# 📚 AI Study Pack Generator

A practice Generative AI application built with:

- Python
- Streamlit
- Google Gemini API
- Gemini 3.6 Flash
- Prompt chaining
- Modular/multi-file architecture

## Workflow

User input → Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Final Study Pack

### Stage 1
Understand the topic and create a learning blueprint.

### Stage 2
Use the Stage 1 output as context and generate study notes.

### Stage 3
Use the Stage 2 notes to create important exam questions.

### Stage 4
Use the Stage 2 notes to create a quiz.

### Stage 5
Combine all stage outputs into one final study pack.

## Project Structure

```text
ai-study-pack-generator/
├── app.py
├── ai_service.py
├── prompts.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── secrets.toml.example
```

## Run locally

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install:

```bash
pip install -r requirements.txt
```

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
GEMINI_API_KEY = "your_real_key_here"
```

Run:

```bash
streamlit run app.py
```

## GitHub

```bash
git init
git add .
git commit -m "Build AI Study Pack Generator"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

## Streamlit Community Cloud

1. Push the project to GitHub.
2. Sign in to Streamlit Community Cloud with GitHub.
3. Create a new app.
4. Select your repository and `main` branch.
5. Set the main file to `app.py`.
6. Open Advanced settings → Secrets.
7. Add:

```toml
GEMINI_API_KEY = "your_real_key_here"
```

8. Deploy.

Do not upload `.streamlit/secrets.toml` to GitHub.
