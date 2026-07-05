# Explain

Plan: 1) show the runtime flow, 2) point to the key code locations, 3) give a few implementation notes.

**Flow:**  
- **Prompt generation:** `format_document(doc_id)` returns a list containing a `base.UserMessage` with the textual prompt (see mcp_server.py).  
- **Framework → model:** The MCP framework sends that message to the model/agent as the user prompt. The prompt contains the `doc_id` but not the document contents.  
- **Tool calls (model-driven):** The model can call registered tools exposed by the framework — e.g., `read_doc_contents` and `edit_document` (see their definitions in mcp_server.py). When the model invokes a tool, the framework runs the corresponding Python function on the server.  
- **Document read/edit:** Typical sequence: model calls `read_doc_contents(doc_id)` → server runs `read_document` and returns the current text; model decides edits and calls `edit_document(doc_id, old_str, new_str)` → server runs `edit_document` which updates the `docs` dict.  
- **Final response:** After using tools, the model returns the final reformatted document as its message; the framework forwards that back to the caller.

**Key code:**  
- **Prompt builder:** `format_document` — creates the instruction the model will follow (mcp_server.py).  
- **Read tool:** `read_document` registered as `read_doc_contents` — returns the document string (mcp_server.py).  
- **Edit tool:** `edit_document` — performs text replacement on the in-memory `docs` dict (mcp_server.py).  
- **Resources:** `list_docs` / `fetch_doc` register read-only endpoints (mcp_server.py).

**Notes / implications:**  
- The prompt instructs the model to use `edit_document` but the actual edit happens on the server when the tool is invoked — the prompt function itself performs no edits.  
- The prompt embeds `doc_id` as plain text; the model must call `read_doc_contents` to obtain the document.  
- Annotations (`-> list[base.Message]`) and `base.UserMessage` are used so the framework can build role-marked messages for the model.  
- Tool use is model-driven: if the model ignores the tool instructions, no edit occurs unless you enforce tool usage in the framework.

Want a traced example of a model-tool exchange (sample tool calls/responses)?