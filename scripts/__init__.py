"""
Prism - Scripts Package

This package contains all the processing scripts for document extraction,
RAG pipeline operations, and Azure AI Search integration.

Structure:
    extraction/                 # Core document extraction
        - pdf_extraction_di: Azure Document Intelligence PDF extraction
        - excel_extraction_agents: Excel processing with agent enhancement
        - email_extraction_agents: Email processing with agent enhancement
        - extract_msg_files: python-oxmsg helper functions for .msg file extraction
        - plugins/              # Domain-specific extractors (optional)
            - sld_extractor: Specialized SLD (Single-Line Diagram) extraction

    testing/                    # Testing and batch processing
        - process_all_documents: Batch processing of all documents
        - test_single_document: Single document testing interface

    rag/                        # RAG pipeline
        - deduplicate_documents: Document deduplication analysis
        - chunk_documents: Semantic chunking for RAG
        - generate_embeddings: Embedding generation

    search_index/               # Azure AI Search setup
        - create_search_index: Azure AI Search index creation
        - upload_to_search: Batch upload to search index
        - create_knowledge_source: Knowledge source wrapper
        - create_knowledge_agent: Knowledge agent creation

    query/                      # Query interface
        - query_knowledge_agent: Interactive query interface
"""

__version__ = "1.0.0"
