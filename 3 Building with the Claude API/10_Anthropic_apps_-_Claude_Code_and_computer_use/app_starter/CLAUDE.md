# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Commands

| Purpose | Command |
|---|---|
| Run MCP server | `uv run main.py` |
| Run tests | `uv run pytest` |
| Format (whole project) | `uvx ruff format .` |
| Lint (whole project) | `uvx ruff check --fix .` |

Individual `.py` files are auto-formatted and linted via a PostToolUse hook on every Write/Edit — no manual step needed.

## Skills

Use `/add-mcp-tool <name>` to scaffold a new tool: creates `tools/<name>.py` with the correct structure, adds a test file, and registers it in `main.py`.

## Defining MCP Tools

Tools are Python functions registered with the MCP server. **Registration is manual** — adding a function to `tools/` does NOT register it automatically. For each new tool, you must add the import and registration call to `main.py`:

```python
from tools.my_module import my_function
mcp.tool()(my_function)
```

Do not register functions that are not intended as public tools. `binary_document_to_markdown` in `tools/document.py` is intentionally unregistered (it is an example only).

### Tool function structure

Every tool function must follow this exact pattern:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does"),
) -> ReturnType:
    """One-line summary of what this tool does.

    Detailed explanation of the functionality and behavior.

    When to use:
    - Scenario A
    - Scenario B

    When NOT to use:
    - Scenario C

    Examples:
    >>> my_tool("foo", 42)
    "expected result"
    """
```

Rules:
- All parameters **must** use `pydantic.Field(description="...")` — plain type annotations are not sufficient; the MCP client uses these descriptions to understand the parameter.
- The function docstring is what the MCP client sees as the tool's description; make it thorough.
- Return type annotations are required.
- Place each tool in its own module under `tools/`.

### Tests

Add fixture files (`.docx`, `.pdf`, etc.) to `tests/fixtures/` when testing document tools. Run a single test with:

```bash
uv run pytest tests/test_my_module.py::test_my_function
```
