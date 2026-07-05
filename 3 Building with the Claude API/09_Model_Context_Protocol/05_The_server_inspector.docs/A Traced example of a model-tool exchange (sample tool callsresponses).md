# A Traced example of a model-tool exchange (sample tool calls/responses)

Plan: 1) show the runtime sequence, 2) give a concrete simulated transcript of prompt → tool calls → edits.

**Runtime sequence (short)**  
- Caller asks the MCP to run the `format` prompt for a specific doc id.  
- The framework runs `format_document(doc_id)` (see mcp_server.py) which returns a `base.UserMessage` prompt containing only the `doc_id`.  
- The framework sends that message to the model.  
- The model calls registered tools (e.g. `read_doc_contents`, `edit_document`) as needed. Each tool call is executed by the server (the Python functions in mcp_server.py) and the result is returned to the model.  
- After using tools, the model returns the final reformatted document text as its message.

**Simulated transcript (concrete example)**

1) Client: request format prompt for doc "plan.md"
- API: run prompt `format` with param `{ "doc_id": "plan.md" }`

2) Server: builds prompt by calling `format_document("plan.md")` and sends the following user message to the model:
---
User message (from `format_document`):
Your goal is to reformat a document to be written with markdown syntax.

The id of the document you need to reformat is:
<document_id>
plan.md
</document_id>

Add in headers, bullet points, tables, etc as necessary. Feel free to add in extra text, but don't change the meaning of the report.
Use the 'edit_document' tool to edit the document. After the document has been edited, respond with the final version of the doc. Don't explain your changes.
---

3) Model: decides it needs the doc text and issues a tool call
Tool call: `read_doc_contents` with args
{ "doc_id": "plan.md" }

4) Server: executes `read_document(doc_id)` (the `read_doc_contents` tool) and returns:
"The plan outlines the steps for the project's implementation."

5) Model: constructs a reformatted markdown version and decides to persist it via the tool
Tool call: `edit_document` with args
{
  "doc_id": "plan.md",
  "old_str": "The plan outlines the steps for the project's implementation.",
  "new_str": "# Project Plan\n\n- Overview: Steps for the project's implementation.\n\nDetailed steps:\n1. ...\n2. ..."
}

6) Server: runs `edit_document(...)` which updates the in-memory `docs["plan.md"]` to the new markdown text and returns success (no return value).

7) Model: replies with the final document content (the model’s user-visible response):
# Project Plan

- Overview: Steps for the project's implementation.

Detailed steps:
1. ...
2. ...

(optional) Client or user can then fetch the saved document via the registered resource `docs://documents/{doc_id}` (calls `fetch_doc`) to verify the stored text.

Notes:
- The prompt function (`format_document`) does not itself read or edit the document — it only produces the instruction message including `doc_id`.  
- The actual reads/edits happen when the model issues tool calls and the server executes `read_document`/`edit_document` (see mcp_server.py tools).  
- If the model never calls the tools, no edit occurs.