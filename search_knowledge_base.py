"""
Search utility for querying the Azure AI Search index.
This script provides functions to search through the indexed markdown files.
"""

import os
from typing import List, Dict, Any, Optional
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv


class KnowledgeBaseSearcher:
    """Search client for querying the knowledge base index."""
    
    def __init__(self, search_service_name: str, search_admin_key: str, index_name: str = "knowledge-base-index"):
        """Initialize the search client.
        
        Args:
            search_service_name: Name of the Azure Search service
            search_admin_key: Admin key for Azure Search service
            index_name: Name of the search index (default: knowledge-base-index)
        """
        search_endpoint = f"https://{search_service_name}.search.windows.net"
        credential = AzureKeyCredential(search_admin_key)
        
        self.search_client = SearchClient(
            endpoint=search_endpoint,
            index_name=index_name,
            credential=credential
        )
    
    def search(
        self,
        query: str,
        top: int = 5,
        filters: Optional[str] = None,
        order_by: Optional[List[str]] = None,
        highlight_fields: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Search the knowledge base.
        
        Args:
            query: Search query string
            top: Number of results to return (default: 5)
            filters: OData filter expression
            order_by: List of fields to order by
            highlight_fields: List of fields to highlight in results
            
        Returns:
            List of search results
        """
        try:
            # Set default highlight fields
            if highlight_fields is None:
                highlight_fields = ["content", "title"]
            
            results = self.search_client.search(
                search_text=query,
                top=top,
                filter=filters,
                order_by=order_by,
                highlight_fields=highlight_fields,
                select=["id", "title", "content", "file_name", "folder", "file_path", "last_modified"]
            )
            
            search_results = []
            for result in results:
                # Extract highlights if available
                highlights = {}
                if hasattr(result, '@search.highlights'):
                    highlights = result.get('@search.highlights', {})
                
                search_result = {
                    "score": result.get('@search.score', 0),
                    "title": result.get('title', 'Untitled'),
                    "content": result.get('content', '')[:500] + "..." if len(result.get('content', '')) > 500 else result.get('content', ''),
                    "file_name": result.get('file_name', ''),
                    "folder": result.get('folder', ''),
                    "file_path": result.get('file_path', ''),
                    "last_modified": result.get('last_modified', ''),
                    "highlights": highlights
                }
                search_results.append(search_result)
            
            return search_results
            
        except Exception as e:
            print(f"Error during search: {e}")
            return []
    
    def search_by_folder(self, query: str, folder: str, top: int = 5) -> List[Dict[str, Any]]:
        """Search within a specific folder.
        
        Args:
            query: Search query string
            folder: Folder name to search within
            top: Number of results to return
            
        Returns:
            List of search results from the specified folder
        """
        filter_expression = f"folder eq '{folder}'"
        return self.search(query=query, top=top, filters=filter_expression)
    
    def get_document_by_filename(self, filename: str) -> Optional[Dict[str, Any]]:
        """Get a specific document by filename.
        
        Args:
            filename: Name of the file to retrieve
            
        Returns:
            Document data if found, None otherwise
        """
        filter_expression = f"file_name eq '{filename}'"
        results = self.search(query="*", top=1, filters=filter_expression)
        return results[0] if results else None
    
    def list_all_documents(self, top: int = 100) -> List[Dict[str, Any]]:
        """List all documents in the index.
        
        Args:
            top: Maximum number of documents to return
            
        Returns:
            List of all documents
        """
        return self.search(query="*", top=top, order_by=["last_modified desc"])
    
    def get_facets(self, facet_fields: List[str] = None) -> Dict[str, Any]:
        """Get facet counts for specified fields.
        
        Args:
            facet_fields: List of fields to get facets for
            
        Returns:
            Dictionary of facet counts
        """
        if facet_fields is None:
            facet_fields = ["folder"]
        
        try:
            results = self.search_client.search(
                search_text="*",
                facets=facet_fields,
                top=0  # We only want facets, not results
            )
            
            # Extract facets from results
            facets = {}
            if hasattr(results, 'get_facets'):
                facets = results.get_facets()
            
            return facets
            
        except Exception as e:
            print(f"Error getting facets: {e}")
            return {}


def load_search_config() -> Dict[str, str]:
    """Load search configuration from environment variables."""
    load_dotenv()
    
    required_vars = [
        "AZURE_SEARCH_SERVICE_NAME",
        "AZURE_SEARCH_ADMIN_KEY"
    ]
    
    config = {}
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        config[var] = value
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return config


def interactive_search():
    """Interactive search interface."""
    try:
        # Load configuration
        config = load_search_config()
        
        # Initialize searcher
        searcher = KnowledgeBaseSearcher(
            search_service_name=config["AZURE_SEARCH_SERVICE_NAME"],
            search_admin_key=config["AZURE_SEARCH_ADMIN_KEY"]
        )
        
        print("Knowledge Base Search Interface")
        print("=" * 40)
        print("Available commands:")
        print("  search <query>     - Search for documents")
        print("  folder <folder>    - List documents in a folder")
        print("  list              - List all documents")
        print("  facets            - Show folder facets")
        print("  quit              - Exit")
        print()
        
        while True:
            try:
                user_input = input("Search> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                parts = user_input.split(' ', 1)
                command = parts[0].lower()
                
                if command == 'search':
                    if len(parts) < 2:
                        print("Usage: search <query>")
                        continue
                    
                    query = parts[1]
                    print(f"\nSearching for: '{query}'")
                    results = searcher.search(query, top=5)
                    
                    if not results:
                        print("No results found.")
                    else:
                        for i, result in enumerate(results, 1):
                            print(f"\n{i}. {result['title']} (Score: {result['score']:.2f})")
                            print(f"   File: {result['file_name']} | Folder: {result['folder']}")
                            print(f"   Content: {result['content']}")
                            if result['highlights']:
                                print(f"   Highlights: {result['highlights']}")
                
                elif command == 'folder':
                    if len(parts) < 2:
                        print("Usage: folder <folder_name>")
                        continue
                    
                    folder = parts[1]
                    results = searcher.search_by_folder("*", folder, top=10)
                    
                    if not results:
                        print(f"No documents found in folder: {folder}")
                    else:
                        print(f"\nDocuments in folder '{folder}':")
                        for i, result in enumerate(results, 1):
                            print(f"{i}. {result['file_name']} - {result['title']}")
                
                elif command == 'list':
                    print("\nAll documents:")
                    results = searcher.list_all_documents(top=20)
                    
                    for i, result in enumerate(results, 1):
                        print(f"{i}. {result['file_name']} ({result['folder']}) - {result['title']}")
                
                elif command == 'facets':
                    print("\nFolder facets:")
                    facets = searcher.get_facets(['folder'])
                    
                    if 'folder' in facets:
                        for facet in facets['folder']:
                            print(f"  {facet['value']}: {facet['count']} documents")
                    else:
                        print("No facets available.")
                
                else:
                    print(f"Unknown command: {command}")
                    print("Type 'quit' to exit or use one of the available commands.")
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    except Exception as e:
        print(f"Error initializing search: {e}")
        print("Please ensure your Azure AI Search service is set up and .env file is configured.")


def main():
    """Main function for the search utility."""
    interactive_search()


if __name__ == "__main__":
    main()