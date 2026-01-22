🤖 AI Code Reviewer — Full-Stack AI SaaS

AI-powered code review platform that analyzes local files, ZIP projects, GitHub repositories, and Pull Requests using LLMs — built end-to-end with FastAPI, React, authentication, database, and GitHub integrations.

🚀 Why This Project

This project demonstrates my ability to design and build a real-world AI SaaS, not just a demo app.

It covers:

Secure authentication & authorization

Database-backed user features

AI/LLM integration with structured outputs

GitHub API integrations (repos + PRs)

End-to-end full-stack ownership

✨ Key Features
🔐 Authentication & Security

JWT-based authentication (signup / login)

Password hashing with bcrypt

Protected APIs with ownership checks

🧠 AI Code Review

Detects bugs, security issues, performance problems

Provides explanations + suggested improvements

Structured AI output (frontend-safe)

📂 Multiple Input Types

Single file upload (.py, .js, .ts, .java)

ZIP project upload (multi-file analysis)

GitHub repository analysis

GitHub Pull Request review (diff-aware)

🧾 User Data Management

Persistent review history per user

Delete individual or all reviews

Results stored as JSON for flexibility

🔗 GitHub Integration (Advanced)

Analyze public & private repositories

Analyze Pull Requests only on changed files

Uses:

GitHub REST API

PR diff + full-file context

Defensive handling of:

Large PRs

Missing patches

API pagination

Rate limits

🏗️ Architecture (High Level)
React Frontend
   ↓
FastAPI Backend
   ├── Auth (JWT)
   ├── AI Review Engine
   ├── GitHub Repo & PR APIs
   ├── Review History
   ↓
Database (Users & Reviews)

🛠️ Tech Stack

Backend

Python, FastAPI

SQLAlchemy

JWT Authentication

GitHub REST API

LLM integration (Ollama / OpenAI-compatible)

Frontend

React (Vite)

Fetch API

Minimal, clean MVP UI

Database

SQLite (dev)

PostgreSQL-ready schema

📁 Project Structure
backend/
 ├── main.py
 ├── auth_routes.py
 ├── auth_utils.py
 ├── jwt_utils.py
 ├── models.py
 ├── ai_review.py
 ├── github_utils.py
 ├── github_pr_utils.py

frontend/
 ├── App.jsx
 ├── api.js
 ├── Login.jsx
 ├── Signup.jsx
 └── components/

🧠 What This Shows Recruiters

This project demonstrates:

✅ Full-stack development (frontend + backend)

✅ Secure authentication & API protection

✅ Database design & data ownership

✅ AI prompt engineering with structured output

✅ External API integration (GitHub)

✅ Real SaaS feature evolution

✅ Debugging & defensive programming

This is not a tutorial project — it reflects how production developer tools are built.

🚀 Future Enhancements (Planned)

GitHub OAuth (replace personal tokens)

Inline PR comments

Webhooks for automatic PR review

Usage limits & billing

Team accounts

CI-based PR blocking on high severity issues

📌 How to Run (Quick)
# Backend
uvicorn main:app --reload

# Frontend
npm install
npm run dev

👨‍💻 Author

Built as part of a build-in-public journey focused on:

AI engineering

Backend systems

SaaS architecture

Developer tooling

⭐ If you’re a recruiter

This project reflects how I approach:

Problem decomposition

Feature prioritization

Security

Scalability

Real-world constraints
