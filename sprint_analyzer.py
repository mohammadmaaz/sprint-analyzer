import os
import random
import string
from datetime import datetime
from jira import JIRA
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from groq import Groq

load_dotenv()
console = Console()

# --- Connect to JIRA ---
jira = JIRA(
    server=os.getenv("JIRA_URL"),
    basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
)

# --- Query: Current Sprint for You ---
jql = "sprint in openSprints() AND assignee = currentUser()"
issues = jira.search_issues(jql, maxResults=100)

console.print(f"\n[bold green]Found {len(issues)} tickets in current sprint[/bold green]\n")

# --- Analyze ---
summary_data = []
for issue in issues:
    fields = issue.fields
    desc = fields.description or ""
    risk = 0

    # Basic heuristics
    if not fields.summary or len(desc) < 50:
        risk += 1
    if hasattr(fields, 'issuelinks') and len(fields.issuelinks) > 0:
        risk += 1
    if "refactor" in fields.summary.lower() or "migrate" in fields.summary.lower():
        risk += 1

    summary_data.append({
        "key": issue.key,
        "summary": fields.summary,
        "points": getattr(fields, "customfield_10016", None),  # story points field (may vary)
        "risk": risk,
        "type": fields.issuetype.name,
    })

# --- Display Table ---
table = Table(title="Sprint Ticket Overview")
table.add_column("Key", style="cyan")
table.add_column("Summary", style="white")
table.add_column("Points", justify="right")
table.add_column("Type", style="magenta")
table.add_column("Risk", style="red")

for item in summary_data:
    table.add_row(
        item["key"],
        item["summary"][:60],
        str(item["points"] or "-"),
        item["type"],
        "⚠️" * item["risk"] if item["risk"] else "✅"
    )

console.print(table)

# --- Optional: GPT Summary ---
# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
summary_text = "\n".join(
    f"{i['key']}: {i['summary']} (Risk={i['risk']})" for i in summary_data
)

# Ask Groq (Llama 3) for sprint insights
prompt = f"""
Analyze the following sprint backlog items and identify:
1. High-risk or ambiguous stories.
2. Possible dependencies.

Items:
{summary_data}
"""
# === Choose your model ===
MODEL_NAME = "llama-3.1-8b-instant"  # or "llama-3.1-8b-instant"
response = client.chat.completions.create(
    model=MODEL_NAME,  # or "llama3-70b-8192" if you want larger context
    messages=[
        {"role": "system", "content": "You are an agile sprint planning assistant."},
        {"role": "user", "content": prompt}
    ],
)

analysis_text = response.choices[0].message.content.strip()

console.print("\n[bold yellow]Sprint Analysis:[/bold yellow]")
console.print(analysis_text)

# === Generate folder and filename ===
today_str = datetime.now().strftime("%Y-%m-%d")
random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

output_dir = os.path.join("model", "data", today_str)
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, f"result_{random_str}.txt")

# === Write to file ===
with open(output_path, "w", encoding="utf-8") as f:
    f.write(f"Model used: {MODEL_NAME}\n")
    f.write(f"Generated at: {datetime.now().isoformat()}\n\n")
    f.write("=== Sprint Data ===\n")
    f.write(str(summary_data) + "\n\n")
    f.write("=== Sprint Analysis ===\n")
    f.write(analysis_text + "\n")

console.print(f"\n[green]✅ Result saved to:[/green] {output_path}")
