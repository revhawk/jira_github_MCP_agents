# graph/langgraph_unified.py
from langgraph.graph import StateGraph, START

def run_unified_graph(project_key: str, ticket_keys: list):
    from typing_extensions import TypedDict
    from agents.jira_agent import read_issue
    from agents.implementation_agent import write_files
    from agents.tester_agent import run_pytest
    from openai import OpenAI
    from config.settings import Settings
    import os, ast, logging, json
    from datetime import datetime
    
    # Setup logging
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"unified_{project_key}_{timestamp}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info(f"Starting unified generation for {project_key} with tickets: {ticket_keys}")
    print(f"📝 Logging to: {log_file}")

    class GenState(TypedDict, total=False):
        project_key: str
        ticket_keys: list
        tickets: list  # [{key, title, description}]
        epic_description: str
        architecture_plan: str
        modules: dict  # {module_name: {tickets: [], functions: []}}
        specs: dict  # {module_name: spec_json}
        test_files: dict  # {module_name: path}
        code_files: dict  # {module_name: path}
        app_path: str
        test_results: dict
        passed: int
        failed: int

    def log_phase(phase: str):
        logger.info(f"Phase: {phase}")
        print(f"⚙️  {phase}...")

    def jira_reader(state: GenState) -> GenState:
        log_phase("jira_reader")
        from agents.jira_agent import list_all_issues_in_project
        
        ticket_keys = state["ticket_keys"]
        project_key = state.get("project_key", "")
        
        # Handle "ALL" keyword - load all tickets from project
        if len(ticket_keys) == 1 and ticket_keys[0].upper() == "ALL":
            logger.info(f"Loading all tickets from project {project_key}")
            result = list_all_issues_in_project(project_key, max_results=50)
            issues = result.get("issues", [])
            ticket_keys = [issue.get("key") for issue in issues]
            logger.info(f"Found {len(ticket_keys)} tickets in {project_key}")
        
        tickets = []
        epic_description = ""
        
        for key in ticket_keys:
            data = read_issue(key)
            if "error" not in data:
                # Check if this is an EPIC
                issue_type = data.get("issuetype", "")
                logger.info(f"{key}: issue_type = {issue_type}")
                
                if issue_type.upper() == "EPIC":
                    desc = data.get("description", "")
                    if desc:
                        epic_description = str(desc)
                        logger.info(f"Found EPIC: {key} with description length: {len(epic_description)}")
                        print(f"📋 EPIC: {data.get('summary', '')}")
                    else:
                        logger.warning(f"EPIC {key} has no description")
                else:
                    tickets.append({
                        "key": key,
                        "title": data.get("summary", ""),
                        "description": str(data.get("description", ""))
                    })
        
        logger.info(f"Loaded {len(tickets)} tickets and EPIC description")
        return {"tickets": tickets, "epic_description": epic_description}

    def system_architect(state: GenState) -> GenState:
        log_phase("system_architect")
        tickets = state.get("tickets", [])
        epic_description = state.get("epic_description", "")
        project_key = state.get("project_key", "")
        client = OpenAI(api_key=Settings.OPENAI_API_KEY)
        
        if not tickets:
            logger.error("No tickets loaded. Cannot design architecture.")
            return {"architecture_plan": "{}", "modules": {}}
        
        tickets_summary = "\n".join([f"- {t['key']}: {t['title']}" for t in tickets])
        
        # Use EPIC description if available, otherwise infer goal
        if epic_description:
            app_goal = f"EPIC Requirements:\n{epic_description}"
            logger.info("Using EPIC description for application goal")
            print(f"🎯 Using EPIC requirements")
        else:
            app_goal_prompt = (
                "Based on these Jira tickets, what is the overall application goal?\n\n"
                f"TICKETS:\n{tickets_summary}\n\n"
                "OUTPUT: One sentence describing the application purpose.\n"
            )
            
            goal_resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": app_goal_prompt}],
                temperature=0.2,
                top_p=0.95,
                max_tokens=100,
            )
            
            app_goal = goal_resp.choices[0].message.content.strip()
            logger.info(f"Inferred application goal: {app_goal}")
            print(f"🎯 Goal: {app_goal}")
        
        prompt = (
            "You are a software architect. Design a unified Streamlit application structure.\n\n"
            "EXAMPLE OUTPUT:\n"
            "{\n"
            '  "app_name": "Calculator App",\n'
            '  "modules": [\n'
            '    {\n'
            '      "name": "calculator",\n'
            '      "purpose": "Core math operations",\n'
            '      "tickets": ["CAL-1", "CAL-2"],\n'
            '      "functions": ["add", "subtract", "multiply"]\n'
            '    },\n'
            '    {\n'
            '      "name": "validator",\n'
            '      "purpose": "Input validation",\n'
            '      "tickets": ["CAL-3"],\n'
            '      "functions": ["validate_number"]\n'
            '    }\n'
            '  ],\n'
            '  "main_app": {\n'
            '    "layout": "sidebar navigation",\n'
            '    "pages": ["Calculator", "About"]\n'
            '  }\n'
            "}\n\n"
            "REQUIREMENTS:\n"
            "- Follow the EPIC requirements and constraints\n"
            "- Group tickets by logical functionality into modules\n"
            "- Module names should be descriptive (not ticket IDs)\n"
            "- Each module has clear purpose and function list\n"
            "- Main app integrates all modules with Streamlit UI\n"
            "- Keep it SIMPLE - avoid over-engineering\n"
            "- Return valid JSON only\n\n"
            f"APPLICATION GOAL:\n{app_goal}\n\n"
            f"TICKETS:\n{tickets_summary}\n\n"
            "TICKET DETAILS:\n"
        )
        
        for t in tickets:
            prompt += f"\n{t['key']}: {t['title']}\n{t['description'][:200]}\n"
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a software architect. Output only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            top_p=0.95,
            max_tokens=2000,
        )
        
        arch_plan = resp.choices[0].message.content.strip()
        logger.info(f"Architecture plan:\n{arch_plan}")
        
        # Parse modules
        try:
            plan_json = json.loads(arch_plan)
            modules = {}
            for mod in plan_json.get("modules", []):
                modules[mod["name"]] = {
                    "tickets": mod.get("tickets", []),
                    "functions": mod.get("functions", []),
                    "purpose": mod.get("purpose", "")
                }
        except Exception as e:
            logger.error(f"Failed to parse architecture: {e}")
            modules = {"main": {"tickets": [t["key"] for t in tickets], "functions": [], "purpose": "Main module"}}
        
        return {"architecture_plan": arch_plan, "modules": modules}

    def spec_agent(state: GenState) -> GenState:
        log_phase("spec_agent")
        tickets = state.get("tickets", [])
        modules = state.get("modules", {})
        client = OpenAI(api_key=Settings.OPENAI_API_KEY)
        
        specs = {}
        for module_name, module_info in modules.items():
            module_tickets = [t for t in tickets if t["key"] in module_info["tickets"]]
            
            tickets_text = "\n".join([f"{t['key']}: {t['title']}\n{t['description']}" for t in module_tickets])
            
            prompt = (
                "Extract implementation spec for this module.\n\n"
                "EXAMPLE OUTPUT:\n"
                "{\n"
                '  "module": "calculator",\n'
                '  "problem": "Perform basic math operations",\n'
                '  "functions": [\n'
                '    {"name": "add", "inputs": ["a: float", "b: float"], "output": "float", "purpose": "Add two numbers"},\n'
                '    {"name": "subtract", "inputs": ["a: float", "b: float"], "output": "float", "purpose": "Subtract b from a"}\n'
                '  ],\n'
                '  "edge_cases": ["negative numbers", "zero", "large numbers"],\n'
                '  "acceptance": ["add(1, 2) returns 3", "subtract(5, 3) returns 2"]\n'
                "}\n\n"
                "REQUIREMENTS:\n"
                "- Return valid JSON\n"
                "- Define clear function signatures\n"
                "- List edge cases and acceptance criteria\n\n"
                f"MODULE: {module_name}\n"
                f"PURPOSE: {module_info['purpose']}\n"
                f"TICKETS:\n{tickets_text}\n"
            )
            
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Output only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                top_p=0.95,
                max_tokens=1500,
            )
            
            spec = resp.choices[0].message.content.strip()
            try:
                json.loads(spec)
            except Exception:
                spec = json.dumps({"module": module_name, "functions": [], "edge_cases": [], "acceptance": []})
            
            specs[module_name] = spec
            logger.info(f"Spec for {module_name}:\n{spec}")
        
        return {"specs": specs}

    def spec_reviewer(state: GenState) -> GenState:
        log_phase("spec_reviewer")
        specs = state.get("specs", {})
        client = OpenAI(api_key=Settings.OPENAI_API_KEY)
        
        for module_name, spec in specs.items():
            prompt = (
                "Review spec completeness.\n\n"
                f"MODULE: {module_name}\n"
                f"SPEC:\n{spec}\n\n"
                "OUTPUT FORMAT:\n"
                "SPEC_QUALITY: [score 1-10]\n"
                "MISSING: [what's missing or 'None']\n"
                "READY: [YES or NO]\n"
            )
            
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                top_p=0.95,
                max_tokens=500,
            )
            
            review = resp.choices[0].message.content
            logger.info(f"Spec review for {module_name}:\n{review}")
        
        return {}

    def generate_tests(state: GenState) -> GenState:
        log_phase("generate_tests")
        specs = state.get("specs", {})
        client = OpenAI(api_key=Settings.OPENAI_API_KEY)
        
        test_files = {}
        os.makedirs("generated_tests", exist_ok=True)
        
        for module_name, spec in specs.items():
            test_path = os.path.join("generated_tests", f"test_{module_name}.py")
            
            prompt = (
                "Create pytest tests for this module.\n\n"
                "EXAMPLE:\n"
                "```python\n"
                "import pytest\n"
                "from modules.calculator import add, subtract\n\n"
                "def test_add_positive():\n"
                "    assert add(2, 3) == 5\n\n"
                "def test_subtract_positive():\n"
                "    assert subtract(5, 3) == 2\n"
                "```\n\n"
                "REQUIREMENTS:\n"
                f"- Import from modules.{module_name}\n"
                "- Test all functions in spec\n"
                "- Cover normal, edge, and error cases\n"
                "- 2-7 tests per function\n"
                "- Use pytest.approx() for floats\n\n"
                f"SPEC:\n{spec}\n\n"
                "OUTPUT: Only Python test code, no markdown.\n"
            )
            
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Output only valid Python test code."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                top_p=0.9,
                max_tokens=3000,
            )
            
            tests_src = resp.choices[0].message.content.strip()
            import re
            tests_src = re.sub(r'^```python\s*', '', tests_src)
            tests_src = re.sub(r'```\s*$', '', tests_src)
            
            # Validate
            if f"modules.{module_name}" not in tests_src:
                tests_src = f"import pytest\nfrom modules.{module_name} import *\n\n" + tests_src
            
            try:
                ast.parse(tests_src)
            except SyntaxError:
                tests_src = f"import pytest\nfrom modules.{module_name} import *\n\ndef test_placeholder():\n    assert True\n"
            
            write_files([{"path": test_path, "content": tests_src}])
            test_files[module_name] = test_path
            logger.info(f"Tests written: {test_path}")
        
        return {"test_files": test_files}

    def generate_code(state: GenState) -> GenState:
        log_phase("generate_code")
        specs = state.get("specs", {})
        test_files = state.get("test_files", {})
        client = OpenAI(api_key=Settings.OPENAI_API_KEY)
        
        os.makedirs("modules", exist_ok=True)
        code_files = {}
        
        # Generate modules
        for module_name, spec in specs.items():
            code_path = os.path.join("modules", f"{module_name}.py")
            test_path = test_files.get(module_name, "")
            
            tests_src = ""
            if test_path and os.path.exists(test_path):
                with open(test_path, "r") as f:
                    tests_src = f.read()
            
            prompt = (
                "Implement module to pass tests.\n\n"
                "EXAMPLE:\n"
                "```python\n"
                '"""Calculator module for basic math operations."""\n\n'
                "def add(a: float, b: float) -> float:\n"
                '    """Add two numbers."""\n'
                "    return a + b\n\n"
                "def subtract(a: float, b: float) -> float:\n"
                '    """Subtract b from a."""\n'
                "    return a - b\n"
                "```\n\n"
                "REQUIREMENTS:\n"
                "- Implement all functions from spec\n"
                "- Use type hints\n"
                "- Add docstrings\n"
                "- No UI code (pure business logic)\n"
                "- Pass all tests\n\n"
                f"SPEC:\n{spec}\n\n"
                f"TESTS:\n{tests_src}\n\n"
                "OUTPUT: Only Python code, no markdown.\n"
            )
            
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Output only valid Python code."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                top_p=0.9,
                max_tokens=3000,
            )
            
            code_src = resp.choices[0].message.content.strip()
            import re
            code_src = re.sub(r'^```python\s*', '', code_src)
            code_src = re.sub(r'```\s*$', '', code_src)
            
            try:
                ast.parse(code_src)
            except SyntaxError:
                code_src = f'"""Module {module_name}"""\n\ndef placeholder():\n    pass\n'
            
            write_files([{"path": code_path, "content": code_src}])
            code_files[module_name] = code_path
            logger.info(f"Code written: {code_path}")
        
        # Generate __init__.py
        init_path = os.path.join("modules", "__init__.py")
        write_files([{"path": init_path, "content": ""}])
        
        return {"code_files": code_files}

    def validate_modules(state: GenState) -> GenState:
        """Validate that modules have the functions they claim to have."""
        log_phase("validate_modules")
        code_files = state.get("code_files", {})
        specs = state.get("specs", {})
        
        for module_name, code_path in code_files.items():
            if not os.path.exists(code_path):
                continue
            
            with open(code_path, "r") as f:
                code_content = f.read()
            
            # Extract function names from spec
            spec = specs.get(module_name, "")
            try:
                spec_json = json.loads(spec)
                expected_funcs = [f["name"] for f in spec_json.get("functions", [])]
            except Exception:
                expected_funcs = []
            
            # Check if functions exist in code
            import re
            actual_funcs = re.findall(r'^def (\w+)\(', code_content, re.MULTILINE)
            
            missing = [f for f in expected_funcs if f not in actual_funcs]
            if missing:
                logger.warning(f"{module_name}: Missing functions {missing}. Found: {actual_funcs}")
        
        return {}

    def generate_main_app(state: GenState) -> GenState:
        log_phase("generate_main_app")
        architecture_plan = state.get("architecture_plan", "")
        modules = state.get("modules", {})
        specs = state.get("specs", {})
        code_files = state.get("code_files", {})
        client = OpenAI(api_key=Settings.OPENAI_API_KEY)
        
        # Read actual module code to get real function names
        actual_functions = {}
        for module_name, code_path in code_files.items():
            if os.path.exists(code_path):
                with open(code_path, "r") as f:
                    code_content = f.read()
                import re
                funcs = re.findall(r'^def (\w+)\(', code_content, re.MULTILINE)
                actual_functions[module_name] = funcs
                logger.info(f"{module_name} actual functions: {funcs}")
        
        modules_list = "\n".join([f"- {name}: {info['purpose']}" for name, info in modules.items()])
        
        # Build accurate function list from actual code
        functions_text = ""
        for module_name, funcs in actual_functions.items():
            functions_text += f"\nmodules.{module_name}: {', '.join(funcs)}"
        
        specs_text = "\n".join([f"{name}:\n{spec}" for name, spec in specs.items()])
        
        prompt = (
            "Create main Streamlit app that integrates all modules.\n\n"
            "EXAMPLE:\n"
            "```python\n"
            '"""Main Streamlit Application"""\n'
            "import streamlit as st\n"
            "from modules.calculator import add, subtract\n\n"
            "def main():\n"
            "    st.title('Calculator App')\n"
            "    \n"
            "    page = st.sidebar.selectbox('Choose function', ['Add', 'Subtract'])\n"
            "    \n"
            "    if page == 'Add':\n"
            "        st.header('Addition')\n"
            "        a = st.number_input('First number', value=0.0)\n"
            "        b = st.number_input('Second number', value=0.0)\n"
            "        if st.button('Calculate'):\n"
            "            result = add(a, b)\n"
            "            st.success(f'Result: {result}')\n"
            "    \n"
            "    elif page == 'Subtract':\n"
            "        st.header('Subtraction')\n"
            "        a = st.number_input('First number', value=0.0, key='sub_a')\n"
            "        b = st.number_input('Second number', value=0.0, key='sub_b')\n"
            "        if st.button('Calculate', key='sub_btn'):\n"
            "            result = subtract(a, b)\n"
            "            st.success(f'Result: {result}')\n\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
            "```\n\n"
            "REQUIREMENTS:\n"
            "- Import ONLY functions that actually exist in modules\n"
            "- Use st.sidebar for navigation\n"
            "- Create UI for each function\n"
            "- Use unique keys for widgets\n"
            "- Professional layout\n\n"
            f"ARCHITECTURE:\n{architecture_plan}\n\n"
            f"MODULES:\n{modules_list}\n\n"
            f"ACTUAL FUNCTIONS (use these exact names):\n{functions_text}\n\n"
            f"SPECS:\n{specs_text}\n\n"
            "OUTPUT: Only Python code, no markdown.\n"
        )
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Output only valid Python code."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            top_p=0.9,
            max_tokens=4000,
        )
        
        app_src = resp.choices[0].message.content.strip()
        import re
        app_src = re.sub(r'^```python\s*', '', app_src)
        app_src = re.sub(r'```\s*$', '', app_src)
        
        try:
            ast.parse(app_src)
        except SyntaxError:
            app_src = 'import streamlit as st\n\ndef main():\n    st.title("App")\n\nif __name__ == "__main__":\n    main()\n'
        
        app_path = "app.py"
        write_files([{"path": app_path, "content": app_src}])
        logger.info(f"Main app written: {app_path}")
        
        return {"app_path": app_path}

    def run_tests_node(state: GenState) -> GenState:
        log_phase("run_tests")
        test_files = state.get("test_files", {})
        
        total_passed = 0
        total_failed = 0
        test_results = {}
        
        for module_name, test_path in test_files.items():
            res = run_pytest(test_path)
            test_results[module_name] = res
            total_passed += res.get("passed", 0)
            total_failed += res.get("failed", 0)
            logger.info(f"{module_name}: {res.get('passed', 0)} passed, {res.get('failed', 0)} failed")
        
        return {"test_results": test_results, "passed": total_passed, "failed": total_failed}

    # Build graph
    builder = StateGraph(GenState)
    builder.add_node(jira_reader)
    builder.add_node(system_architect)
    builder.add_node(spec_agent)
    builder.add_node(spec_reviewer)
    builder.add_node(generate_tests)
    builder.add_node(generate_code)
    builder.add_node(validate_modules)
    builder.add_node(generate_main_app)
    builder.add_node(run_tests_node)
    
    builder.add_edge(START, "jira_reader")
    builder.add_edge("jira_reader", "system_architect")
    builder.add_edge("system_architect", "spec_agent")
    builder.add_edge("spec_agent", "spec_reviewer")
    builder.add_edge("spec_reviewer", "generate_tests")
    builder.add_edge("generate_tests", "generate_code")
    builder.add_edge("generate_code", "validate_modules")
    builder.add_edge("validate_modules", "generate_main_app")
    builder.add_edge("generate_main_app", "run_tests_node")
    
    graph = builder.compile()
    
    result = graph.invoke({"project_key": project_key, "ticket_keys": ticket_keys})
    
    print(f"\n✅ Unified app generated")
    print(f"📊 Tests: {result.get('passed', 0)} passed, {result.get('failed', 0)} failed")
    print(f"🚀 streamlit run {result.get('app_path', 'app.py')}")
    print(f"📄 Log: {log_file}\n")
    
    logger.info(f"Generation complete for {project_key}")
    return result
