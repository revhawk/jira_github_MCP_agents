# LangSmith Setup for LangGraph Tracing

## 1. Get LangSmith API Key

1. Go to https://smith.langchain.com/
2. Sign up or log in
3. Go to Settings → API Keys
4. Create a new API key

## 2. Add to .env File

Add these lines to your `.env` file:

```bash
# LangSmith Tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=jira-code-generator
```

## 3. Update Code to Enable Tracing

The tracing is automatically enabled when environment variables are set. No code changes needed.

## 4. View Traces

1. Run your workflow: `python main.py`
2. Go to https://smith.langchain.com/
3. Select your project: "jira-code-generator"
4. View traces showing:
   - Each agent execution
   - LLM calls with prompts and responses
   - State transitions
   - Execution time
   - Token usage
   - Errors and retries

## 5. What You'll See

- **Workflow Graph**: Visual representation of agent flow
- **Agent Execution**: Each node (jira_reader, system_architect, etc.)
- **LLM Calls**: Full prompts sent to OpenAI
- **Responses**: Complete LLM outputs
- **State Changes**: How state evolves through workflow
- **Performance**: Timing and token usage per agent

## 6. Debugging Tips

- Filter by status (success/error)
- Search by agent name
- Compare runs to see consistency
- Export traces for analysis
- Set up alerts for failures

## Example Trace Structure

```
Run: unified_app_generation
├── jira_reader (2.3s)
│   └── read_issue x30 calls
├── system_architect (15.2s)
│   └── OpenAI o1 call (4000 tokens)
├── requirements_analyzer (8.1s)
│   └── OpenAI o1 call (2000 tokens)
├── spec_agent (12.5s)
│   └── OpenAI o1 call x2 (6000 tokens)
├── generate_tests (5.3s)
│   └── OpenAI gpt-4o-mini call x2
├── generate_code (6.1s)
│   └── OpenAI gpt-4o-mini call x2
└── generate_main_app (4.2s)
    └── OpenAI gpt-4o-mini call
```
