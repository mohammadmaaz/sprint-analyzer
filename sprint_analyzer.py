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
jql = "sprint in openSprints() AND assignee = currentUser() AND status in ('Open', 'Reopened')"
issues = jira.search_issues(jql, maxResults=100)

console.print(f"\n[bold green]Found {len(issues)} tickets in current sprint[/bold green]\n")

# --- Helper to get field ID by name ---
def get_field_id_by_name(jira, name):
    for f in jira.fields():
        if f['name'].lower() == name.lower():
            return f['id']
    return None

# --- Mapping numeric scores to words ---
impact_map = {
    range(1, 4): "Low impact: isolated",
    range(4, 7): "Moderate impact: some users/features",
    range(7, 9): "High impact: major disruption",
    range(9, 11): "Critical impact: widespread or severe"
}

severity_map = {
    range(1, 4): "Minor disruption: low impact",
    range(4, 7): "Moderate disruption: partial loss or noticeable impact",
    range(7, 9): "Major disruption: critical feature blocked",
    range(9, 11): "Critical disruption: system-wide failure or blocker"
}

dev_lift_map = {
    range(1, 4): "Very heavy lift: >3 days",
    range(4, 7): "Heavy lift: 1–2 days",
    range(7, 9): "Moderate lift: 3–8 hours",
    range(9, 11): "Light lift: 1–3 hours"
}

def map_score(score, mapping):
    if score is None:
        return "-"
    try:
        score = int(score)  # ensure score is an integer
    except ValueError:
        return "-"
    for r, desc in mapping.items():
        if score in r:
            return desc
    return str(score)

# --- Collect summary data from Jira issues ---
summary_data = []
for issue in issues:
    fields = issue.fields
    desc = fields.description or ""
    risk = 0
    tt = getattr(fields, "timetracking", None)

    if tt:
        original_estimate = getattr(tt, "originalEstimate", None)
        remaining_estimate = getattr(tt, "remainingEstimate", None)
        # time_spent = getattr(tt, "timeSpent", None)
    else:
        original_estimate = None
        remaining_estimate = None

    # Basic heuristics to calculate risk
    if not fields.summary or len(desc) < 50:
        risk += 1
    if hasattr(fields, 'issuelinks') and len(fields.issuelinks) > 0:
        risk += 1
    if "refactor" in fields.summary.lower() or "migrate" in fields.summary.lower():
        risk += 1

    impact_field = get_field_id_by_name(jira, "Impact Score")
    severity_field = get_field_id_by_name(jira, "Severity Score")
    devlift_field = get_field_id_by_name(jira, "Dev Lift Score")
    priorityscore_field = get_field_id_by_name(jira, "Priority Score")
    impactpriorityaccount_field = get_field_id_by_name(jira, "Impact Priority Account?")
    priority_score = getattr(fields, priorityscore_field, None)
    impact_priority_account = getattr(fields, impactpriorityaccount_field, None)
    # If it's a list of CustomFieldOption objects
    if isinstance(impact_priority_account, list) and len(impact_priority_account) > 0:
        impact_priority_account = impact_priority_account[0].value  # 'Yes'
    else:
        impact_priority_account = None
    
    summary_data.append({
        "key": issue.key,
        "summary": fields.summary,
        "original_estimate": original_estimate,
        "remaining_estimate": remaining_estimate,
        "impact_score": getattr(fields, impact_field, None),
        "severity_score": getattr(fields, severity_field, None),
        "dev_lift_score": getattr(fields, devlift_field, None),
        "priority_score": priority_score,
        "impact_priority_account": impact_priority_account,
        "risk": risk,
        "type": fields.issuetype.name,
    })

# --- Display Table ---
table = Table(title="Sprint Ticket Overview")
table.add_column("Key", style="cyan")
table.add_column("Summary", style="white")
table.add_column("Impact", justify="left")
table.add_column("Severity", justify="left")
table.add_column("Dev Effort", justify="left")
table.add_column("Priority Score", justify="left")
table.add_column("Impact Priority Account?", justify="left")
table.add_column("Original Estimate", justify="left")
table.add_column("Remaining Estimate", justify="left")
table.add_column("Type", style="magenta")
table.add_column("Risk", style="red")

for item in summary_data:
    impact_text = map_score(item["impact_score"], impact_map)
    severity_text = map_score(item["severity_score"], severity_map)
    dev_lift_text = map_score(item["dev_lift_score"], dev_lift_map)
    priority_score = str(item["priority_score"])
    impact_priority_account = str(item["impact_priority_account"])

    table.add_row(
        item["key"],
        item["summary"][:60] + ("..." if len(item["summary"]) > 60 else ""),
        impact_text,
        severity_text,
        dev_lift_text,
        priority_score,
        impact_priority_account,
        original_estimate,
        remaining_estimate,
        item["type"],
        "⚠️" * item["risk"] if item["risk"] else "✅"
    )

console.print(table)
exit()
# --- Optional: GPT Summary ---
# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
summary_text = "\n".join(
    f"{i['key']}: {i['summary']} (Risk={i['risk']})" for i in summary_data
)

# Ask Groq (Llama 3) for sprint insights
prompt = f"""
You are an expert Sprint Analyst and Engineering Manager. Using the list of sprint items below,
create a deep analysis and a 10-day execution plan for me.

DATA (list of issue objects):
{summary_data}

Your tasks:

1. **Risk Analysis**
   - Identify high-risk, ambiguous, or incomplete stories.
   - Use fields: impact_score, severity_score, priority_score, dev_lift_score, impact_priority_account, and risk.
   - Highlight items with no estimates or unclear acceptance criteria.

2. **Dependency Detection**
   - Identify potential blockers.
   - Point out tasks requiring QA sequencing, environment dependencies, backend–frontend coordination, or cross-team work.

3. **Effort Breakdown**
   - Convert estimates (‘1h’, ‘2h’, ‘1d’) into hours.
   - Calculate total sprint hours.
   - Identify overloaded or underloaded sections.

4. **Priority Reordering**
   - Rank tasks for execution using:
       - risk
       - remaining_estimate
       - priority_score
       - dev_lift_score
       - type (Bug, Task, P0)
       - impact_priority_account (“Yes” = business-critical)
   - Give me a final “Recommended Execution Order”.

5. **10-Day Personal Execution Plan**
   - Spread the work across 10 days.
   - Max 6–7 productive hours/day.
   - Group work logically (e.g., similar module, same system area, same repo).
   - Call out where to pair with QA, Product, or Testing.

6. **Identify Quick Wins**
   - Highlight items < 2 hours that can fit between larger tasks.

7. **Sprint Health Summary**
   - Team focus areas
   - Possible slip points
   - Items that need clarification before work starts

Return the result in sections:
- High-Risk Items
- Dependencies & Blockers
- Estimate & Capacity Analysis
- Recommended Execution Order
- 10-Day Plan (Day 1 → Day 10)
- Quick Wins
- Sprint Summary

Be concise but provide actionable insights.
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
