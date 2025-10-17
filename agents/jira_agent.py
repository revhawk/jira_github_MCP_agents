import requests
import time
import logging
from requests.auth import HTTPBasicAuth
from typing import Dict, Any, List, Optional

from config.settings import Settings

logger = logging.getLogger(__name__)


class JiraClient:
    """A client for interacting with the Jira API."""

    def __init__(self):
        self.base_url = Settings.JIRA_BASE
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(Settings.JIRA_EMAIL, Settings.JIRA_API_TOKEN)
        self.session.headers.update({"Accept": "application/json"})

    def _request(
        self, method: str, endpoint: str, max_retries: int = 3, **kwargs
    ) -> requests.Response:
        """Make a request to the Jira API with retries for timeouts."""
        url = f"{self.base_url}{endpoint}"
        for attempt in range(max_retries):
            try:
                return self.session.request(method, url, timeout=20, **kwargs)
            except requests.exceptions.Timeout:
                if attempt == max_retries - 1:
                    raise
                time.sleep(2**attempt)
        # This line should not be reachable due to the raise in the loop
        raise requests.exceptions.RequestException("Request failed after all retries.")

    def get_issue(self, issue_key: str) -> Dict[str, Any]:
        """Fetch a full Jira ticket by its key."""
        try:
            response = self._request("GET", f"/rest/api/3/issue/{issue_key}")
            response.raise_for_status()
            return {"ticket": response.json()}
        except requests.RequestException as e:
            details = e.response.text if e.response else str(e)
            status = e.response.status_code if e.response else "N/A"
            return {
                "ticket": None,
                "error": f"Jira API returned {status}",
                "details": details,
            }

    def read_issue(self, issue_key: str) -> Dict[str, Any]:
        """Fetch Jira issue fields needed for generation (summary, description, and issuetype)."""
        params = {"fields": "summary,description,issuetype"}
        try:
            response = self._request("GET", f"/rest/api/3/issue/{issue_key}", params=params)
            response.raise_for_status()
            data = response.json()
            fields = data.get("fields", {})
            summary = fields.get("summary") or ""
            description = fields.get("description")  # Can be rich text (ADF)
            issuetype = fields.get("issuetype", {}).get("name", "")
            return {
                "key": issue_key,
                "summary": summary,
                "description": description,
                "issuetype": issuetype,
            }
        except requests.RequestException as e:
            details = e.response.text if e.response else str(e)
            status = e.response.status_code if e.response else "N/A"
            return {"key": issue_key, "error": f"Jira API returned {status}", "details": details}

    def list_recent_tickets(
        self, max_results: int = 50, project_key: str = Settings.JIRA_PROJECT_KEY
    ) -> Dict[str, Any]:
        """List recent Jira issues for a project using JQL."""
        params = {
            "jql": f"project = {project_key} ORDER BY updated DESC",
            "maxResults": str(max_results),
            "fields": "summary,status,assignee,updated",
        }
        try:
            response = self._request("GET", "/rest/api/3/search", params=params)
            response.raise_for_status()
            return {"issues": response.json().get("issues", [])}
        except requests.RequestException as e:
            details = e.response.text if e.response else str(e)
            status = e.response.status_code if e.response else "N/A"
            return {
                "issues": [],
                "error": f"Jira search returned {status}",
                "details": details,
            }

    def list_all_issues_in_project(
        self, project_key: str, max_results: int = 100
    ) -> Dict[str, Any]:
        """List all issues in a Jira project using the Agile API as a primary method."""
        # NOTE: This logic seems specific to your Jira setup (e.g., project "CAL").
        # Consider moving board ID mappings to your settings/config file.
        board_ids_to_try: List[int] = []
        if project_key == "CAL":
            board_ids_to_try.append(34)
        else:
            board_ids_to_try.append(Settings.JIRA_BOARD_ID)

        agile_params = {"maxResults": str(max_results)}
        all_errors = []

        for board_id in board_ids_to_try:
            logger.debug(f"Trying Agile API (board {board_id})...")
            try:
                response = self._request(
                    "GET", f"/rest/agile/1.0/board/{board_id}/issue", params=agile_params
                )
                logger.debug(f"Agile response for board {board_id}: {response.status_code}")
                response.raise_for_status()
                all_issues = response.json().get("issues", [])
                
                # Filter by project since Agile API doesn't filter by project
                project_issues = [
                    issue for issue in all_issues if issue.get("key", "").startswith(project_key)
                ]
                
                if project_issues:
                    logger.info(f"Found {len(project_issues)} issues for project {project_key} on board {board_id}")
                    return {"issues": project_issues}

            except requests.RequestException as e:
                details = e.response.text if e.response else str(e)
                error_msg = f"Board {board_id} failed: {details}"
                logger.warning(error_msg)
                all_errors.append(error_msg)
                continue

        return {"issues": [], "error": "No issues found via Agile API", "details": "\n".join(all_errors)}


# --- LangGraph Node ---
# This function remains separate for clean integration with LangGraph.
# It uses the JiraClient to perform its actions.

jira_client = JiraClient()

def fetch_ticket(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph node: fetch a Jira ticket by key provided in state['issue_key']."""
    issue_key = state.get("issue_key")
    if not issue_key:
        return {"error": "Missing issue_key in state"}

    return jira_client.get_issue(issue_key)
