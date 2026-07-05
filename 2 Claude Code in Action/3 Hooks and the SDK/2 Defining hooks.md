## Defining hooks

- https://anthropic.skilljar.com/claude-code-in-action/312002

#### Downloads

- [queries.zip](https://cc.sj-cdn.net/instructor/4hdejjwplbrm-anthropic/assets/1773097175/queries.zip?response-content-disposition=attachment&Expires=1776536476&Signature=GSYHmYFFBiFydftbktKQ1yaAbzVmOuM9Ufvs20tyhohhAzevILHys7HrN8Jp9gMVxur6xSnyYWKFUYZs~8XIq9WW0gaLK~RsXV7Y7ndFreqlOiq~-lToRDKkp69KrgwPxVHCc3LfffDLiOfhey6dwXibZpep9U9~2T0GryuZnbVe0EqokWNtI3mgVQO82N2z2W3D81-fJXffxV2FnXqH~lDIWZ7Q9eg6LwQHbG7l1Yju4PdJwIFEA1VIJpQJxjfL4DVQtnTUwyAatsIBAH~amU647r-kaLp2fwOCzxfMhaLGkZlBvSxPJIaAZNSgIJAebvvqhM~5pGa-ajSMjJCEPg__&Key-Pair-Id=APKAI3B7HFD2VYJQK4MQ)
- [queries_COMPLETED.zip](https://cc.sj-cdn.net/instructor/4hdejjwplbrm-anthropic/assets/1773097185/queries_COMPLETED.zip?response-content-disposition=attachment&Expires=1776628297&Signature=DHb27VGfbgBvYYghkyosX3vC0qDvD0UL5rII0JK~Dm9KPcdb01wLW4xqLfib8~Bx7QvUdIddabRWxIwY1pxCj86oa1MdImlHd0QXH3koLdkAQMah~Ngl54AkW-3yyyRGphKuF589s2fCR4VK~dhbhMVS7rPUEj1dAtpsX5k7K3ZnAu8eQpXwRxpCpsm0S4DM5me00DxxjOWp1plLkQt27nbebt9aM73iUjTCaFAbyr~KMlbJPJKE1xm7u08RLMBGN9U47OBSc~rusIHzwA85413J0F4UXQU891NYNqjmHtHISd0ZhXjFNw1WGO58WlT0n8la6HWwfAlpHvj63EDOdg__&Key-Pair-Id=APKAI3B7HFD2VYJQK4MQ)

Hooks in Claude Code allow you to intercept and control tool calls before or after they execute. This gives you fine-grained control over what Claude can and cannot do in your development environment.

## Building a Hook

Creating a hook involves four main steps:

![img](assets/011_-_Defining_Hooks_05.png)

1. **Decide on a PreToolUse or PostToolUse hook** - PreToolUse hooks can prevent tool calls from executing, while PostToolUse hooks run after the tool has already been used
2. **Determine which type of tool calls you want to watch for** - You need to specify exactly which tools should trigger your hook
3. **Write a command that will receive the tool call** - This command gets JSON data about the proposed tool call via standard input
4. **If needed, command should provide feedback to Claude** - Your command's exit code tells Claude whether to allow or block the operation

## Available Tools

Claude Code provides several built-in tools that you can monitor with hooks:

![img](assets/011_-_Defining_Hooks_07.png)

To see exactly which tools are available in your current setup, you can ask Claude directly for a list. This is especially useful since the available tools can change when you add custom MCP servers.

 

## Tool Call Data Structure

When your hook command executes, Claude sends JSON data through standard input containing details about the proposed tool call:

![img](assets/011_-_Defining_Hooks_11.png)

```
{
  "session_id": "2d6a1e4d-6...",
  "transcript_path": "/Users/sg/...",
  "hook_event_name": "PreToolUse",
  "tool_name": "Read",
  "tool_input": {
    "file_path": "/code/queries/.env"
  }
}
```

Your command reads this JSON from standard input, parses it, and then decides whether to allow or block the operation based on the tool name and input parameters.

## Exit Codes and Control Flow

Your hook command communicates back to Claude through exit codes:

![img](assets/011_-_Defining_Hooks_16.png)

- **Exit Code 0** - Everything is fine, allow the tool call to proceed
- **Exit Code 2** - Block the tool call (PreToolUse hooks only)

When you exit with code 2 in a PreToolUse hook, any error messages you write to standard error will be sent to Claude as feedback, explaining why the operation was blocked.

## Example Use Case

A common use case is preventing Claude from reading sensitive files like `.env` files. Since both the `Read` and `Grep` tools can access file contents, you'd want to monitor both tool types and check if they're trying to access restricted file paths.

This approach gives you complete control over Claude's file system access while providing clear feedback about why certain operations are restricted.

#### Downloads

- [queries.zip](https://cc.sj-cdn.net/instructor/4hdejjwplbrm-anthropic/assets/1773097175/queries.zip?response-content-disposition=attachment&Expires=1776536476&Signature=GSYHmYFFBiFydftbktKQ1yaAbzVmOuM9Ufvs20tyhohhAzevILHys7HrN8Jp9gMVxur6xSnyYWKFUYZs~8XIq9WW0gaLK~RsXV7Y7ndFreqlOiq~-lToRDKkp69KrgwPxVHCc3LfffDLiOfhey6dwXibZpep9U9~2T0GryuZnbVe0EqokWNtI3mgVQO82N2z2W3D81-fJXffxV2FnXqH~lDIWZ7Q9eg6LwQHbG7l1Yju4PdJwIFEA1VIJpQJxjfL4DVQtnTUwyAatsIBAH~amU647r-kaLp2fwOCzxfMhaLGkZlBvSxPJIaAZNSgIJAebvvqhM~5pGa-ajSMjJCEPg__&Key-Pair-Id=APKAI3B7HFD2VYJQK4MQ)