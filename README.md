# jira_github_MCP_agents
Langgraph agents jira github MCP

## Running Tests

To run the connection tests, use the following command from the project root:

```bash
python -m tests.test_connections
```

**Notes:**
- Do not run the test script directly (e.g., `python tests/test_connections.py`), as this may cause import errors.
- Ensure all required dependencies are installed (see below).

## Installing Dependencies
## Jira listing configuration

If listing issues returns 410 (Gone), ensure your service account has Jira Software access and Browse Projects permission. Configure:

```
JIRA_PROJECT_KEY=MFLP
JIRA_BOARD_ID=1
```

The app lists via Agile API for the board first, then falls back to JQL search.


Before running the tests or main program, install all required dependencies:

```bash
pip install -r requirements.txt
```

## Troubleshooting
- If you see `ModuleNotFoundError: No module named 'config'`, make sure you are running the command from the project root and using the `-m` flag as shown above.
- If you see `No module named 'openai'`, install the OpenAI Python package:
  ```bash
  pip install openai
  ```

## Verifying Generated CAL Tests

After running the bulk import for the CAL project, you can verify that tests were generated and run them easily.

1. List all generated CAL test files in version order:
   ```bash
   ls -1 generated_tests/test_CAL-*.py 2>/dev/null | sort -V || echo "No CAL tests found"
   ```

2. Run all CAL tests at once:
   ```bash
   python -m pytest -q $(ls generated_tests/test_CAL-*.py 2>/dev/null | sort -V)
   ```

3. Run each CAL test sequentially with headings:
   ```bash
   for f in $(ls generated_tests/test_CAL-*.py 2>/dev/null | sort -V); do
     echo "===== $(basename "$f") =====";
     python -m pytest -q "$f" || true;
   done
   ```

4. Run a single CAL ticket test (example CAL-19):
   ```bash
   python -m pytest -q generated_tests/test_CAL-19.py
   ```

Notes:
- Always run from the project root so `generated_code/` and `generated_tests/` import correctly.
- Imports use underscores, e.g., `from generated_code.CAL_19 import some_function`.

## Groq (Qwen) API Access

To enable Groq API access for the Qwen model, add your Groq API key to your `.env` file:

```
GROQ_API_KEY=your_groq_api_key_here
```

Install the Groq Python package (already included in requirements.txt):

```bash
pip install -r requirements.txt
```

The test suite will now check Groq (Qwen) connectivity along with Jira, GitHub, and OpenAI.

## Anthropic and Gemini API Access

To enable Anthropic and Gemini API access, add your API keys to your `.env` file:

```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

Install the required packages (already included in requirements.txt):

```bash
pip install -r requirements.txt
```

The test suite will now check Anthropic and Gemini connectivity along with Jira, GitHub, OpenAI, and Groq (Qwen).
