"""Expense Manager module for managing and categorizing expenses."""

from datetime import datetime
from typing import List, Dict, Union

expenses: List[Dict[str, Union[float, str]]] = []
expense_ids: List[str] = []

def add_expense(amount: float, category: str, date: str) -> bool:
    """Add a new expense to the system."""
    if amount < 0:
        return False
    if not is_valid_date(date):
        return False
    if any(exp['amount'] == amount and exp['category'] == category and exp['date'] == date for exp in expenses):
        return False
    
    expense_id = generate_expense_id()
    expenses.append({'id': expense_id, 'amount': amount, 'category': category, 'date': date})
    expense_ids.append(expense_id)
    return True

def get_expenses_by_category(category: str) -> List[Dict[str, Union[float, str]]]:
    """Retrieve all expenses for a specific category."""
    return [exp for exp in expenses if exp['category'] == category]

def get_total_expenses() -> float:
    """Calculate the total amount of all expenses."""
    return sum(exp['amount'] for exp in expenses)

def delete_expense(expense_id: str) -> bool:
    """Remove an expense from the system by its ID."""
    global expenses
    if expense_id not in expense_ids:
        return False
    expenses = [exp for exp in expenses if exp['id'] != expense_id]
    expense_ids.remove(expense_id)
    return True

def is_valid_date(date_str: str) -> bool:
    """Check if the date string is in valid format YYYY-MM-DD."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def generate_expense_id() -> str:
    """Generate a unique expense ID."""
    return f"id-{len(expenses) + 1}"
