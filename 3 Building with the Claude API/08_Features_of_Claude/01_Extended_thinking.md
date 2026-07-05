## Extended thinking

#### Downloads

- [001_thinking_complete.ipynb(opens in new tab)](https://cc.sj-cdn.net/instructor/4hdejjwplbrm-anthropic/assets/1762980359/001_thinking_complete.ipynb?response-content-disposition=attachment&Expires=1778848251&Signature=V80FzZg8dQ8HgVyxgcQ57lR8gZpKyKHEW9DKGDLr4Gm0c0KN4hoii8T-vqOmXDn2~Qzm5YYmd6Ves0yjVlCyUMtepP97FXIAwlJ14Fw-5EVBJYL81heymHbxIhSaGeCrv3BT70rQE8ezhEEQ43MkI6adT4KElzZjiosgI~3XVfurpuABDP32rrRtcbOtO~1V4~HFjsalrj3d9FqYhIH58BXcgqDBvB~Q0uzG0XfSN5UX2UcNNU02pjvCKdjK2q0aRs4q6m~XHM4Mm-5OFC0GkQtKNssULY231C66BBYRsYkSxIbTteTapzD757j2oMICjl8k0i6Jb7pKjnu~m9YsbA__&Key-Pair-Id=APKAI3B7HFD2VYJQK4MQ)
- [001_thinking.ipynb](https://cc.sj-cdn.net/instructor/4hdejjwplbrm-anthropic/assets/1762980359/001_thinking.ipynb?response-content-disposition=attachment&Expires=1778848252&Signature=t2IiMl2QNoJULxRIvdtm20Wh6SQMsequpC1qiaKmgZX5jCMiWMfJQmmljp0TBr~LQehxcFbTBBnZ7IgP2LWcp8v7hfhq~0hDzJah7wgGOtjLclYWuMlC~C4Kjs2WYNtLeSg9Kza-fOk3eXQi7FwaEMgw9rbSleb48hx1-qwoUbQonTJZWCZkV-YFAVZHQILeNoJKM7x1O8RilYjuTNjauaO3WftumioqxlYTmwGEXGFepl~6~c~nhI5oNMH43BCyOxHyG8iUnO5MI2bAZrs6gSeDCnlj~NkIgi76YEOZ3JprG0FUqvSfQvDA4aDvfhWubFr1fqvrR81XKhigR6liNw__&Key-Pair-Id=APKAI3B7HFD2VYJQK4MQ)

**Important Note: Extended Thinking is not compatible with some other features, notable message pre-filling and temperature. See the full list of restrictions here:** [**https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking#feature-compatibility**](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking#feature-compatibility)

 

Extended thinking is Claude's advanced reasoning feature that gives the model time to work through complex problems before generating a final response. Think of it as Claude's "scratch paper" - you can see the reasoning process that leads to the answer, which helps with transparency and often results in better quality responses.

## How Extended Thinking Works

When extended thinking is enabled, Claude's response changes from a simple text block to a structured response containing two parts:

![img](01_Extended_thinking.assets/08_-_001_-_Extended_Thinking_04.jpg)

With thinking enabled, you get both the reasoning process and the final answer:

![img](01_Extended_thinking.assets/08_-_001_-_Extended_Thinking_05.jpg)

The key benefits include:

- Better reasoning capabilities for complex tasks
- Increased accuracy on difficult problems
- Transparency into Claude's thought process

However, there are important trade-offs:

- Higher costs (you pay for thinking tokens)
- Increased latency (thinking takes time)
- More complex response handling in your code

## When to Use Extended Thinking

The decision is straightforward: use your prompt evaluations. Run your prompts without thinking first, and if the accuracy isn't meeting your requirements after you've already optimized your prompt, then consider enabling extended thinking. It's a tool for when standard prompting isn't quite getting you there.

## Response Structure and Security

Extended thinking responses include a special signature system for security:

![img](01_Extended_thinking.assets/08_-_001_-_Extended_Thinking_06.jpg)

The signature is a cryptographic token that ensures you haven't modified the thinking text. This prevents developers from tampering with Claude's reasoning process, which could potentially lead the model in unsafe directions.

## Redacted Thinking

Sometimes you'll receive a redacted thinking block instead of readable reasoning text:

![img](01_Extended_thinking.assets/08_-_001_-_Extended_Thinking_08.jpg)

This happens when Claude's thinking process gets flagged by internal safety systems. The redacted content contains the actual thinking in encrypted form, allowing you to pass the complete message back to Claude in future conversations without losing context.

## Implementation

To enable extended thinking in your code, you need to add two parameters to your chat function:

```
def chat(
    messages,
    system=None,
    temperature=1.0,
    stop_sequences=[],
    tools=None,
    thinking=False,
    thinking_budget=1024
):
```

The thinking budget sets the maximum tokens Claude can use for reasoning. The minimum value is 1024 tokens, and your `max_tokens` parameter must be greater than your thinking budget.

Add the thinking configuration to your API parameters:

```
if thinking:
    params["thinking"] = {
        "type": "enabled",
        "budget": thinking_budget
    }
```

Then call it with thinking enabled:

```
chat(messages, thinking=True)
```

## Testing Redacted Responses

For testing purposes, you can force Claude to return a redacted thinking block by sending a special trigger string. This helps ensure your application handles redacted responses gracefully without crashing.

Extended thinking is a powerful feature when you need Claude to tackle complex reasoning tasks, but use it judiciously given the cost and latency implications. Start with standard prompting, optimize thoroughly, then add thinking when you need that extra reasoning capability.