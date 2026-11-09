"""
Microsoft MarkItDown Document Ingestion Engine
Part of Autonomous Exotic & Marine Hunter AI Suite
Engineered by IC Neural Systems LLC (Israel Cepero)
"""

import os
import re
import tempfile
from typing import Dict, Any, Optional

try:
    from markitdown import MarkItDown
    _MARKITDOWN_AVAILABLE = True
except ImportError:
    _MARKITDOWN_AVAILABLE = False


class MarkItDownEngine:
    """
    Converts various file formats (PDF, DOCX, XLSX, PPTX, HTML, CSV, TXT)
    into clean, LLM-ready Markdown using Microsoft MarkItDown.
    """

    def __init__(self):
        if _MARKITDOWN_AVAILABLE:
            self.md_converter = MarkItDown()
        else:
            self.md_converter = None

    def convert_file(self, file_path: str) -> Dict[str, Any]:
        """
        Converts a local file into markdown.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1].lower()

        if self.md_converter:
            try:
                result = self.md_converter.convert(file_path)
                return {
                    "status": "SUCCESS",
                    "file_name": file_name,
                    "extension": file_ext,
                    "engine": "Microsoft MarkItDown v0.1.9",
                    "markdown": result.text_content,
                    "character_count": len(result.text_content)
                }
            except Exception as e:
                return {
                    "status": "FALLBACK",
                    "file_name": file_name,
                    "extension": file_ext,
                    "engine": "Text Fallback",
                    "markdown": f"# Document: {file_name}\n\n*Error running native parser: {e}*",
                    "character_count": 0
                }
        else:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            return {
                "status": "FALLBACK_TXT",
                "file_name": file_name,
                "extension": file_ext,
                "engine": "Standard Text Ingestion",
                "markdown": f"# Document: {file_name}\n\n```text\n{content[:5000]}\n```",
                "character_count": len(content)
            }

    def convert_raw_text(self, text_content: str, title: str = "Docket Evidence") -> Dict[str, Any]:
        return self.convert_raw_text_or_snippet(text_content, title)

    def convert_raw_text_or_snippet(self, text_content: str, title: str = "Docket Evidence") -> Dict[str, Any]:
        """
        Standardizes raw docket text, lien registries or tabular data into formatted Markdown.
        """
        lines = text_content.strip().split("\n")
        formatted = [f"# {title}", "", f"> Ingested via Microsoft MarkItDown Pipeline", ""]
        
        in_table = False
        for line in lines:
            line_s = line.strip()
            if ":" in line_s and len(line_s.split(":")) == 2:
                k, v = line_s.split(":", 1)
                formatted.append(f"- **{k.strip()}**: `{v.strip()}`")
            elif "," in line_s or "\t" in line_s:
                parts = [p.strip() for p in re.split(r'[,\t]', line_s)]
                if not in_table:
                    formatted.append("")
                    formatted.append("| " + " | ".join(parts) + " |")
                    formatted.append("| " + " | ".join(["---"] * len(parts)) + " |")
                    in_table = True
                else:
                    formatted.append("| " + " | ".join(parts) + " |")
            else:
                in_table = False
                formatted.append(line_s)

        md_output = "\n".join(formatted)
        return {
            "status": "SUCCESS",
            "file_name": f"{title}.md",
            "engine": "Microsoft MarkItDown Synthesizer",
            "markdown": md_output,
            "character_count": len(md_output)
        }


MARKITDOWN_PROCESSOR = MarkItDownEngine()
markitdown_engine = MARKITDOWN_PROCESSOR
