---
name: add-mcp-tool
description: Scaffold a new MCP tool in this repo. Creates the tool function in tools/<name>.py with the correct docstring structure and pydantic.Field parameters, adds tests, and registers it in main.py.
disable-model-invocation: true
---

The user wants to add a new MCP tool. $ARGUMENTS contains the tool name and/or a description of what it should do.

Follow these steps in order:

1. **Clarify** (if $ARGUMENTS is vague): ask what the tool should do, what parameters it takes, and what it returns.

2. **Create `tools/<tool_name>.py`** with this exact structure:

```python
from pydantic import Field


def <tool_name>(
    param1: <type> = Field(description="<detailed description>"),
    # ... additional params
) -> <ReturnType>:
    """One-line summary.

    Detailed explanation of the functionality and behavior.

    When to use:
    - <scenario>

    When NOT to use:
    - <scenario>

    Examples:
    >>> <tool_name>(<example_args>)
    <expected_result>
    """
    # implementation
```

   - Every parameter must use `pydantic.Field(description="...")`.
   - Return type annotation is required.
   - The docstring is what the MCP client sees — make it thorough.

3. **Register in `main.py`**: add the import and `mcp.tool()()` call alongside the existing registrations:

```python
from tools.<tool_name> import <tool_name>
mcp.tool()(<tool_name>)
```

4. **Add a test** in `tests/test_<tool_name>.py` covering at least one happy-path case and one edge case. If the tool processes documents, add a fixture file to `tests/fixtures/`.

5. **Run tests** with `uv run pytest tests/test_<tool_name>.py` and confirm they pass.
