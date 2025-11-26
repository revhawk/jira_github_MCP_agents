# Jira Code Generator

AI-powered code generation from Jira tickets using LangGraph, featuring multiple specialized agents for TDD and full-stack application generation.

## 🌐 Web UI Available!

```bash
streamlit run jira_coder_ui.py
```

Visual interface with real-time feedback, code viewing, and archive management. See [WEB_UI_GUIDE.md](WEB_UI_GUIDE.md) for details.

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

### 3. Run Jira Coder

**Option A: Web UI (Recommended)**
```bash
streamlit run jira_coder_ui.py
```
Then open http://localhost:8501 in your browser.

**Option B: Command Line**
```bash
python main.py
```

Choose mode:
1. **TDD Workflow** - Standalone module from single ticket
2. **Full Generation** - Complete app from multiple tickets
3. **Incremental Update** - Add features without regenerating
4. **Compare Archives** - View differences between versions
10-12. **Demos** - Run example calculators
20+. **Archives** - Run previously generated apps

## Workflow Architecture

**20 Specialized AI Agents** orchestrated by LangGraph. See [AGENT_ARCHITECTURE.md](AGENT_ARCHITECTURE.md) for complete details.

### Key Agents
1.  **jira_reader**: Fetches tickets and EPIC from Jira
2.  **system_architect**: Designs modules and functions (context-aware)
3.  **requirements_analyzer**: Validates against EPIC constraints
4.  **spec_agent**: Generates detailed specifications
5.  **generate_tests**: Creates pytest test files
6.  **code_merger** ⭐: Merges new functions without deleting existing code
7.  **generate_code**: Implements business logic
8.  **ui_designer**: Chooses optimal UI pattern
9.  **generate_main_app**: Creates Streamlit UI
10. **fix_analyzer** + **fixer_agent**: Auto-fixes failing tests
11. **quality_reviewer** + **senior_dev_reviewer** + **architecture_reviewer**: Final reviews

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

**From Web UI:**
- Generated apps appear in the Status panel
- Click "View app.py" to see the code
- Run demos directly from the UI

**From Command Line:**
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

### View Test Results in Web UI

1. Launch web UI: `streamlit run jira_coder_ui.py`
2. Click "📊 View Test Results" in sidebar
3. See pass/fail counts and details

## Documentation

- [README.md](README.md) - This file (quick start)
- [WEB_UI_GUIDE.md](WEB_UI_GUIDE.md) - Streamlit UI guide
- [AGENT_ARCHITECTURE.md](AGENT_ARCHITECTURE.md) - Agent structure and details
- [WORKFLOW_FLOWCHART.md](WORKFLOW_FLOWCHART.md) - Complete workflow diagrams
- [CHANGELOG.md](CHANGELOG.md) - Version history

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
- View logs in Web UI: Click "View Latest Log" in Status panel

### Test Failures

Check `logs/unified_*.log` for detailed error messages. The workflow auto-fixes tests up to loop detection limit.

### Web UI Issues

- Ensure port 8501 is available
- Check `.env` file has all required keys
- View status panel for file existence checks

## Examples

### Demo Apps (Modes 10-12)
- **Mode 10**: Basic calculator (digits + operators)
- **Mode 11**: Calculator with memory (M+, MR, MC)
- **Mode 12**: Calculator with binary mode (DEC/BIN toggle)

### Archived Apps (Modes 20+)
Previously generated apps are auto-discovered and listed.
Use Mode 4 to compare any two archives.

### Full Example
See `simple_calculator/` for a complete working example generated from 30 Jira tickets.

## Contributing

To add new reference examples:
1. Create working Streamlit app
2. Add to `reference_examples/streamlit_apps/`
3. Include docstring with pattern name and use case
4. Update `ui_designer` to detect the pattern

## License

MIT
