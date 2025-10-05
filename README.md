# Evaluation Intro - Azure AI Search for Knowledge Base

This project sets up an Azure AI Search index with an indexer to process markdown files from an Azure Storage account's knowledge-base folder.

## Features

- 🔍 **Azure AI Search Integration**: Automatically index markdown files from Azure Storage
- 📁 **Knowledge Base Processing**: Specifically targets markdown files in the `knowledge-base` folder
- 🔄 **Automated Indexing**: Configurable indexer that runs on a schedule
- 🔎 **Search Interface**: Interactive search utility to query indexed content
- 📊 **Rich Metadata**: Extracts file metadata, content, and supports faceted search

## Setup

### Prerequisites

- Azure AI Search service
- Azure Storage account with a container containing your markdown files
- Python 3.12+

### Installation

1. Install dependencies:
```bash
pip install -e .
```

2. Copy the environment template and configure your Azure credentials:
```bash
cp .env.template .env
```

3. Edit `.env` with your Azure service details:
```env
AZURE_SEARCH_SERVICE_NAME=your-search-service-name
AZURE_SEARCH_ADMIN_KEY=your-search-admin-key
AZURE_STORAGE_ACCOUNT_NAME=your-storage-account-name
AZURE_STORAGE_ACCOUNT_KEY=your-storage-account-key
AZURE_STORAGE_CONTAINER_NAME=knowledge-base
```

### Azure Storage Setup

Ensure your Azure Storage account has a container with the following structure:
```
knowledge-base/
├── core-business/
│   ├── case-studies.md
│   ├── company-overview.md
│   ├── industry-expertise.md
│   └── service-offerings.md
└── methodologies/
    └── meridian-strategic-methodology.md
```

## Usage

### Setting up the Azure AI Search Index

Run the main script to create the index, data source, and indexer:

```bash
python main.py
```

This will:
1. Create a search index optimized for markdown content
2. Set up a data source connection to your Azure Storage
3. Create an indexer that processes markdown files
4. Start the initial indexing process

### Searching the Knowledge Base

Use the interactive search utility:

```bash
python search_knowledge_base.py
```

Available search commands:
- `search <query>` - Search for documents containing the query
- `folder <folder>` - List documents in a specific folder
- `list` - List all indexed documents
- `facets` - Show folder facets and document counts
- `quit` - Exit the search interface

### Programmatic Usage

You can also use the classes directly in your Python code:

```python
from azure_search_setup import AzureSearchIndexManager
from search_knowledge_base import KnowledgeBaseSearcher

# Setup
manager = AzureSearchIndexManager(
    search_service_name="your-service",
    search_admin_key="your-key",
    storage_account_name="your-storage",
    storage_account_key="your-storage-key"
)
manager.setup_complete_search_solution()

# Search
searcher = KnowledgeBaseSearcher("your-service", "your-key")
results = searcher.search("company overview")
```

## Index Schema

The search index includes these fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | String | Unique document identifier (key) |
| `content` | String | Full text content of the markdown file |
| `title` | String | Document title (extracted from content) |
| `file_path` | String | Full path to the file in storage |
| `file_name` | String | Name of the file |
| `folder` | String | Folder containing the file |
| `last_modified` | DateTime | When the file was last modified |
| `size` | Int64 | File size in bytes |
| `metadata_storage_*` | Various | Additional storage metadata |

## Indexer Configuration

The indexer is configured to:
- Process only markdown files (`.md`, `.markdown`)
- Run on a daily schedule
- Extract text content and metadata
- Handle file updates and deletions
- Focus on the `knowledge-base` folder in your storage container

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Verify your Azure credentials in the `.env` file
2. **Storage Access**: Ensure the storage account key has read permissions
3. **Search Service**: Confirm the search service name and admin key are correct
4. **Container Not Found**: Check that the storage container exists and contains markdown files

### Checking Indexer Status

You can check the indexer status programmatically:

```python
manager = AzureSearchIndexManager(...)
status = manager.get_indexer_status()
print(f"Status: {status.status}")
print(f"Last run: {status.last_result.start_time}")
```

## Development

### Project Structure

```
├── azure_search_setup.py      # Main Azure AI Search setup
├── search_knowledge_base.py   # Search utility
├── main.py                    # Entry point
├── .env.template              # Environment variables template
└── knowledge-base/            # Local markdown files (for reference)
```

### Adding New Features

The codebase is designed to be extensible. You can:
- Add new fields to the index schema
- Implement custom text processing
- Add new search capabilities
- Integrate with other Azure Cognitive Services

## License

This project is provided as-is for educational and demonstration purposes.