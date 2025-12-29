import os
from datetime import datetime
import random, string

from fetcher import fetch_jira_issues
from memory import build_summary_data
from thinker import analyze_sprint
from actor import display_table, save_analysis

# --- Score maps ---
impact_map = {range(1,4):"Low", range(4,7):"Moderate", range(7,9):"High", range(9,11):"Critical"}
severity_map = {range(1,4):"Minor", range(4,7):"Moderate", range(7,9):"Major", range(9,11):"Critical"}
dev_lift_map = {range(1,4):"Heavy", range(4,7):"Medium", range(7,9):"Moderate", range(9,11):"Light"}

def run_agent():
    jira, issues = fetch_jira_issues()
    summary_data = build_summary_data(issues, jira, None)  # pass jira object if needed

    display_table(summary_data, impact_map, severity_map, dev_lift_map)
    
    analysis_text = analyze_sprint(summary_data)
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    output_dir = os.path.join("model", "data", today_str)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"result_{random_str}.txt")
    
    save_analysis(summary_data, analysis_text, "llama-3.1-8b-instant", output_path)
    print(f"✅ Result saved to: {output_path}")

if __name__ == "__main__":
    run_agent()
