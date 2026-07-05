import io
import shutil
import zipfile
from pathlib import Path

import pytest

from tools.document import document_path_to_markdown

FIXTURES_DIR = Path(__file__).parent / "fixtures"
DOCX_FIXTURE = FIXTURES_DIR / "mcp_docs.docx"
PDF_FIXTURE = FIXTURES_DIR / "mcp_docs.pdf"


def _make_minimal_docx(text: str) -> bytes:
    """Build the smallest valid DOCX (ZIP + OOXML) containing the given text."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml"'
            ' ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            "</Types>",
        )
        zf.writestr(
            "_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1"'
            ' Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"'
            ' Target="word/document.xml"/>'
            "</Relationships>",
        )
        zf.writestr(
            "word/_rels/document.xml.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            "</Relationships>",
        )
        zf.writestr(
            "word/document.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            f"<w:body><w:p><w:r><w:t>{text}</w:t></w:r></w:p><w:sectPr/></w:body>"
            "</w:document>",
        )
    return buf.getvalue()


class TestHappyPath:
    def test_basic_docx_returns_nonempty_string(self):
        result = document_path_to_markdown(str(DOCX_FIXTURE))
        assert isinstance(result, str)
        assert len(result) > 0

    def test_basic_pdf_returns_nonempty_string(self):
        result = document_path_to_markdown(str(PDF_FIXTURE))
        assert isinstance(result, str)
        assert len(result) > 0

    def test_return_type_is_str(self):
        assert type(document_path_to_markdown(str(DOCX_FIXTURE))) is str

    def test_absolute_path_works(self):
        assert DOCX_FIXTURE.is_absolute()
        result = document_path_to_markdown(str(DOCX_FIXTURE))
        assert len(result) > 0


class TestContentFidelity:
    def test_docx_headings_preserved(self):
        result = document_path_to_markdown(str(DOCX_FIXTURE))
        assert "#" in result

    def test_docx_bullet_list_preserved(self):
        result = document_path_to_markdown(str(DOCX_FIXTURE))
        assert "*" in result or "-" in result

    def test_docx_table_preserved(self):
        result = document_path_to_markdown(str(DOCX_FIXTURE))
        assert "|" in result

    def test_pdf_has_substantial_text(self):
        result = document_path_to_markdown(str(PDF_FIXTURE))
        assert len(result) > 100

    def test_unicode_characters_preserved(self, tmp_path):
        unicode_text = "Héllo Wörld 日本語"
        docx_bytes = _make_minimal_docx(unicode_text)
        docx_file = tmp_path / "unicode.docx"
        docx_file.write_bytes(docx_bytes)
        result = document_path_to_markdown(str(docx_file))
        assert "Héllo" in result or "Wörld" in result or "日本語" in result


class TestPathHandling:
    def test_path_with_spaces(self, tmp_path):
        spaced_dir = tmp_path / "my documents"
        spaced_dir.mkdir()
        dest = spaced_dir / "mcp docs.docx"
        shutil.copy(DOCX_FIXTURE, dest)
        result = document_path_to_markdown(str(dest))
        assert len(result) > 0

    def test_uppercase_pdf_extension(self, tmp_path):
        dest = tmp_path / "file.PDF"
        shutil.copy(PDF_FIXTURE, dest)
        result = document_path_to_markdown(str(dest))
        assert len(result) > 0

    def test_uppercase_docx_extension(self, tmp_path):
        dest = tmp_path / "file.DOCX"
        shutil.copy(DOCX_FIXTURE, dest)
        result = document_path_to_markdown(str(dest))
        assert len(result) > 0

    def test_mixed_case_extension(self, tmp_path):
        dest = tmp_path / "file.Docx"
        shutil.copy(DOCX_FIXTURE, dest)
        result = document_path_to_markdown(str(dest))
        assert len(result) > 0


class TestErrorHandling:
    def test_file_not_found_raises_file_not_found_error(self, tmp_path):
        missing = tmp_path / "nonexistent.pdf"
        with pytest.raises(FileNotFoundError):
            document_path_to_markdown(str(missing))

    def test_file_not_found_message_contains_path(self, tmp_path):
        missing = tmp_path / "nonexistent.pdf"
        with pytest.raises(FileNotFoundError, match="nonexistent.pdf"):
            document_path_to_markdown(str(missing))

    def test_directory_path_raises_value_error(self, tmp_path):
        with pytest.raises(ValueError):
            document_path_to_markdown(str(tmp_path))

    def test_unsupported_extension_txt_raises_value_error(self, tmp_path):
        f = tmp_path / "file.txt"
        f.write_text("hello")
        with pytest.raises(ValueError):
            document_path_to_markdown(str(f))

    def test_unsupported_extension_png_raises_value_error(self, tmp_path):
        f = tmp_path / "image.png"
        f.write_bytes(b"\x89PNG\r\n\x1a\n")
        with pytest.raises(ValueError):
            document_path_to_markdown(str(f))

    def test_unsupported_extension_xlsx_raises_value_error(self, tmp_path):
        f = tmp_path / "sheet.xlsx"
        f.write_bytes(b"PK\x03\x04")
        with pytest.raises(ValueError):
            document_path_to_markdown(str(f))

    def test_unsupported_extension_error_message_names_extension(self, tmp_path):
        f = tmp_path / "file.txt"
        f.write_text("hello")
        with pytest.raises(ValueError, match=r"\.txt"):
            document_path_to_markdown(str(f))

    def test_corrupted_pdf_returns_string(self, tmp_path):
        # markitdown is resilient: falls back to treating content as plain text
        bad = tmp_path / "bad.pdf"
        bad.write_bytes(b"this is not a valid pdf file at all")
        result = document_path_to_markdown(str(bad))
        assert isinstance(result, str)

    def test_corrupted_docx_returns_string(self, tmp_path):
        # markitdown is resilient: falls back to treating content as plain text
        bad = tmp_path / "bad.docx"
        bad.write_bytes(b"this is not a valid docx zip file at all")
        result = document_path_to_markdown(str(bad))
        assert isinstance(result, str)
