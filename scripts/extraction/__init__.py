"""
Document extraction utilities.

Extractors:
- pdf_extraction_di: Azure Document Intelligence for PDF extraction
- excel_extraction_agents: Excel extraction with agent enhancement
- email_extraction_agents: Email (.msg) extraction with agent enhancement
"""
from .pdf_extraction_di import process_pdf_di_sync

# Backward compatibility alias
process_pdf_hybrid_sync = process_pdf_di_sync

from .excel_extraction_agents import process_excel_with_agents_sync
from .email_extraction_agents import process_email_with_agents_sync

__all__ = [
    'process_pdf_di_sync',
    'process_pdf_hybrid_sync',  # Backward compatibility
    'process_excel_with_agents_sync',
    'process_email_with_agents_sync',
]
