# Prompt Engineering: Before vs After

## Philosophy Change

### Before: Minimal Instructions
- Assume LLM knows best practices
- Provide basic examples
- Rely on fix loop to correct mistakes

### After: Explicit Patterns
- Assume nothing - spell out every rule
- Show correct AND incorrect examples
- Prevent mistakes before they happen

## Example: Button Key Rule

### Before (Implicit)
```
Use st.button() for interactive elements.
```

**Result**: LLM creates `st.button('7')` without key → duplicate ID error

### After (Explicit)
```
2. **BUTTON KEYS**: EVERY st.button() MUST have a unique key parameter:
   ✅ CORRECT: st.button('7', key='7')
   ❌ WRONG: st.button('7')
```

**Result**: LLM creates `st.button('7', key='7')` → works first time

## Example: Operator Buttons

### Before (Implicit)
```
Create calculator buttons for operations.
```

**Result**: LLM creates `st.button('✖️', key='multiply')` and appends '✖️' → eval() fails

### After (Explicit)
```
4. **OPERATOR BUTTONS**: Use emoji for label, symbol for key, append SYMBOL not emoji:
   ✅ CORRECT:
   ```python
   if st.button('✖️', key='*'):  # Emoji label, symbol key
       st.session_state.display += '*'  # Append symbol, not emoji
       st.rerun()
   ```
   ❌ WRONG: st.button('*', key='multiply') or appending '✖️'
```

**Result**: LLM creates correct pattern → works first time

## Example: Button Layout

### Before (Implicit)
```
Use st.columns() for grid layout.
```

**Result**: LLM creates `cols[0].button('7')` → all buttons in one column

### After (Explicit)
```
7. **BUTTON GRID LAYOUT**: Use `with col:` blocks, NOT cols[index]:
   ✅ CORRECT:
   ```python
   col1, col2, col3, col4 = st.columns(4)
   with col1:
       if st.button('7', key='7', use_container_width=True):
           st.session_state.display += '7'
           st.rerun()
   ```
   ❌ WRONG: cols[0].button('7', key='7')
```

**Result**: LLM creates proper grid layout → works first time

## Complete Example Comparison

### Before: Minimal Prompt
```
You are a Streamlit developer. Create app.py that integrates these modules:
- calculator: add, subtract, multiply, divide

Use a button grid for the calculator interface.
```

**Generated Code Issues**:
- ❌ No button keys
- ❌ Wrong layout (cols[index])
- ❌ Emoji operators in eval()
- ❌ No st.rerun()
- ❌ Wrong display format
- 🔄 Requires 5+ fix iterations

### After: Explicit Prompt
```
You are a senior Streamlit developer. Create app.py following these CRITICAL RULES:

1. **IMPORTS**: ONLY import: add, subtract, multiply, divide from modules.calculator

2. **BUTTON KEYS**: EVERY st.button() MUST have unique key:
   ✅ st.button('7', key='7')
   ❌ st.button('7')

3. **BUTTON PATTERN**: Use if-statement with st.rerun():
   ✅ if st.button('7', key='7'): st.session_state.display += '7'; st.rerun()
   ❌ st.button('7', on_click=handler)

4. **OPERATOR BUTTONS**: Emoji label, symbol key, append symbol:
   ✅ if st.button('✖️', key='*'): st.session_state.display += '*'; st.rerun()
   ❌ Appending '✖️'

5. **DISPLAY**: st.markdown() with backticks inside f-string:
   ✅ st.markdown(f'### Display: `{st.session_state.display}`')
   ❌ st.text_input(disabled=True)

6. **SESSION STATE**: Initialize at top:
   if 'display' not in st.session_state: st.session_state.display = '0'

7. **BUTTON GRID**: Use `with col:` blocks:
   ✅ with col1: st.button('7', key='7', use_container_width=True)
   ❌ cols[0].button('7')

[Complete working example provided...]
```

**Generated Code**:
- ✅ All buttons have keys
- ✅ Proper grid layout
- ✅ Symbol operators
- ✅ st.rerun() after updates
- ✅ Correct display format
- 🎯 Works on first generation

## Key Principles

### 1. Show Don't Tell
Instead of: "Use proper button keys"
Use: "✅ CORRECT: st.button('7', key='7') ❌ WRONG: st.button('7')"

### 2. Anticipate Mistakes
Think: "What will the LLM get wrong?"
Then: Explicitly prevent that mistake in the prompt

### 3. Provide Complete Examples
Not: "Use st.columns() for layout"
But: Full working code showing exact pattern

### 4. Use Visual Markers
- ✅ for correct patterns
- ❌ for wrong patterns
- 🎯 for goals
- 🔧 for fixes

### 5. Be Redundant
Say the same thing multiple ways:
- In rules
- In examples
- In comments
- In complete code

## Prompt Size vs Quality Trade-off

### Before
- Prompt: ~200 tokens
- Generation: Often wrong
- Fixes: 5-10 iterations × 500 tokens = 2500-5000 tokens
- **Total: ~2700-5200 tokens**

### After
- Prompt: ~1500 tokens (7.5x larger)
- Generation: Usually correct
- Fixes: 0-2 iterations × 500 tokens = 0-1000 tokens
- **Total: ~1500-2500 tokens**

**Result**: Larger prompt, but LOWER total token usage and cost!

## Temperature Impact

### Before: temperature=0.3
- More creative/varied output
- Less consistent with patterns
- More likely to deviate from examples

### After: temperature=0.1
- More deterministic output
- Strictly follows patterns
- Copies examples more faithfully

**For code generation, we WANT copying, not creativity!**

## Validation Strategy

### Before: Validate After Generation
1. Generate code (often wrong)
2. Validate (find errors)
3. Fix (multiple iterations)

### After: Prevent During Generation
1. Generate code (usually correct due to explicit prompts)
2. Validate (confirm correctness)
3. Fix only if needed (rare)

**Prevention > Detection > Correction**

## Measuring Success

### Metrics to Track
1. **First-time success rate**: % of apps that work without fixes
2. **Average fix iterations**: Should be 0-2 (down from 5-10)
3. **Total tokens per app**: Should decrease despite larger prompts
4. **Cost per app**: Should decrease by ~20-40%
5. **Generation time**: Should decrease (fewer iterations)

### Target Goals
- ✅ 80%+ first-time success rate
- ✅ <2 average fix iterations
- ✅ <3000 total tokens per app
- ✅ <$1.00 per app
- ✅ <5 minutes generation time

## Conclusion

**Explicit prompts with examples > Implicit instructions + fix loops**

The fix loop is still valuable as a safety net, but the goal is to rarely need it. By investing in better prompts upfront, we:
- Generate correct code first time
- Reduce total token usage
- Lower costs
- Faster generation
- More consistent quality
