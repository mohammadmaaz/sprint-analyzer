import os
from jira import JIRA
from dotenv import load_dotenv

load_dotenv()

def fetch_jira_issues():
    jira = JIRA(
        server=os.getenv("JIRA_URL"),
        basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
    )
    jql = "sprint in openSprints() AND assignee = currentUser() AND status in ('Open', 'Reopened')"
    issues = jira.search_issues(jql, maxResults=100)
    return jira, issues

def get_field_id_by_name(jira, name):
    for f in jira.fields():
        if f['name'].lower() == name.lower():
            return f['id']
    return None
