"""Report Generator module for generating financial reports."""

def generate_income_statement(revenue: float, expenses: float, period: str) -> str:
    """Generate an income statement for a given period."""
    return f'Income Statement for {period}: Revenue: {revenue}, Expenses: {expenses}'

def generate_balance_sheet(assets: float, liabilities: float, equity: float, period: str) -> str:
    """Generate a balance sheet for a given period."""
    return f'Balance Sheet for {period}: Assets: {assets}, Liabilities: {liabilities}, Equity: {equity}'

def generate_cash_flow_statement(operating_cash_flow: float, investing_cash_flow: float, financing_cash_flow: float, period: str) -> str:
    """Generate a cash flow statement for a given period."""
    return f'Cash Flow Statement for {period}: Operating Cash Flow: {operating_cash_flow}, Investing Cash Flow: {investing_cash_flow}, Financing Cash Flow: {financing_cash_flow}'