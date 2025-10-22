# Jira Code Generator

AI-powered code generation from Jira tickets using LangGraph, featuring multiple specialized agents for TDD and full-stack application generation.

## Features

- **Unified App Generation**: Multiple Jira tickets → One cohesive Streamlit application
- **TDD Workflow**: Generates standalone, tested modules from single tickets.
- **Multi-Agent Workflow**: Architecture design, spec extraction, code generation, testing, and validation
- **Automatic Fixing**: Auto-fixes failing tests and Streamlit app errors
- **Cost Optimized**: Uses `gpt-4o-mini` for a balance of performance and cost.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file with:

```bash
# Jira Configuration
JIRA_BASE=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_jira_api_token
JIRA_PROJECT_KEY=CAL
JIRA_BOARD_ID=34

# OpenAI API
OPENAI_API_KEY=your_openai_api_key

# Optional: Other AI providers
GROQ_API_KEY=your_groq_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GEMINI_API_KEY=your_gemini_api_key
```

### 3. Run Code Generation

```bash
python main.py
```

Choose mode:
1. **Single ticket** - Standalone app per ticket
2. **Bulk import** - Standalone apps for all tickets
3. **Unified app** - One integrated Streamlit app (recommended)

## Workflow Architecture

### Agents
1.  **jira_reader**: Reads Jira tickets based on keys or fetches all from a project.
2.  **system_architect**: Designs the application architecture based on Jira tickets, inferring the application's goal and defining modules, their purposes, and functions.
3.  **spec_agent**: Generates detailed implementation specifications for each module, including function signatures, inputs, outputs, edge cases, and acceptance criteria.
4.  **spec_reviewer**: Reviews the generated specifications for completeness and quality, acting as a quality gate before code generation.
5.  **generate_tests**: Generates pytest test files for each module based on its spec, covering normal functionality, edge cases, and error handling.
6.  **generate_code**: Implements the business logic for each module, aiming to satisfy the spec and pass generated tests.
7.  **validate_modules**: Validates that generated modules contain the functions they claim to have according to their specifications.
8.  **generate_main_app**: Creates the main Streamlit application file (`app.py`), integrating all generated modules into a cohesive user interface.
9.  **run_tests**: Executes the generated pytest tests against the generated code.

## Generated Structure

```
modules/
  calculator.py          # Business logic modules
  validator.py
  __init__.py
generated_tests/
  test_calculator.py     # Pytest tests
  test_validator.py
app.py                   # Main Streamlit application
```

## Running Generated Apps

```bash
streamlit run app.py
```

## Testing

### Run Connection Tests

```bash
python -m tests.test_connections
```

### Run Generated Module Tests

```bash
python -m pytest generated_tests/ -v
```

### Run Streamlit UI Tests

```bash
python -m pytest tests/test_streamlit_app.py -v
```

## Reference Examples

Add proven working patterns to `reference_examples/streamlit_apps/`:

- `calculator_button_grid.py` - Button grid layout with st.rerun()
- `sidebar_navigation.py` - Multi-page sidebar navigation

The workflow automatically loads and uses these examples.

## Jira Configuration

### Board ID Setup

For CAL project, board ID is 34. Configure in `.env`:

```bash
JIRA_PROJECT_KEY=CAL
JIRA_BOARD_ID=34
```

The system uses Jira Agile API directly (skips GET/POST that return 410).

### EPIC Requirements

Create an EPIC ticket with description containing:
- Application requirements
- Constraints (e.g., "simple", "no complex state management")
- Architecture preferences

Link all feature tickets to the EPIC.

## Cost Optimization

- **o1 model** ($15/$60 per 1M tokens): Architecture, specs, requirements
- **gpt-4o-mini** ($0.15/$0.60 per 1M tokens): Code generation, tests, UI, fixes
- **Estimated cost**: ~$0.50-$2 per unified app generation

## Troubleshooting

### Module Import Errors

Run from project root with `-m` flag:
```bash
python -m tests.test_connections
```

### Streamlit App Not Updating

- Restart Streamlit server: `Ctrl+C` then `streamlit run app.py`
- Hard refresh browser: `Ctrl+Shift+R`
- Check logs in `logs/unified_*.log`

### Test Failures

Check `logs/unified_*.log` for detailed error messages. The workflow auto-fixes tests up to loop detection limit.

## Examples

See `simple_calculator/` for a complete working example generated from 30 Jira tickets.

## Contributing

To add new reference examples:
1. Create working Streamlit app
2. Add to `reference_examples/streamlit_apps/`
3. Include docstring with pattern name and use case
4. Update `ui_designer` to detect the pattern

## License

MIT
