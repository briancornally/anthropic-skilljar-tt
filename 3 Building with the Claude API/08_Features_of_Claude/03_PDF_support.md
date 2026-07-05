## PDF support

#### Downloads

- [earth.pdf](https://cc.sj-cdn.net/instructor/4hdejjwplbrm-anthropic-poc/assets/1748559008/earth.pdf?response-content-disposition=attachment&Expires=1778848374&Signature=ee3h6l1r5E3ldKx0IijmdsoNJluv~~e4baKXZ2GQe30tjeED6-KnI1w7vUpaPj8~JqIeLoWVi6nklKSWXMDIKYQdeTnCjikS2gwDuVXZ2ZFYpPbcP2xUIImTFTLr2cYTYtFdYxQ81Qh5o5SIdkOVdxPjJTd7jnInDeea7LjV6NhFB3mn0vzLa-xKYH8sJo-FwpGtvKd1dReLM80kHz1ne5v7hf4hgu8C~JktA8X304em4hsWvQMP4DrJhd6fgiM4DU2or9~jx0aA4zBmxr9iQQBdxBuReXNq5~I6xrGJgLB7GkBBybfd-mklkwZLRrcwW~dDpyqhEw3v1eqVlcnuZA__&Key-Pair-Id=APKAI3B7HFD2VYJQK4MQ)

Claude can read and analyze PDF files directly, making it a powerful tool for document processing. This capability works similarly to image processing, but with a few key differences in how you structure your code.

## Setting Up PDF Processing

To process a PDF file with Claude, you'll use nearly identical code to what you'd use for images. The main differences are in the file type specifications and variable names for clarity.

Here's how to modify your existing image processing code for PDFs:

```
with open("earth.pdf", "rb") as f:
    file_bytes = base64.standard_b64encode(f.read()).decode("utf-8")

messages = []

add_user_message(
    messages,
    [
        {
            "type": "document",
            "source": {
                "type": "base64",
                "media_type": "application/pdf",
                "data": file_bytes,
            },
        },
        {"type": "text", "text": "Summarize the document in one sentence"},
    ],
)

chat(messages)
```

## Key Changes from Image Processing

When adapting your image processing code for PDFs, you need to update several elements:

- Change the file extension from `.png` to `.pdf`
- Update the variable name from `image_bytes` to `file_bytes` for clarity
- Set the type to `"document"` instead of `"image"`
- Change the media type to `"application/pdf"` instead of `"image/png"`

## What Claude Can Extract from PDFs

Claude's PDF processing capabilities go beyond simple text extraction. It can analyze and understand:

- Text content throughout the document
- Images and charts embedded in the PDF
- Tables and their data relationships
- Document structure and formatting

This makes Claude essentially a one-stop solution for extracting any type of information from PDF documents, whether you need summaries, data analysis, or specific content extraction.

![img](03_PDF_support.assets/08_-_003_-_PDF_Support_02.jpg)

The example above shows Claude successfully processing a Wikipedia article about Earth that was saved as a PDF, demonstrating how it can understand and summarize complex document content in a single sentence.