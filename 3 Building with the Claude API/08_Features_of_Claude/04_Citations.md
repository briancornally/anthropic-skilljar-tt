## Citations

#### Downloads

- [002_citations_complete.ipynb(opens in new tab)](https://cc.sj-cdn.net/instructor/4hdejjwplbrm-anthropic/assets/1762980791/002_citations_complete.ipynb?response-content-disposition=attachment&Expires=1778848375&Signature=Lsq7exlY1xqWLGlUNt8ZDxg6pqUSGMjcncxu9-ce3ATTxiBv8jDrGrti50XurLE4kONX7CxJ7LMEZInzTMEfsMhib7HiMIRyHdoYPyA5P8tuSEjD3w7rVMlsd50A0WUvIZIEtqbZe7p04Hjwt3cJ5jPo6SbNgV8s2sOdT5wSeEqADSXShwszV6qRv~O9NxstncKbvSYBU0X7t7QLWIqla3MdI~LYFykwhXj1DLxx6o6iPhqn1EkDNnzgRFH0YWGDdx66xKZ03yv~k0II2ydCY57jgYGDgni7R5zMMmHAe9vcViiKXSZ98rWk669yRry0u1cngKCU1koybDoWpw4vpg__&Key-Pair-Id=APKAI3B7HFD2VYJQK4MQ)
- [earth.pdf](https://cc.sj-cdn.net/instructor/4hdejjwplbrm-anthropic/assets/1762980798/earth.pdf?response-content-disposition=attachment&Expires=1778848375&Signature=XM4rNPzkpOeVkFnRi6Zc71cINIlEZtL1XzbHxbIRlXG29Md-vqc6JfewGWVUXCT10k-holnCZ3nglkpnNp43nvz1cgSQqFyj3f5OFeCdNX9XDb7ne91yYb63T1LtKh3wttqqvTFLRRJV77OeQ3A6dMCTqVKbg8Je0I0d~iEWwDLIUA5vHbXFvREZA-xyaW3I5PrKGNw3lH3Qebb~yup5h-6~wW~PKbrYD7QXHcur2Nh-qO4-WhgoKwzQtUxcNV2Vndvn-CetsGfKPT42ugrbJAjXcwLC5E~vBXzbYfqlS8tBhJPYDYSC-H3NHFVdxFurvsWkIsA9CNhf-suhBEolRA__&Key-Pair-Id=APKAI3B7HFD2VYJQK4MQ)

When Claude answers questions based on documents you provide, users might assume it's just drawing from its training data. But what if Claude could show exactly where it found specific information? That's where citations come in - a powerful feature that lets Claude reference specific parts of your source documents and show users exactly where each piece of information comes from.

## Why Citations Matter

Imagine asking Claude about how Earth's atmosphere formed and getting a detailed answer. Without citations, users have no way to verify the information or understand that Claude is actually referencing a specific document you provided. Citations solve this transparency problem by creating a clear trail from Claude's response back to your source material.

![img](04_Citations.assets/08_-_004_-_Citations_00.jpg)

## Enabling Citations

To enable citations, you need to modify your document message structure. Add two new fields to your document block:

```
{
    "type": "document",
    "source": {
        "type": "base64",
        "media_type": "application/pdf",
        "data": file_bytes,
    },
    "title": "earth.pdf",
    "citations": { "enabled": True }
}
```

The `title` field gives your document a readable name, while `citations: {"enabled": True}` tells Claude to track where it finds information.

## Understanding Citation Structure

When citations are enabled, Claude's response becomes more complex. Instead of simple text, you get structured data that includes citation information for each claim.

![img](04_Citations.assets/08_-_004_-_Citations_08.jpg)

Each citation contains several key pieces of information:

- **cited_text** - The exact text from your document that supports Claude's statement
- **document_index** - Which document Claude is referencing (useful when you provide multiple documents)
- **document_title** - The title you assigned to the document
- **start_page_number** - Where the cited text begins
- **end_page_number** - Where the cited text ends

![img](04_Citations.assets/08_-_004_-_Citations_09.jpg)

## Building User Interfaces with Citations

The real power of citations comes from building user interfaces that make this information accessible. You can create interactive elements where users can hover over citation markers to see exactly where information came from.

![img](04_Citations.assets/08_-_004_-_Citations_11.jpg)

This creates a transparent experience where users can:

- See that Claude's answers are grounded in actual source material
- Verify the information by checking the original document
- Understand the context around each cited piece of information

## Citations with Plain Text

Citations aren't limited to PDF documents. You can also use them with plain text sources. When working with text, modify your document structure like this:

```
{
    "type": "document", 
    "source": {
        "type": "text",
        "media_type": "text/plain",
        "data": article_text,
    },
    "title": "earth_article",
    "citations": { "enabled": True }
}
```

With plain text sources, instead of page numbers, you'll get character positions that pinpoint exactly where in the text Claude found each piece of information.

## When to Use Citations

Citations are particularly valuable when:

- Users need to verify information for accuracy
- You're working with authoritative documents that users should be able to reference
- Transparency about information sources is critical for your application
- Users might want to explore the broader context around specific facts

By implementing citations, you transform Claude from a "black box" that provides answers into a transparent research assistant that shows its work. This builds user trust and enables them to dive deeper into your source materials when needed.