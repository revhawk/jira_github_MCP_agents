import requests
import time
from requests.auth import HTTPBasicAuth
from typing import Dict, Any

from config.settings import Settings


def fetch_ticket(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph node: fetch a Jira ticket by key provided in state['issue_key']."""
    issue_key = state.get("issue_key")
    if not issue_key:
        return {"error": "Missing issue_key in state"}

    url = f"{Settings.JIRA_BASE}/rest/api/3/issue/{issue_key}"
    auth = HTTPBasicAuth(Settings.JIRA_EMAIL, Settings.JIRA_API_TOKEN)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth, timeout=15)
    if response.status_code == 200:
        return {"ticket": response.json()}
    return {
        "ticket": None,
        "error": f"Jira API returned {response.status_code}",
        "details": response.text,
    }


def read_issue(issue_key: str) -> Dict[str, Any]:
    """Fetch Jira issue fields needed for generation (summary, description, and issuetype)."""
    url = f"{Settings.JIRA_BASE}/rest/api/3/issue/{issue_key}"
    auth = HTTPBasicAuth(Settings.JIRA_EMAIL, Settings.JIRA_API_TOKEN)
    headers = {"Accept": "application/json"}
    params = {"fields": "summary,description,issuetype"}
    
    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, params=params, auth=auth, timeout=30)
            break
        except requests.exceptions.Timeout:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)
            continue
    if response.status_code == 200:
        data = response.json()
        fields = data.get("fields", {})
        summary = fields.get("summary") or ""
        # Jira Cloud description can be rich text (ADF). Return raw; downstream can simplify.
        description = fields.get("description")
        issuetype = fields.get("issuetype", {}).get("name", "")
        return {"key": issue_key, "summary": summary, "description": description, "issuetype": issuetype}
    return {"key": issue_key, "error": f"Jira API returned {response.status_code}", "details": response.text}

def list_recent_tickets(max_results: int = 50, project_key: str = Settings.JIRA_PROJECT_KEY, board_id: int = Settings.JIRA_BOARD_ID) -> Dict[str, Any]:
    """List recent Jira issues for the authenticated user or project.

    Uses a simple JQL to fetch the latest updated issues visible to the user.
    """
    url = f"{Settings.JIRA_BASE}/rest/api/3/search"
    auth = HTTPBasicAuth(Settings.JIRA_EMAIL, Settings.JIRA_API_TOKEN)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    # Prefer GET with query params (avoids 410 in some Jira Cloud setups)
    params = {
        "jql": f"project = {project_key} ORDER BY updated DESC",
        "maxResults": str(max_results),
        "fields": "summary,status,assignee,updated",
    }

    try:
        response = requests.get(url, params=params, headers=headers, auth=auth, timeout=20)
        if response.status_code == 200:
            data = response.json()
            return {"issues": data.get("issues", [])}
        # Fallback to POST if GET not accepted
        if response.status_code in (400, 405, 410):
            payload = {
                "jql": params["jql"],
                "maxResults": max_results,
                "fields": ["summary", "status", "assignee", "updated"],
            }
            post_resp = requests.post(url, json=payload, headers=headers, auth=auth, timeout=20)
            if post_resp.status_code == 200:
                data = post_resp.json()
                return {"issues": data.get("issues", [])}
            return {
                "issues": [],
                "error": f"Jira search returned {post_resp.status_code}",
                "details": post_resp.text,
            }
        # Fallback 2: Use Jira Agile API by board to list issues
        agile_url = f"{Settings.JIRA_BASE}/rest/agile/1.0/board/{board_id}/issue"
        agile_params = {"maxResults": str(max_results)}
        agile_resp = requests.get(agile_url, params=agile_params, headers=headers, auth=auth, timeout=20)
        if agile_resp.status_code == 200:
            data = agile_resp.json()
            # Agile API returns { issues: [...] }
            return {"issues": data.get("issues", [])}
        return {
            "issues": [],
            "error": f"Jira search returned {response.status_code}; agile returned {agile_resp.status_code}",
            "details": f"search: {response.text}\nagile: {agile_resp.text}",
        }
    except requests.RequestException as e:
        return {"issues": [], "error": "request_exception", "details": str(e)}


def list_all_issues_in_project(project_key: str, max_results: int = 100) -> Dict[str, Any]:
    """List all issues in a Jira project using JQL search with fallbacks.

    Returns a dict with 'issues' (list) or 'error'.
    """
    url = f"{Settings.JIRA_BASE}/rest/api/3/search"
    auth = HTTPBasicAuth(Settings.JIRA_EMAIL, Settings.JIRA_API_TOKEN)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    # Prefer GET with query params (avoids 410 in some Jira Cloud setups)
    params = {
        "jql": f"project = {project_key} ORDER BY key ASC",
        "maxResults": str(max_results),
        "fields": "summary,description",
    }

    try:
        # Use Jira Agile API directly (GET/POST search returns 410)
        if project_key == "CAL":
            board_ids_to_try = [34]
        else:
            board_ids_to_try = [Settings.JIRA_BOARD_ID]
        for board_id in board_ids_to_try:
            agile_url = f"{Settings.JIRA_BASE}/rest/agile/1.0/board/{board_id}/issue"
            agile_params = {"maxResults": str(max_results)}
            print(f"   Trying Agile API (board {board_id})...")
            try:
                agile_resp = requests.get(agile_url, params=agile_params, headers=headers, auth=auth, timeout=20)
                print(f"   Agile response: {agile_resp.status_code}")
                if agile_resp.status_code == 200:
                    data = agile_resp.json()
                    # Agile API returns { issues: [...] }
                    all_issues = data.get("issues", [])
                    # Filter by project since Agile API doesn't filter by project
                    project_issues = [issue for issue in all_issues if issue.get("key", "").startswith(project_key)]
                    if project_issues:
                        print(f"   Found {len(project_issues)} issues for project {project_key} on board {board_id}")
                        return {"issues": project_issues}
            except requests.RequestException as e:
                print(f"   Board {board_id} failed: {e}")
                continue
        return {"issues": [], "error": "No issues found via Agile API"}
    except requests.RequestException as e:
        return {"issues": [], "error": "request_exception", "details": str(e)}

