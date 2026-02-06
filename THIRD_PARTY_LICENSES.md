# Third-Party Licenses

This project (PrismRAG) is licensed under the MIT License. All third-party dependencies use permissive open-source licenses (MIT, BSD, Apache 2.0).

## Key Dependencies

| Package | License | Purpose |
|---------|---------|---------|
| azure-ai-documentintelligence | MIT | Azure Document Intelligence SDK for PDF extraction |
| python-oxmsg | MIT | Outlook .msg email parsing |
| openpyxl | MIT | Excel file extraction |
| agent-framework | MIT | Microsoft Agent Framework for extraction and workflow agents |
| langchain-text-splitters | MIT | Semantic chunking with markdown support |
| tiktoken | MIT | Token counting for chunking |
| azure-search-documents | MIT | Azure AI Search SDK |
| azure-ai-evaluation | MIT | Answer quality evaluation |
| azure-identity | MIT | Azure authentication (DefaultAzureCredential) |
| azure-storage-blob | MIT | Azure Blob Storage SDK |
| openai | Apache 2.0 | Azure OpenAI API client |
| python-dotenv | BSD-3-Clause | Environment variable loading |
| FastAPI | MIT | Backend API framework |
| Vue 3 | MIT | Frontend framework |

## Azure Services

The following Azure services are used at runtime (not bundled as dependencies):

| Service | Purpose |
|---------|---------|
| Azure Document Intelligence | PDF extraction via `prebuilt-layout` model |
| Azure OpenAI | GPT-4.1/GPT-5-chat for AI agents, text-embedding-3-large for embeddings |
| Azure AI Search | Hybrid search, semantic ranking, agentic retrieval |
| Azure Blob Storage | Document and project data storage |

Azure services are governed by [Microsoft Azure Terms of Service](https://azure.microsoft.com/support/legal/).

## License Compliance

All third-party packages in this project use permissive licenses that are compatible with the MIT License. No copyleft (GPL, AGPL) or commercial license dependencies exist.

## Disclaimer

This document is provided for informational purposes and does not constitute legal advice. Consult with a legal professional for specific licensing questions.
