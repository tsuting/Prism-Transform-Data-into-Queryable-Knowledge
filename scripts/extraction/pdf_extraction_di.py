"""
PDF Extraction using Azure Document Intelligence.

Uses the prebuilt-layout model for comprehensive document extraction:
- Text with paragraph roles (title, sectionHeading, footnote, etc.)
- Tables as HTML (supports merged cells, rowspan/colspan)
- Figures with captions and bounding boxes
- Selection marks as Unicode (☒/☐)
- Formulas in LaTeX format
- Page structure (headers, footers, page numbers)

Output: Native DI markdown format with <!-- PageBreak --> markers.
"""

import os
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import (
    AnalyzeResult,
    DocumentContentFormat,
)

from scripts.logging_config import get_logger
from scripts.azure_credential_helper import get_credential

# Import progress reporting
try:
    from apps.api.app.services.progress_tracker import report_page_progress
except ImportError:
    def report_page_progress(page_num: int, total_pages: int, message: str = "") -> None:
        pass

# Load environment
load_dotenv()

# Logger
logger = get_logger(__name__)

# Configuration
AZURE_DI_ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")

# Client cache
_client_cache: Dict[str, DocumentIntelligenceClient] = {}


def get_client() -> DocumentIntelligenceClient:
    """
    Get or create Document Intelligence client with DefaultAzureCredential.
    """
    if '_client' not in _client_cache:
        if not AZURE_DI_ENDPOINT:
            raise ValueError(
                "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT environment variable is not set. "
                "Document Intelligence is required for PDF extraction. "
                "For Azure deployment: run 'azd up' to provision the resource. "
                "For local development: set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT in your .env file."
            )

        logger.debug("Initializing Document Intelligence client")
        credential = get_credential()
        _client_cache['_client'] = DocumentIntelligenceClient(
            endpoint=AZURE_DI_ENDPOINT,
            credential=credential
        )
    return _client_cache['_client']


@dataclass
class PageInfo:
    """Information about a page in the document."""
    page_number: int
    start_offset: int
    length: int
    has_tables: bool
    has_figures: bool
    has_formulas: bool


def extract_page_info(result: AnalyzeResult) -> list[PageInfo]:
    """
    Extract page information from DI result.

    Args:
        result: AnalyzeResult from Document Intelligence

    Returns:
        List of PageInfo objects
    """
    pages = []
    content = result.content or ""

    # Find page breaks
    page_breaks = []
    marker = "<!-- PageBreak -->"
    pos = 0
    while True:
        idx = content.find(marker, pos)
        if idx == -1:
            break
        page_breaks.append(idx)
        pos = idx + len(marker)

    # Build page info
    page_starts = [0] + [pb + len(marker) for pb in page_breaks]
    page_ends = page_breaks + [len(content)]

    for i, (start, end) in enumerate(zip(page_starts, page_ends), 1):
        page_content = content[start:end]
        pages.append(PageInfo(
            page_number=i,
            start_offset=start,
            length=end - start,
            has_tables="<table" in page_content.lower(),
            has_figures="<figure" in page_content.lower(),
            has_formulas="$" in page_content
        ))

    # If no page breaks found, treat as single page
    if not pages:
        pages.append(PageInfo(
            page_number=1,
            start_offset=0,
            length=len(content),
            has_tables="<table" in content.lower(),
            has_figures="<figure" in content.lower(),
            has_formulas="$" in content
        ))

    return pages


def analyze_document(pdf_path: Path) -> AnalyzeResult:
    """
    Analyze a PDF document using Document Intelligence.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        AnalyzeResult from Document Intelligence
    """
    client = get_client()

    logger.info(f"Analyzing {pdf_path.name} with Document Intelligence")

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    # Analyze with prebuilt-layout model, markdown output
    poller = client.begin_analyze_document(
        "prebuilt-layout",
        body=pdf_bytes,
        output_content_format=DocumentContentFormat.MARKDOWN,
        content_type="application/pdf"
    )

    result = poller.result()

    return result


def process_pdf_di(
    pdf_path: Path,
    project_instructions: Optional[str] = None
) -> Dict:
    """
    Process PDF using Azure Document Intelligence.

    Args:
        pdf_path: Path to the PDF file
        project_instructions: Optional project-specific instructions (currently unused,
                            DI doesn't support custom instructions during extraction)

    Returns:
        Dict compatible with pipeline format
    """
    try:
        # Analyze document
        result = analyze_document(pdf_path)

        # Get markdown content (native DI format)
        markdown = result.content or ""

        # Extract page information
        pages = extract_page_info(result)
        page_count = len(pages)

        # Report progress
        for page in pages:
            report_page_progress(page.page_number, page_count, "Extracted")

        # Count features
        tables_count = len(result.tables) if result.tables else 0
        figures_count = len(result.figures) if result.figures else 0

        # Build result structure
        output = {
            "status": "Succeeded",
            "method": "azure_document_intelligence",
            "result": {
                "contents": [{
                    "markdown": markdown
                }],
                "pages": [{"pageNumber": p.page_number} for p in pages],
                "page_boundaries": [
                    {
                        "page": p.page_number,
                        "start_offset": p.start_offset,
                        "length": p.length
                    }
                    for p in pages
                ],
                "processing_summary": {
                    "total_pages": page_count,
                    "tables_detected": tables_count,
                    "figures_detected": figures_count,
                    "method": "prebuilt-layout",
                    "output_format": "markdown"
                }
            }
        }

        # Include structured data if available
        if result.tables:
            output["result"]["tables"] = [
                {
                    "row_count": t.row_count,
                    "column_count": t.column_count,
                    "caption": t.caption.content if t.caption else None
                }
                for t in result.tables
            ]

        if result.figures:
            output["result"]["figures"] = [
                {
                    "id": f.id,
                    "caption": f.caption.content if f.caption else None,
                    "page": f.bounding_regions[0].page_number if f.bounding_regions else None
                }
                for f in result.figures
            ]

        logger.info(
            f"Extraction complete: {len(markdown):,} chars | "
            f"Pages: {page_count} | Tables: {tables_count} | Figures: {figures_count}"
        )

        return output

    except Exception as e:
        logger.error(f"Document Intelligence extraction failed: {e}", exc_info=True)
        return None


def process_pdf_di_sync(
    pdf_path: Path,
    project_instructions: Optional[str] = None
) -> Dict:
    """Synchronous wrapper for DI processing."""
    return process_pdf_di(pdf_path, project_instructions)
