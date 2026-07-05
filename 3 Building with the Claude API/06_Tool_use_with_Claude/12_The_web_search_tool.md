## The web search tool

#### Downloads

- [006_web_search.ipynb(opens in new tab)](https://cc.sj-cdn.net/instructor/4hdejjwplbrm-anthropic/assets/1762980062/006_web_search.ipynb?response-content-disposition=attachment&Expires=1778758627&Signature=MgflyeVohHnV7AcaseRDfR2Xxo9wt2hYwU2WA89cHFW990h56E0Et3OqkyNVKpoPvvznzq-CL88e6uVVXu6EkXq7Q2SFQZFBzR075LCqN2trV7G0OkhFl6bdfjOWq3GmAkKA5HOrCCEjns9zw0p0VySugTWXoYLVmyFZouEmcVmN3etK1n433cSbhZ8NGxOfEW8idwR0ULXEgnUWaJJv56eD~OcQii~60TgCS-t1kkHmDaO8HvnIPqjBuXX5o1nfJRnsqEd2JeCmFt5w6GmhnNkLj9~p5-7JNEsUqYbEcVvvkEor5~jPSTWSomBBmFZ2MDjrNwEfLiF~zTYpgE~7KQ__&Key-Pair-Id=APKAI3B7HFD2VYJQK4MQ)
- [006_web_search_complete.ipynb](https://cc.sj-cdn.net/instructor/4hdejjwplbrm-anthropic/assets/1762980063/006_web_search_complete.ipynb?response-content-disposition=attachment&Expires=1778758627&Signature=ltw20VH51t9WUuadmmSXEfCso~QhqEyGQu4sL5z-3solj95pLAHiK~pC5L9YVoCBxVDos3skFzBc40L5jF1fomdO7dt3VjiytCc0s4hXQT10eltIxpIQbiJiiLWPAxhD143MxDFIKkwP4OjIE9Q~bCKNN5ZY06f0rc1Z6ewkgt30felVNSUZUeyTCMZsAupXVCdbKogCKtZrXEfH~FHhJ~wEz8FxsxjpS8Bg894-QFYw8N3th85qbwMXHKJAwDNoankxMpxGgOE6eaWyA9DGU4vgLlbsq8NB9Q7NlT1PAxbvSZNJbGKSjzGxL0c4o24~YouwQ4KoIedav1WkjTwpfQ__&Key-Pair-Id=APKAI3B7HFD2VYJQK4MQ)

**Important note:** Your organization must enable the Web Search tool in the settings console before using it. You can find this setting here: https://console.anthropic.com/settings/privacy

Claude includes a built-in web search tool that lets it search the internet for current or specialized information to answer user questions. Unlike other tools where you need to provide the implementation, Claude handles the entire search process automatically - you just need to provide a simple schema to enable it.

![img](12_The_web_search_tool.assets/06_-_013_-_The_Web_Search_Tool_00.png)

## Setting Up the Web Search Tool

To use the web search tool, you create a schema object with these required fields:

```
web_search_schema = {
    "type": "web_search_20250305",
    "name": "web_search", 
    "max_uses": 5
}
```

The `max_uses` field limits how many searches Claude can perform. Claude might do follow-up searches based on initial results, so this prevents excessive API calls. A single search returns multiple results, but Claude may decide additional searches are needed.

## How the Response Works

When Claude uses the web search tool, the response contains several types of blocks:

- **Text blocks** - Claude's explanation of what it's doing
- **ServerToolUseBlock** - Shows the exact search query Claude used
- **WebSearchToolResultBlock** - Contains the search results
- **WebSearchResultBlock** - Individual search results with titles and URLs
- **Citation blocks** - Text that supports Claude's statements

![img](12_The_web_search_tool.assets/06_-_013_-_The_Web_Search_Tool_07.png)

The response structure lets you see exactly what Claude searched for and which sources it found. Citations include the specific text Claude used to support its answers, along with the source URLs.

## Restricting Search Domains

You can limit searches to specific domains using the `allowed_domains` field. This is particularly useful when you want reliable, authoritative sources:

```
web_search_schema = {
    "type": "web_search_20250305",
    "name": "web_search",
    "max_uses": 5,
    "allowed_domains": ["nih.gov"]
}
```

For example, when asking about medical or exercise advice, restricting to domains like PubMed (nih.gov) ensures you get evidence-based information rather than random blog content.

![img](12_The_web_search_tool.assets/06_-_013_-_The_Web_Search_Tool_13.png)

## Rendering Search Results

The different block types in the response are designed for specific UI rendering:

- Render text blocks as regular content
- Display web search results as a list of sources at the top
- Show citations inline with the text, including the source domain, page title, URL, and quoted text

![img](12_The_web_search_tool.assets/06_-_013_-_The_Web_Search_Tool_17.png)

This structure helps users understand how Claude arrived at its answers and provides transparency about the sources being used. The citation format makes it clear which specific information came from which sources, building trust in the AI's responses.

## Practical Usage

The web search tool works best for:

- Current events and recent developments
- Specialized information not in Claude's training data
- Fact-checking and finding authoritative sources
- Research tasks requiring up-to-date information

Simply include the schema in your tools array when making API calls, and Claude will automatically decide when a web search would help answer the user's question.