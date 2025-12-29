# 🧠 Sprint Analyzer  
> AI-powered Sprint Analysis Agent for Agile Teams using JIRA or Manual Input

---

## 🚀 Overview

**Sprint Analyzer** is an AI-powered assistant that helps developers, QA, and project managers quickly **understand, assess, and prioritize sprint tickets**.  

It calculates **risk, complexity, dependencies**, and generates a **10-day execution plan** using an AI model (powered by **Groq** and **Llama 3.1**).  

Ideal for sprint planning, backlog grooming, or retrospectives.

---

## 🗂 Project Structure

sprint-analyzer/
│
├── agent.py # Orchestrator: runs the agent loop
├── fetcher.py # JIRA fetcher and API integration
├── memory.py # Memory, ticket scoring, risk calculation
├── thinker.py # AI reasoning via Groq LLM
├── actor.py # Console display & result saving
├── utils.py # Helper functions (score mapping, formatting)
├── requirements.txt # Python dependencies
├── .env # Stores GROQ API key & JIRA credentials
├── README.md
└── model/
└── data/ # AI-generated analysis results (auto-created per run)

vbnet
Copy code

Each run generates a **date-based folder** with a random ID to save results:

model/data/2025-12-29_ab12c/
└── sprint_analysis.txt

yaml
Copy code

---

## ⚙️ Installation Guide

### 🪟 Windows Setup

1. **Install Python 3.13+**  
   ```bash
   python --version
(Install via Microsoft Store or python.org)

Clone the repository

bash
Copy code
git clone https://github.com/<your-org>/sprint-analyzer.git
cd sprint-analyzer
Install dependencies

bash
Copy code
pip install -r requirements.txt
Configure environment

bash
Copy code
cp .env.example .env
Set your:

GROQ_API_KEY

JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN (optional if using JIRA integration)

Run the analyzer

bash
Copy code
python agent.py
🧩 Requirements
Python 3.10+

Internet connection

Groq API key (free tier available)

Optional: JIRA access for automatic sprint fetch

🧠 What It Does
Fetch Tickets

Manual input or via JIRA API

Supports current sprint, assignee, and status filters

Memory & Risk Scoring

Calculates risk based on:

Description length

Linked issues

Keywords (refactor, migrate)

Maps numeric scores to human-readable text (Impact, Severity, Dev Lift)

Think (AI Reasoning)

Sends ticket data + metrics to Groq LLM (Llama 3.1)

Generates:

Risk Analysis

Dependency Detection

Effort Breakdown

Priority Reordering

10-Day Execution Plan

Quick Wins

Sprint Health Summary

Act (Output)

Displays a rich console table with all tickets

Saves AI analysis + raw data to model/data/<date_random>/sprint_analysis.txt

🖥️ Example Console Output
pgsql
Copy code
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
┃ Key           ┃ Summary                              ┃ Points ┃ Type   ┃ Risk    ┃
┣━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━╋━━━━━━━━╋━━━━━━━━━┫
┃ SK12-145      ┃ Refactor user service auth layer     ┃ 8      ┃ Story  ┃ ⚠️⚠️     ┃
┃ SK12-148      ┃ Fix dashboard widget error           ┃ 3      ┃ Bug    ┃ ✅      ┃
┗━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━┻━━━━━━━━┻━━━━━━━━━┛
🧰 Tech Stack
Python 3.13+

Groq API (Llama 3.1)

Rich for terminal formatting

JIRA Python API (optional for live sprint data)

🧭 Roadmap
✅ MVP (Current)
Manual or automatic sprint data fetch

AI-based risk & complexity analysis

Console summary table

Auto-save results per run

🚧 Coming Next
Multi-agent setup (fetcher → analyzer → reporter)

Sprint trend comparison dashboard

Export to CSV, Markdown, or PDF reports

Integration with Slack / MS Teams notifications

🧑‍💻 Author
Muhammad Maaz
Backend Engineer & AI Enthusiast
📧 maazafzal92@gmail.com
🌐 GitHub

📜 License
MIT License — free to modify and extend