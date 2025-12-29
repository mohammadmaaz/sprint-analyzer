from fetcher import get_field_id_by_name

def calculate_risk(issue, fields_map):
    risk = 0
    fields = issue.fields
    if not fields.summary or len(fields.description or "") < 50:
        risk += 1
    if hasattr(fields, 'issuelinks') and len(fields.issuelinks) > 0:
        risk += 1
    if "refactor" in fields.summary.lower() or "migrate" in fields.summary.lower():
        risk += 1
    return risk

def build_summary_data(issues, jira, utils):
    summary_data = []
    # Pre-fetch field IDs
    impact_field = get_field_id_by_name(jira, "Impact Score")
    severity_field = get_field_id_by_name(jira, "Severity Score")
    devlift_field = get_field_id_by_name(jira, "Dev Lift Score")
    priorityscore_field = get_field_id_by_name(jira, "Priority Score")
    impactpriority_field = get_field_id_by_name(jira, "Impact Priority Account?")
    
    for issue in issues:
        fields = issue.fields
        summary_data.append({
            "key": issue.key,
            "summary": fields.summary,
            "impact_score": getattr(fields, impact_field, None),
            "severity_score": getattr(fields, severity_field, None),
            "dev_lift_score": getattr(fields, devlift_field, None),
            "priority_score": getattr(fields, priorityscore_field, None),
            "impact_priority_account": getattr(fields, impactpriority_field, None),
            "risk": calculate_risk(issue, {}),
            "type": fields.issuetype.name
        })
    return summary_data
