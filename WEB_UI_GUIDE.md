# Jira Coder - Web UI Guide

## Launch the Web UI

```bash
streamlit run jira_coder_ui.py
```

Then open: **http://localhost:8501**

---

## Interface Overview

```
┌─────────────────────────────────────────────────────────────┐
│  🔧 Jira Coder                                              │
│  AI-powered code generation from Jira tickets               │
├──────────────┬──────────────────────────────────────────────┤
│              │                                               │
│  SIDEBAR     │  MAIN CONTENT                                │
│              │                                               │
│  Mode Select │  Configuration Panel                         │
│  ┌─────────┐ │  ┌──────────────────────────────────────┐   │
│  │ 1. TDD  │ │  │ Input fields for selected mode       │   │
│  │ 2. Full │ │  │ [Ticket Keys]                        │   │
│  │ 3. Incr │ │  │ [Project Key]                        │   │
│  │ 4. Comp │ │  │ [Generate Button]                    │   │
│  │ 10. Demo│ │  └──────────────────────────────────────┘   │
│  │ 11. Demo│ │                                               │
│  │ 12. Demo│ │  Status Panel                                │
│  └─────────┘ │  ┌──────────────────────────────────────┐   │
│              │  │ ✅ app.py exists                     │   │
│  Quick       │  │ ✅ 3 modules                         │   │
│  Actions     │  │ [View Code Button]                   │   │
│  ┌─────────┐ │  │                                       │   │
│  │🗂️ Archive│ │  │ Recent Logs                          │   │
│  │📊 Tests  │ │  │ [View Latest Log]                    │   │
│  └─────────┘ │  └──────────────────────────────────────┘   │
└──────────────┴──────────────────────────────────────────────┘
```

---

## Mode Guide

### 1. TDD Workflow
**Purpose:** Generate a single tested module from one Jira ticket

**Steps:**
1. Select "1. TDD Workflow" from sidebar
2. Enter Jira ticket key (e.g., `CAL-1`)
3. Click "Generate Module"
4. View output in main panel
5. Check Status panel for generated files

**Output:**
- `modules/[module_name].py` - Business logic
- `generated_tests/test_[module_name].py` - Tests

---

### 2. Full Generation
**Purpose:** Generate complete Streamlit app from multiple tickets

**Steps:**
1. Select "2. Full Generation" from sidebar
2. If existing code detected, choose:
   - **Backup and regenerate** (safe, creates archive)
   - **Cancel** (use Mode 3 instead)
   - **Overwrite** (dangerous, requires confirmation)
3. Enter project key (e.g., `CAL`)
4. Enter ticket keys (comma-separated) or leave empty for ALL
5. Click "Generate Application"
6. Wait for generation (may take 5-10 minutes)

**Output:**
- `app.py` - Main Streamlit application
- `modules/` - Business logic modules
- `generated_tests/` - Pytest tests
- `archive/backup_*/` - Backup if selected

**Safety Features:**
- ⚠️ Warns if existing code detected
- 💾 Auto-backup option
- 🛡️ Confirmation required for overwrite

---

### 3. Incremental Update
**Purpose:** Add new features without regenerating UI

**Steps:**
1. Select "3. Incremental Update" from sidebar
2. Enter ticket keys for new features (e.g., `CAL-31,CAL-32`)
3. Click "Add Features"
4. View which functions were added
5. Manually update `app.py` UI if needed

**Output:**
- Updated `modules/[module_name].py` with new functions
- `modules/[module_name].py.backup` - Backup of original
- Existing code preserved ✅

**Benefits:**
- ✅ No code loss
- ✅ Fast (seconds, not minutes)
- ✅ Safe (creates backup)
- ⚠️ UI not updated (manual step)

---

### 4. Compare Archives
**Purpose:** View differences between archived versions

**Steps:**
1. Select "4. Compare Archives" from sidebar
2. Choose first archive from dropdown
3. Choose second archive from dropdown
4. Click "Compare"
5. View unified diff in main panel

**Output:**
- Diff view showing:
  - Added lines (green +)
  - Removed lines (red -)
  - Changed files
  - Module count changes

**Use Cases:**
- See what changed between versions
- Verify incremental updates worked
- Review before/after comparisons

---

### 10-12. Demo Apps
**Purpose:** Run example calculators

**Available Demos:**
- **Mode 10**: Basic Calculator
  - Digits, operators, equals, clear
  - No memory, no binary
  
