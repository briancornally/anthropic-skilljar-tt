## Code execution and the Files API

#### Downloads

- [streaming.csv(opens in new tab)](https://cc.sj-cdn.net/instructor/4hdejjwplbrm-anthropic-poc/assets/1748559110/streaming.csv?response-content-disposition=attachment&Expires=1778848378&Signature=mr1H596K8y7d1edJRd5CKlqDwA3Bu24NztP3VkzhRYx6VHyqmiwHlJFkBiAJR8ZgF4cOt-ZwiDAJCMhurEYgVIidmvI3LXwKs~p2sSghB5a8iw5fWhK-UAhbs7NEn4B6L2Uh~DbC2vCeQXbaWY7lRchtzUOknJKsb12UqvLq81fteY3DKNwmdHmYnZAj8I4iVYZAdA-cKk-J~6WotpPSYfRhTq1LznrRtNBsRuEqNE9ekCfqorfU3O3PZHG0HcKtF4Tk8JxvhtMlpyCFR4kH5Mp127j1E4PirY3hJZZjYBjftkCBg6efjPFnepRGiBeVB7nDxl9El5dZzJoUVm0VxA__&Key-Pair-Id=APKAI3B7HFD2VYJQK4MQ)
- [005_code_execution.ipynb](https://cc.sj-cdn.net/instructor/4hdejjwplbrm-anthropic/assets/1762981347/005_code_execution.ipynb?response-content-disposition=attachment&Expires=1778848378&Signature=Emhm8cBJ9htiUU~q~dJfV3frJZLzeMw0mFpYJnBrim6GpwOyWHAJF6m95l5FA75g3OMKNAbq63tQf8zqj3FeAUbeebvjLQTz3iAejqr0z4of4ATwWuVnPzxbkpmp2-mZ3bEaSaorQ2e76WlZiroZ2PtYJBE67QjNecoFdluT3fzuii-iU8VlP9UlX9fqSFIN12P9Oc32yxiU7319huBDwMlTQtsm210NVTg8tLcH97sw8TcgRM8J8NLxA11Spk31LP950YCIzlBPWZsn2T4P02GVWS0PcoYMjqWaPjkCVty8cGoGLjpUPD0hxwZA6lvc~JpV9RhEWw5nLnoDk1lMmw__&Key-Pair-Id=APKAI3B7HFD2VYJQK4MQ)

The Anthropic API offers two powerful features that work exceptionally well together: the Files API and Code Execution. While they might seem separate at first, combining them opens up some really interesting possibilities for delegating complex tasks to Claude.

## Files API

The Files API provides an alternative way to handle file uploads. Instead of encoding images or PDFs directly in your messages as base64 data, you can upload files ahead of time and reference them later.

![img](08_Code_execution_and_the_Files_API.assets/08_-_008_-_Code_Execution_and_the_Files_API_01.jpg)

Here's how it works:

- Upload your file (image, PDF, text, etc.) to Claude using a separate API call
- Receive a file metadata object containing a unique file ID
- Reference that file ID in future messages instead of including raw file data

![img](08_Code_execution_and_the_Files_API.assets/08_-_008_-_Code_Execution_and_the_Files_API_02.jpg)

This approach is particularly useful when you want to reference the same file multiple times or when working with larger files that would be cumbersome to include in every request.

## Code Execution Tool

Code execution is a server-based tool that doesn't require you to provide an implementation. You simply include a predefined tool schema in your request, and Claude can optionally execute Python code in an isolated Docker container.

![img](08_Code_execution_and_the_Files_API.assets/08_-_008_-_Code_Execution_and_the_Files_API_04.jpg)

Key characteristics of the code execution environment:

- Runs in an isolated Docker container
- No network access (can't make external API calls)
- Claude can execute code multiple times during a single conversation
- Results are captured and interpreted by Claude for the final response

## Combining Files API and Code Execution

The real power comes from using these features together. Since the Docker containers have no network access, the Files API becomes the primary way to get data in and out of the execution environment.

![img](08_Code_execution_and_the_Files_API.assets/08_-_008_-_Code_Execution_and_the_Files_API_06.jpg)

Here's a typical workflow:

1. Upload your data file (like a CSV) using the Files API
2. Include a container upload block in your message with the file ID
3. Ask Claude to analyze the data
4. Claude writes and executes code to process your file
5. Claude can generate outputs (like plots) that you can download

## Practical Example

Let's look at a real example using streaming service data. The CSV file contains user information including subscription tiers, viewing habits, and whether they've churned (canceled their subscription).

![img](08_Code_execution_and_the_Files_API.assets/08_-_008_-_Code_Execution_and_the_Files_API_08.jpg)

First, upload the file using a helper function:

```
file_metadata = upload('streaming.csv')
```

Then create a message that includes both the uploaded file and a request for analysis:

```
messages = []
add_user_message(
    messages,
    [
        {
            "type": "text",
            "text": """Run a detailed analysis to determine major drivers of churn.
            Your final output should include at least one detailed plot summarizing your findings."""
        },
        {"type": "container_upload", "file_id": file_metadata.id},
    ],
)

chat(
    messages,
    tools=[{"type": "code_execution_20250522", "name": "code_execution"}]
)
```

## Understanding the Response

When Claude uses code execution, the response contains multiple types of blocks:

- **Text blocks** - Claude's analysis and explanations
- **Server tool use blocks** - The actual code Claude decided to run
- **Code execution tool result blocks** - Output from running the code

![img](08_Code_execution_and_the_Files_API.assets/08_-_008_-_Code_Execution_and_the_Files_API_13.jpg)

Claude might execute code multiple times during a single response, iteratively building up its analysis. Each execution cycle includes the code and its results.

## Downloading Generated Files

One of the most powerful features is Claude's ability to generate files (like plots or reports) and make them available for download. When Claude creates a visualization, it gets stored in the container and you can download it using the Files API.

Look for blocks with `type: "code_execution_output"` in the response - these contain file IDs for generated content:

```
download_file("file_id_from_response")
```

![img](08_Code_execution_and_the_Files_API.assets/08_-_008_-_Code_Execution_and_the_Files_API_18.jpg)

The result is a comprehensive analysis with professional visualizations that would have taken significant manual coding to produce.

## Beyond Data Analysis

While data analysis is a natural fit, the combination of Files API and code execution opens up many possibilities:

- Image processing and manipulation
- Document parsing and transformation
- Mathematical computations and modeling
- Report generation with custom formatting

The key is that you can delegate complex, computational tasks to Claude while maintaining control over the inputs and outputs through the Files API. This creates a powerful workflow where Claude becomes your coding assistant that can actually execute and iterate on solutions.