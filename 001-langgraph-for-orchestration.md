# ADR 001: Use LangGraph for Agent Orchestration

**Date**: 2024-05-22

**Status**: Accepted

## Context

The project requires a robust way to orchestrate multiple AI agents (e.g., architect, coder, tester) in a complex workflow. The workflow involves conditional logic (e.g., fixing failing tests), loops, and a shared state that evolves over time. We considered simple Python scripts with function calls versus a dedicated orchestration framework.

## Decision

We will use LangGraph as the primary framework for defining and executing our agentic workflows.

## Consequences

### Positive:

- **State Management**: LangGraph provides a built-in, explicit state management system (`GenState` TypedDict), which makes data flow between agents clear and debuggable.
- **Cyclical Graphs**: It natively supports cycles, which is essential for our iterative test-fix-review loops.
- **Visualization**: The ability to compile the graph and print a diagram (`graph.get_graph().print_ascii()`) is invaluable for visualizing and debugging the complex flow.
- **Modularity**: It encourages breaking down the workflow into discrete, testable nodes (agents).

### Negative:

- **Learning Curve**: There is a slight learning curve compared to a simple Python script.
- **Boilerplate**: Defining the state and graph structure can introduce some initial boilerplate code.
