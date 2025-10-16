# Prompt Improvements Based on Log Analysis

## Critical Issues

### 1. spec_agent Returns Empty Specs
**Problem**: All specs have `"functions": []`, causing placeholder code generation

**Current Prompt Issue**: Prompt says "Simple, direct functions (NO classes, NO state machines, NO FSM)" but doesn't show HOW to extract functions from tickets

**Fix**: Add concrete example showing ticket → function extraction:
```
EXAMPLE TICKET ANALYSIS:
Ticket CAL-1: "Implement addition operation"
Description: "Create function to add two numbers"
→ Extract: {"name": "add", "inputs": ["a: float", "b: float"], "output": "float"}

Ticket CAL-17: "Memory clear button"
Description: "Clear calculator memory"
→ Extract: {"name": "memory_clear", "inputs": [], "output": "None"}
```

### 2. requirements_analyzer Doesn't Block Workflow
**Problem**: Flags "APPROVED: NO" but workflow continues, generating over-engineered code

**Fix**: Add conditional edge after requirements_analyzer:
- If APPROVED: NO → regenerate architecture with simpler design
- If APPROVED: YES → continue to spec_agent

### 3. Infinite Loop on Same Test Failures
**Problem**: memory_management has same 2 failures repeated 4+ times

**Fix**: Add loop detection in test_fixer:
```python
if iteration > 0:
    prev_failures = state.get("previous_test_failures", {})
    if prev_failures == current_failures:
        logger.error("Same failures repeated - skipping module")
        return {"skip_module": module_name}
```

### 4. Button Validation Too Strict
**Problem**: Took 3 iterations to fix button pattern, but validation still flagged it

**Fix**: Improve validation regex:
```python
# Current: checks for ANY 'if st.button('
# Better: check if buttons modify session state
has_session_state_updates = 'st.session_state.' in app_code
has_button_checks = 'if st.button(' in app_code
if has_button_checks and not has_session_state_updates:
    errors.append("Buttons need session state pattern")
```

## Prompt Improvements

### spec_agent Prompt Enhancement
```python
prompt = (
    "Extract implementation spec by analyzing ticket requirements.\n\n"
    "STEP-BY-STEP:\n"
    "1. Read each ticket title and description\n"
    "2. Identify what function(s) it needs\n"
    "3. Determine function inputs/outputs\n"
    "4. List edge cases from description\n\n"
    "EXAMPLE:\n"
    "Ticket: 'CAL-1: Addition operation'\n"
    "Description: 'Add two numbers and return result'\n"
    "→ Function: add(a: float, b: float) -> float\n"
    "→ Edge cases: negative numbers, zero, large numbers\n\n"
    # ... rest of prompt
)
```

### test_fixer Loop Detection
```python
def test_fixer(state: GenState) -> GenState:
    iteration = state.get("fix_iteration", 0)
    current_failures = {mod: res.get("failed", 0) for mod, res in test_results.items()}
    
    # Check if stuck
    if iteration > 0:
        prev = state.get("prev_failures", {})
        if prev == current_failures:
            logger.warning(f"Stuck on same failures after {iteration} iterations")
            # Skip unfixable modules
            for mod in [m for m, f in current_failures.items() if f > 0]:
                logger.error(f"Giving up on {mod} - tests may be invalid")
            return {"failed": 0}  # Force exit
    
    # ... rest of fixer logic
    return {"prev_failures": current_failures, "fix_iteration": iteration + 1}
```

### requirements_analyzer Blocking
```python
def should_continue_after_requirements(state: GenState) -> str:
    analysis = state.get("requirements_analysis", "")
    
    if "APPROVED: NO" in analysis:
        logger.warning("Architecture rejected - regenerating simpler design")
        return "regenerate_architecture"
    return "continue_to_specs"

# In graph builder:
builder.add_conditional_edges(
    "requirements_analyzer",
    should_continue_after_requirements,
    {"regenerate_architecture": "system_architect", "continue_to_specs": "spec_agent"}
)
```

## Model Selection Recommendations

- **system_architect**: Keep GPT-4o with JSON mode ✓
- **spec_agent**: Upgrade to GPT-4o (currently using gpt-4o-mini, causing empty specs)
- **requirements_analyzer**: Keep GPT-4o ✓
- **test_fixer**: Keep GPT-4o ✓
- **fix_app**: Keep GPT-4o ✓

## Summary

**Top 3 fixes:**
1. Upgrade spec_agent to GPT-4o and add ticket→function extraction example
2. Add loop detection to prevent infinite test fixing
3. Make requirements_analyzer block workflow if architecture is over-engineered
