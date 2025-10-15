"""Budget tracker module for setting and tracking budgets."""

from typing import Dict

budgets: Dict[str, float] = {}
expenses: Dict[str, float] = {}

def set_budget(category: str, amount: float) -> bool:
    """Set a budget for a specific category."""
    if amount < 0:
        return False
    budgets[category] = amount
    if category not in expenses:
        expenses[category] = 0.0
    return True

def track_expense(category: str, amount: float) -> bool:
    """Track an expense under a specific category."""
    if category not in budgets or amount + expenses[category] > budgets[category]:
        return False
    expenses[category] += amount
    return True

def get_budget(category: str) -> float:
    """Retrieve the budget for a specific category."""
    return budgets.get(category, 0.0)

def get_expenses(category: str) -> float:
    """Retrieve total expenses for a specific category."""
    return expenses.get(category, 0.0)

def get_remaining_budget(category: str) -> float:
    """Calculate remaining budget for a specific category."""
    return budgets.get(category, 0.0) - expenses.get(category, 0.0)