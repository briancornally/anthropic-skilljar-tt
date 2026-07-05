from io import BytesIO
from pathlib import Path

from markitdown import MarkItDown, StreamInfo
from pydantic import Field

_SUPPORTED_EXTENSIONS = {"pdf", "docx"}


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    path: str = Field(description="Absolute or relative path to a .pdf or .docx file"),
) -> str:
    """Convert a PDF or DOCX file at the given path to markdown text.

    Reads the file from disk and converts its contents to markdown using
    MarkItDown. Headings, lists, tables, and inline formatting are preserved
    where the source format supports it.

    When to use:
    - Converting a local document file to markdown for further processing
    - Extracting structured text from PDF or DOCX files on disk

    When NOT to use:
    - When the file bytes are already in memory (use binary_document_to_markdown)
    - For file types other than .pdf or .docx

    Examples:
    >>> document_path_to_markdown("/path/to/report.pdf")
    "# Title\\n\\nIntroduction..."
    """
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if file_path.is_dir():
        raise ValueError(f"Path is a directory, not a file: {path}")

    ext = file_path.suffix.lower().lstrip(".")
    if ext not in _SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {file_path.suffix!r}. Expected .pdf or .docx"
        )

    with open(file_path, "rb") as f:
        data = f.read()

    return binary_document_to_markdown(data, ext)
