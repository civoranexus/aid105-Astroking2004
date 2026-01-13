# 🚀 CivoraX Internship Program 2025-26

<p align="center">
  <img src="https://internship.civoranexus.com/CivoraX.png" alt="CivoraX Logo" width="200"/>
</p>

<p align="center">
  <strong>Launch your tech career with real projects, expert mentorship, and industry-recognized certification</strong>
</p>



<p align="center">
  <img src="https://img.shields.io/badge/Duration-5%20Weeks-blue" alt="Duration"/>
  <img src="https://img.shields.io/badge/Start%20Date-Jan%205%2C%202026-green" alt="Start Date"/>
  <img src="https://img.shields.io/badge/End%20Date-Feb%208%2C%202026-orange" alt="End Date"/>
  <img src="https://img.shields.io/badge/Mode-Remote--First-purple" alt="Mode"/>
</p>

---

## 📊 Program Statistics

| Metric | Value |
|--------|-------|
| 🎓 Interns Trained | 300+ |
| 💼 Live Projects | 20 |
| ⏱️ Program Duration | 5 Weeks |

---


## 📅 Program Details

| Detail | Information |
|--------|-------------|
| **Duration** | 5-week intensive program |
| **Dates** | January 5 - February 8, 2026 |
| **Format** | Remote-first with live sessions and workshops |
| **Structure** | Real-time project work with weekly milestones |

---

## ✅ Eligibility Criteria

- ✔️ Students from **any year or degree program**
- ✔️ Recent graduates and **career switchers** welcome
- ✔️ **Basic programming knowledge** required
- ✔️ Strong **passion for technology** and learning

---

## 🛠️ Technologies You'll Master

| Category | Technologies |
|----------|-------------|
| **Frontend** | React, Next.js |
| **Backend** | Node.js, Python |
| **Advanced** | AI & Machine Learning |
| **Infrastructure** | Cloud & DevOps |
| **Mobile** | Cross-platform Development |
| **Database** | SQL & NoSQL Systems |
| **APIs** | RESTful & GraphQL |
| **Workflow** | Agile & Git |

---

## 📋 Application Process

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   01. Register  │───▶│  02. Team       │───▶│  03. Receive    │
│   Online        │    │  Review         │    │  Confirmation   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

1. **📝 Register Online** - Complete your application form with details and preferences
2. **🔍 CivoraX Team Review** - Our team reviews your application and qualifications
3. **✉️ Eligibility Email** - Receive confirmation email if selected



## 📞 Contact Information

| Channel | Details |
|---------|---------|
| 📧 **Email** | [contact@civoranexus.com](mailto:contact@civoranexus.com) |
| 📱 **Phone** | [+91 7350675192](tel:+917350675192) |
| 📍 **Location** | 422605, Sangamner, Maharashtra, India |

### 🔗 Social Links

[![LinkedIn](https://img.shields.io/badge/LinkedIn-CivoraX-blue?style=flat&logo=linkedin)](https://www.linkedin.com/company/civoranexus)
[![Instagram](https://img.shields.io/badge/Instagram-CivoraX-E4405F?style=flat&logo=instagram)](https://www.instagram.com/civoranexus)
[![Twitter](https://img.shields.io/badge/Twitter-CivoraX-1DA1F2?style=flat&logo=twitter)](https://twitter.com/civoranexus)
[![YouTube](https://img.shields.io/badge/YouTube-CivoraX-FF0000?style=flat&logo=youtube)](https://www.youtube.com/@civoranexus)

---

## 🏢 About Civora Nexus

**Civora Nexus Pvt. Ltd.** is a technology company empowering communities through innovative civic and healthcare technology solutions.

### Company Services:
- 🔄 Digital Transformation for Businesses
- 🏘️ Smart Community & Enterprise Solutions
- 💡 Affordable Tech Solutions
- 📊 Data Analytics & Business Insights
- 🎓 Innovation & Skill Development
- 🤖 AI & Automation Solutions

---

## 📚 Quick Links

- 🌐 [Official Website](https://civoranexus.com/)
- 📋 [Internship Portal](https://civoranexus.com/internships)
- 🔐 [Certificate Verification](https://internship.civoranexus.com)
- 📄 [Privacy Policy](https://civoranexus.com/privacy-policy)
- 📜 [Terms of Service](https://civoranexus.com/terms-and-conditions)



<p align="center">
  <strong>© 2025 Civora Nexus Pvt. Ltd. All rights reserved.</strong>
</p>

<p align="center">
  Made with ❤️ by CivoraX Team
</p>

---

## SchemeAssist

SchemeAssist is a small FastAPI backend with a Vite + React frontend demonstrating a recommendation flow for sample "schemes".

This repository contains two primary subprojects:

- `src/backend` — FastAPI backend, SQLAlchemy models, and Alembic migrations.
- `frontend` — Vite + React frontend that proxies `/api` to the backend in development.

This README consolidates quickstart instructions for both frontend and backend.

### Quickstart — Backend

Prerequisites: Python 3.10+ and a virtual environment.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate
pip install -r src/backend/requirements.txt
```

Run locally (reloads on change):

```bash
uvicorn src.backend.main:app --reload --host 127.0.0.1 --port 8000
```

Useful endpoints:

- `GET /health` — health check
- `GET /schemes` — list sample schemes
- `POST /recommendations` — send a user profile JSON to receive ranked schemes

### Quickstart — Frontend

Prerequisites: Node.js (16+) and npm.

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server proxies `/api` to `http://127.0.0.1:8000` by default — start the backend first.

Run frontend tests (Vitest):

```bash
cd frontend
npm run test -- --run
```

### Development Notes

- The frontend lives in `/frontend` and uses React Router and axios (proxied in dev).
- The backend is in `/src/backend` using FastAPI, SQLAlchemy and Alembic (migrations in `/alembic`).
- For local development the app uses SQLite by default; set `DATABASE_URL` to your Postgres URL for production.

### Documentation

This project centralizes documentation in this file. Subfolders contain short pointers to this README.

### License

See the `LICENSE` file in the repo root for licensing information.
