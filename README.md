# 🧠 Sprint Analyzer  
> AI-powered sprint analysis assistant for teams using JIRA or Agile boards.

---

## 🚀 Overview

Sprint Analyzer helps developers and project managers quickly **understand, assess, and prioritize sprint tickets** before starting work.  
It summarizes risk levels, ticket complexity, and dependencies using an AI model (powered by **Groq** and **Llama 3.1**).

Ideal for sprint planning, backlog grooming, or retrospectives.

---

## 📁 Project Structure

sprint-analyzer/
│
├── sprint_analyzer.py # Main script
├── requirements.txt # Python dependencies
├── .env # Stores your GROQ API key
├── .gitignore
├── README.md
│
└── model/
└── data/ # AI-generated analysis results (auto-created)


Each time you run the analyzer, a new date-based folder with a random ID is created inside `model/data/` to store results like:

model/data/2025-10-10_ab12c/
└── sprint_analysis.txt


---

## ⚙️ Installation Guide

### 🪟 Windows 11 Setup

1. **Install Python (from Microsoft Store)**  
   - Open *Microsoft Store* → Search **Python 3.13+** → Click **Install**.  
   - Verify installation:  
     ```bash
     python --version
     ```

2. **Clone the repository**
   ```bash
   git clone https://github.com/<your-org>/sprint-analyzer.git
   cd sprint-analyzer


pip install -r requirements.txt

echo GROQ_API_KEY=your_groq_api_key_here > .env

python sprint_analyzer.py


🧩 Requirements

Python 3.10+
Internet connection
Groq API key(free tier available)

🧠 What It Does

The analyzer:

Reads your sprint summary or ticket list (can be manually added or automated from JIRA).

Sends it to an AI model (llama-3.1-70b-versatile) via Groq.

Evaluates:

Risk level (⚠️ = risky, ✅ = safe)

Estimated complexity / points

Type (Bug, Story, Epic, etc.)

Outputs a rich console summary and a saved .txt result file.

🧾 Example Output

🖥️ Console View

┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
┃ Key           ┃ Summary                              ┃ Points ┃ Type   ┃ Risk    ┃
┣━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━╋━━━━━━━━╋━━━━━━━━━┫
┃ SK12-145      ┃ Refactor user service auth layer     ┃ 8      ┃ Story  ┃ ⚠️⚠️     ┃
┃ SK12-148      ┃ Fix dashboard widget error           ┃ 3      ┃ Bug    ┃ ✅      ┃
┗━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━┻━━━━━━━━┻━━━━━━━━━┛

🧰 Tech Stack

Python 3.13+

Groq API (Llama 3.1) for AI analysis

Rich for console formatting


🧭 Roadmap

✅ MVP (current)

Manual sprint data input

AI-based risk & complexity analysis

Auto-save results per run

🚧 Coming Next

Direct JIRA API integration (/rest/api/3/search)

Sprint trend comparison dashboard

Export to CSV / Markdown reports


🧑‍💻 Author

Muhammad Maaz
Backend Engineer & AI Enthusiast
📧 maazafzal92@gmail.com
🌐 github [mohammadmaaz](https://github.com/mohammadmaaz)


📜 License

This project is licensed under the MIT License — feel free to modify and extend.