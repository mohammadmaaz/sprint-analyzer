# 🧠 Sprint Analyzer  
> AI-powered Sprint Analysis Agent for Agile Teams using JIRA or Manual Input

---

## 🚀 Overview

**Sprint Analyzer** is an AI-powered assistant that helps developers, QA, and project managers quickly **understand, assess, and prioritize sprint tickets**.  

It calculates **risk, complexity, dependencies**, and generates a **10-day execution plan** using an AI model (powered by **Groq** and **Llama 3.1**).  

Ideal for sprint planning, backlog grooming, or retrospectives.

---

## 🗂 Project Structure

- `sprint-analyzer/`
  - `agent.py` – Orchestrator, runs the agent loop
  - `fetcher.py` – Fetches JIRA tickets and handles API integration
  - `memory.py` – Calculates risk, maps scores, stores memory
  - `thinker.py` – Sends data to Groq LLM (Llama 3.1) and returns insights
  - `actor.py` – Displays rich console tables and saves analysis results
  - `utils.py` – Helper functions (score mapping, formatting, conversions)
  - `requirements.txt` – Python dependencies
  - `.env` – Stores API keys (Groq, JIRA)
  - `README.md` – Project documentation
  - `model/`
    - `data/` – Auto-created per run for AI analysis results

- Each run generates a **date-based folder** with a random ID to save results:

- model/data/2025-12-29_ab12c/
   - sprint_analysis.txt

---

## ⚙️ Installation Guide

### 🪟 Windows Setup

1. **Install Python 3.13+**  
   ```bash
   python --version
(Install via Microsoft Store or python.org)

2. **Clone the repository**
   ```bash
   git clone https://github.com/<your-org>/sprint-analyzer.git
   cd sprint-analyzer
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   Set your:
   - GROQ_API_KEY
   - JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN (optional if using   JIRA integration)

5. **Run the analyzer**
   ```bash
   python agent.py
   ```
## Requirements
   - Python 3.10+

   - Internet connection

   - Groq API key (free tier available)

   - Optional: JIRA access for automatic sprint fetch

## What It Does
1. ### Fetch Tickets

   - Manual input or via JIRA API

   - Supports current sprint, assignee, and status filters

2. ### Memory & Risk Scoring

   - Calculates risk based on:

      - Description length

      - Linked issues

      - Keywords (refactor, migrate)

   - Maps numeric scores to human-readable text (Impact, Severity, Dev Lift)

3. ### Think (AI Reasoning)

- Sends ticket data + metrics to Groq LLM (Llama 3.1)

- Generates:

- Risk Analysis

- Dependency Detection

- Effort Breakdown

- Priority Reordering

- 10-Day Execution Plan

- Quick Wins

- Sprint Health Summary

4. ### Act (Output)

   - Displays a rich console table with all tickets

   - Saves AI analysis + raw data to model/data/<date_random>/sprint_analysis.txt

## Example Console Output

| Key  |  Summary | Points | Type | Risk |
|------|----------|--------|------|------|
|SK12-145 | Refactor user service auth layer | 8 | Story | ⚠️⚠️ |
| SK12-148 | Fix dashboard widget error | 3 | Bug | ✅ |


---

## Tech Stack
   - Python 3.13+

   - Groq API (Llama 3.1)

   - Rich for terminal formatting

   - JIRA Python API (optional for live sprint data)

---

## Roadmap

### MVP (Current)
- Manual or automatic sprint data fetch

- AI-based risk & complexity analysis

- Console summary table

- Auto-save results per run

### Coming Next
- Multi-agent setup (fetcher → analyzer → reporter)

- Sprint trend comparison dashboard

- Export to CSV, Markdown, or PDF reports

- Integration with Slack / MS Teams notifications

---

## 🧑‍💻 Author

**Muhammad Maaz**  
Backend Engineer & AI Enthusiast  
📧 [maazafzal92@gmail.com](mailto:maazafzal92@gmail.com)  

🌐 GitHub: [https://github.com/muhammadmaaz](https://github.com/muhammadmaaz)

## 📜 License

This project is licensed under the **MIT License** — free to use, modify, and extend.