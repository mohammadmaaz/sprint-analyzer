from rich.console import Console
from rich.table import Table
from utils import map_score
from datetime import datetime

console = Console()

def display_table(summary_data, impact_map, severity_map, dev_lift_map):
    table = Table(title="Sprint Ticket Overview")
    table.add_column("Key", style="cyan")
    table.add_column("Summary", style="white")
    table.add_column("Impact")
    table.add_column("Severity")
    table.add_column("Dev Effort")
    table.add_column("Priority Score")
    table.add_column("Impact Priority?")
    table.add_column("Type")
    table.add_column("Risk", style="red")
    
    for item in summary_data:
        table.add_row(
            item["key"],
            item["summary"][:60]+"..." if len(item["summary"])>60 else item["summary"],
            map_score(item["impact_score"], impact_map),
            map_score(item["severity_score"], severity_map),
            map_score(item["dev_lift_score"], dev_lift_map),
            str(item["priority_score"]),
            str(item["impact_priority_account"]),
            item["type"],
            "⚠️"*item["risk"] if item["risk"] else "✅"
        )
    console.print(table)

def save_analysis(summary_data, analysis_text, model_name, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"Model used: {model_name}\nGenerated at: {datetime.now().isoformat()}\n\n")
        f.write("=== Sprint Data ===\n")
        f.write(str(summary_data)+"\n\n")
        f.write("=== Sprint Analysis ===\n")
        f.write(analysis_text+"\n")