- **Mode 11**: Calculator with Memory
  - Basic + M+, MR, MC buttons
  - Memory display
  
- **Mode 12**: Calculator with Binary Mode
  - Memory + DEC/BIN toggle
  - Binary arithmetic (1000 + 10 = 1010)

**Steps:**
1. Select demo mode from sidebar
2. Click "Launch Demo"
3. Copy command shown
4. Run in terminal: `streamlit run demos/[demo_name].py`

**Note:** Demos launch in separate Streamlit instance

---

### 20+. Archived Apps
**Purpose:** Run previously generated applications

**How It Works:**
- Archives auto-discovered from `archive/` folder
- Listed as modes 20, 21, 22, etc.
- Shows app name from README (if available)
- Shows timestamp for reference

**Steps:**
1. Archives appear automatically in sidebar
2. Click archive mode number
3. App launches in new Streamlit instance

**Archive Naming:**
- Format: `[name]_[YYYYMMDD]_[HHMMSS]`
- Example: `calculator_with_binary_20251022_145000`

---

## Status Panel Features

### Generated Files
- ✅ Shows if `app.py` exists
- ✅ Shows module count
- 📄 Click "View app.py" to see code
- 📄 Select module from dropdown to view

### Recent Logs
- 📋 Shows latest log file
- 🔍 Click "View Latest Log" to see full output
- 📊 Includes generation progress, errors, reviews

### Quick Actions
- **🗂️ Open Archive Folder**: Shows archive path
- **📊 View Test Results**: Shows pass/fail counts from `.report.json`

---

## Tips & Tricks

### Efficient Workflow
1. **First time**: Use Mode 2 (Full Generation)
2. **Add features**: Use Mode 3 (Incremental Update)
3. **Compare versions**: Use Mode 4 before/after
4. **Demo to stakeholders**: Use Modes 10-12

### Safety Best Practices
- ✅ Always choose "Backup and regenerate" in Mode 2
- ✅ Use Mode 3 for adding features (preserves code)
- ✅ Compare archives (Mode 4) before overwriting
- ✅ Check Status panel after generation

### Performance
- Mode 1: ~30 seconds per ticket
- Mode 2: ~5-10 minutes for full app (30 tickets)
- Mode 3: ~10-30 seconds per feature
- Mode 4: ~5 seconds for comparison

### Troubleshooting
- **Generation timeout**: Increase timeout in code or use CLI
- **Port 8501 in use**: Stop other Streamlit instances
- **No archives shown**: Generate apps first (Mode 2)
- **Demo won't launch**: Check `demos/` folder exists

---

## Keyboard Shortcuts

- **Ctrl+C**: Stop Streamlit server
- **Ctrl+Shift+R**: Hard refresh browser
- **R**: Rerun Streamlit app (when focused)

---

## Advanced Features

### Custom Timeouts
Edit `jira_coder_ui.py`:
```python
timeout=300  # 5 minutes (Mode 1, 3)
timeout=600  # 10 minutes (Mode 2)
```

### Archive Management
Archives stored in: `archive/[name]_[timestamp]/`

Each archive contains:
- `app.py` - Main application
- `modules/` - Business logic
- `generated_tests/` - Tests
- `README.md` - Documentation
- `logs/` - Generation logs

### Log Analysis
Logs show:
- Agent execution order
- LLM prompts and responses
- Test results
- Fix iterations
- Architecture reviews

---

## Comparison: Web UI vs CLI

| Feature | Web UI | CLI |
|---------|--------|-----|
| Ease of use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Visual feedback | ✅ Real-time | ❌ Text only |
| Code viewing | ✅ Inline | ❌ External editor |
| Archive browsing | ✅ Dropdown | ❌ Manual |
| Demo launching | ✅ One click | ❌ Manual command |
| Comparison | ✅ Visual diff | ✅ Terminal diff |
| Automation | ❌ Manual | ✅ Scriptable |
| Speed | Same | Same |

**Recommendation:** Use Web UI for interactive work, CLI for automation.

---

## Next Steps

1. **Launch Web UI**: `streamlit run jira_coder_ui.py`
2. **Try Mode 10**: Run basic calculator demo
3. **Generate your app**: Use Mode 2 with your Jira tickets
4. **Add features**: Use Mode 3 for incremental updates
5. **Compare versions**: Use Mode 4 to see changes

**Need help?** Check `README.md` or `WORKFLOW_FLOWCHART.md`
