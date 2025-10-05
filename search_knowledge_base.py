"""
Search utility for querying the Azure AI Search index.
This script provides functions to search through the indexed markdown files.
"""

import os
from typing import List, Dict, Any, Optional
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery, QueryType, QueryCaptionType, QueryAnswerType
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI
from dotenv import load_dotenv

import config


class KnowledgeBaseSearcher:
    """Search client for querying the knowledge base index."""
    
    def __init__(self, index_name: str = "evaluation-knowledge-base-index"):
        """Initialize the search client.
        
        Args:
            index_name: Name of the search index (default: evaluation-knowledge-base-index)
        """
        search_endpoint = config.search_service_endpoint 
        credential = DefaultAzureCredential() 
        
        self.search_client = SearchClient(
            endpoint=search_endpoint,
            index_name=index_name,
            credential=credential
        )
        
        # Initialize OpenAI client for embeddings
        self.openai_client = AzureOpenAI(
            azure_endpoint=config.azure_openai_endpoint,
            azure_ad_token_provider=lambda: credential.get_token("https://cognitiveservices.azure.com/.default").token,
            api_version="2024-02-01"
        )
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for the given text using Azure OpenAI.
        
        Args:
            text: Text to generate embedding for
            
        Returns:
            List of floats representing the embedding vector
        """
        try:
            response = self.openai_client.embeddings.create(
                input=text,
                model="text-embedding-3-large"
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []
    
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

            results = self.search_client.search(
                search_text=query,
                top=top,
                filter=filters,
                order_by=order_by,
                select=["id", "title", "chunk", "file_name", "folder", "file_path", "last_modified"]
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
                    "chunk": result.get('chunk', '')[:500] + "..." if len(result.get('chunk', '')) > 500 else result.get('chunk', ''),
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
    
    def vector_search(
        self,
        query: str,
        top: int = 5,
        filters: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search using vector similarity (semantic search).
        
        Args:
            query: Search query string
            top: Number of results to return (default: 5)
            filters: OData filter expression
            
        Returns:
            List of search results ranked by semantic similarity
        """
        try:
            # Generate embedding for the query
            query_vector = self._generate_embedding(query)
            
            if not query_vector:
                print("Failed to generate query embedding")
                return []
            
            # Create vectorized query
            vector_query = VectorizedQuery(
                vector=query_vector,
                k_nearest_neighbors=top,
                fields="content_vector"
            )
            
            results = self.search_client.search(
                search_text=None,  # Pure vector search
                vector_queries=[vector_query],
                top=top,
                filter=filters,
                select=["id", "title", "chunk", "file_name", "folder", "file_path", "last_modified"]
            )
            
            search_results = []
            for result in results:
                search_result = {
                    "score": result.get('@search.score', 0),
                    "title": result.get('title', 'Untitled'),
                    "chunk": result.get('chunk', ''),
                    "file_name": result.get('file_name', ''),
                    "folder": result.get('folder', ''),
                    "file_path": result.get('file_path', ''),
                    "last_modified": result.get('last_modified', ''),
                    "search_type": "vector"
                }
                search_results.append(search_result)
            
            return search_results
            
        except Exception as e:
            print(f"Error during vector search: {e}")
            return []
    
    def hybrid_search(
        self,
        query: str,
        top: int = 5,
        filters: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search using hybrid approach (keyword + vector).
        
        Args:
            query: Search query string
            top: Number of results to return (default: 5)
            filters: OData filter expression
            
        Returns:
            List of search results combining keyword and semantic similarity
        """
        try:
            # Generate embedding for the query
            query_vector = self._generate_embedding(query)
            
            if not query_vector:
                print("Failed to generate query embedding, falling back to keyword search")
                return self.search(query, top, filters)
            
            # Create vectorized query
            vector_query = VectorizedQuery(
                vector=query_vector,
                k_nearest_neighbors=50,  # Get more candidates for reranking
                fields="content_vector"
            )
            
            results = self.search_client.search(
                search_text=query,  # Keyword search
                vector_queries=[vector_query],  # Vector search
                top=top,
                filter=filters,
                select=["id", "title", "chunk", "file_name", "folder", "file_path", "last_modified"]
            )
            
            search_results = []
            for result in results:
                search_result = {
                    "score": result.get('@search.score', 0),
                    "title": result.get('title', 'Untitled'),
                    "chunk": result.get('chunk', ''),
                    "file_name": result.get('file_name', ''),
                    "folder": result.get('folder', ''),
                    "file_path": result.get('file_path', ''),
                    "last_modified": result.get('last_modified', ''),
                    "search_type": "hybrid"
                }
                search_results.append(search_result)
            
            return search_results
            
        except Exception as e:
            print(f"Error during hybrid search: {e}")
            return []
    
    def semantic_search(
        self,
        query: str,
        top: int = 20,
        filters: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search using semantic ranking with captions and answers.
        
        Args:
            query: Search query string
            top: Number of results to return (default: 5)
            filters: OData filter expression
            
        Returns:
            List of search results with semantic ranking, captions, and answers
        """
        try:
            # Generate embedding for the query
            query_vector = self._generate_embedding(query)
            
            if not query_vector:
                print("Failed to generate query embedding, falling back to keyword search")
                return self.search(query, top, filters)
            
            # Create vectorized query
            vector_query = VectorizedQuery(
                vector=query_vector,
                k_nearest_neighbors=50,
                fields="content_vector"
            )
            
            results = self.search_client.search(
                search_text=query,
                vector_queries=[vector_query],
                query_type=QueryType.SEMANTIC,
                semantic_configuration_name="default",
                query_caption=QueryCaptionType.NONE,
                query_answer=QueryAnswerType.NONE,
                top=top,
                filter=filters,
                select=["id", "title", "chunk", "file_name", "folder", "file_path", "last_modified"]
            )
            
            search_results = []
            
            # Extract semantic answers if available
            answers = []
            if hasattr(results, 'get_answers'):
                answers = results.get_answers() or []
            
            for result in results:
                # Extract captions
                captions = []
                if hasattr(result, '@search.captions'):
                    captions = result.get('@search.captions', [])
                
                search_result = {
                    "score": result.get('@search.score', 0),
                    "reranker_score": result.get('@search.reranker_score', 0),
                    "title": result.get('title', 'Untitled'),
                    "chunk": result.get('chunk', ''),
                    "file_name": result.get('file_name', ''),
                    "folder": result.get('folder', ''),
                    "file_path": result.get('file_path', ''),
                    "last_modified": result.get('last_modified', ''),
                    "captions": [caption.text for caption in captions] if captions else [],
                    "search_type": "semantic"
                }
                search_results.append(search_result)
            
            # Add answers to the first result if available
            if answers and search_results:
                search_results[0]["answers"] = [answer.text for answer in answers]
            
            return search_results
            
        except Exception as e:
            print(f"Error during semantic search: {e}")
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
    
    def get_facets(self, facet_fields: Optional[List[str]] = None) -> Dict[str, Any]:
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
                facets = results.get_facets() or {}
            
            return facets
            
        except Exception as e:
            print(f"Error getting facets: {e}")
            return {}


def load_search_config() -> Dict[str, str]:
    """Load search configuration from environment variables."""
    load_dotenv()
    
    # Using DefaultAzureCredential, so no need for API keys
    # Just ensure the basic config is loaded
    return {}


def interactive_search():
    """Interactive search interface."""
    try:
        # Load configuration
        load_search_config()
        
        # Initialize searcher
        searcher = KnowledgeBaseSearcher()
        
        print("Knowledge Base Search Interface")
        print("=" * 40)
        print("Available commands:")
        print("  search <query>     - Keyword search for documents")
        print("  vector <query>     - Vector/semantic similarity search")
        print("  hybrid <query>     - Hybrid search (keyword + vector)")
        print("  semantic <query>   - Semantic search with ranking and captions")
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
                    print(f"\nKeyword searching for: '{query}'")
                    results = searcher.search(query, top=5)
                    
                    if not results:
                        print("No results found.")
                    else:
                        for i, result in enumerate(results, 1):
                            print(f"\n{i}. {result['title']} (Score: {result['score']:.2f})")
                            print(f"   File: {result['file_name']} | Folder: {result['folder']}")
                            print(f"   Content: {result['chunk']}")
                            if result.get('highlights'):
                                print(f"   Highlights: {result['highlights']}")
                
                elif command == 'vector':
                    if len(parts) < 2:
                        print("Usage: vector <query>")
                        continue
                    
                    query = parts[1]
                    print(f"\nVector searching for: '{query}'")
                    results = searcher.vector_search(query, top=5)
                    
                    if not results:
                        print("No results found.")
                    else:
                        for i, result in enumerate(results, 1):
                            print(f"\n{i}. {result['title']} (Similarity: {result['score']:.4f})")
                            print(f"   File: {result['file_name']} | Folder: {result['folder']}")
                            print(f"   Content: {result['chunk']}")
                
                elif command == 'hybrid':
                    if len(parts) < 2:
                        print("Usage: hybrid <query>")
                        continue
                    
                    query = parts[1]
                    print(f"\nHybrid searching for: '{query}'")
                    results = searcher.hybrid_search(query, top=5)
                    
                    if not results:
                        print("No results found.")
                    else:
                        for i, result in enumerate(results, 1):
                            print(f"\n{i}. {result['title']} (Score: {result['score']:.4f})")
                            print(f"   File: {result['file_name']} | Folder: {result['folder']}")
                            print(f"   Content: {result['chunk']}")
                
                elif command == 'semantic':
                    if len(parts) < 2:
                        print("Usage: semantic <query>")
                        continue
                    
                    query = parts[1]
                    print(f"\nSemantic searching for: '{query}'")
                    results = searcher.semantic_search(query, top=5)
                    
                    if not results:
                        print("No results found.")
                    else:
                        # Display answers first if available
                        if results and 'answers' in results[0]:
                            print("\n📋 ANSWERS:")
                            for answer in results[0]['answers']:
                                print(f"   {answer}")
                            print()
                        
                        for i, result in enumerate(results, 1):
                            reranker_score = result.get('reranker_score', 0)
                            score_text = f"Score: {result['score']:.4f}"
                            if reranker_score > 0:
                                score_text += f", Reranker: {reranker_score:.4f}"
                            
                            print(f"\n{i}. {result['title']} ({score_text})")
                            print(f"   File: {result['file_name']} | Folder: {result['folder']}")
                            
                            # Show captions if available
                            if result.get('captions'):
                                print(f"   📝 Captions: {'; '.join(result['captions'])}")
                            else:
                                print(f"   Content: {result['chunk']}")
                
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


def demo_search_capabilities():
    """Demo function to showcase different search capabilities."""
    try:
        searcher = KnowledgeBaseSearcher()
        
        # Example queries to demonstrate different search types
        demo_queries = [
            "What is Meridian's mission statement?",
            "AI consulting expertise and capabilities",
            "project methodology and phases",
            "team structure for digital transformation"
        ]
        
        print("🔍 SEARCH CAPABILITIES DEMO")
        print("=" * 50)
        
        for query in demo_queries:
            print(f"\n📝 Query: '{query}'")
            print("-" * 40)
            
            # Keyword Search
            print("🔤 Keyword Search:")
            keyword_results = searcher.search(query, top=2)
            for i, result in enumerate(keyword_results[:1], 1):
                print(f"  {i}. {result['title']} (Score: {result['score']:.3f})")
                print(f"     {result['chunk'][:100]}...")
            
            # Vector Search
            print("\n🧠 Vector Search:")
            vector_results = searcher.vector_search(query, top=2)
            for i, result in enumerate(vector_results[:1], 1):
                print(f"  {i}. {result['title']} (Score: {result['score']:.3f})")
                print(f"     {result['chunk'][:100]}...")
            
            # Semantic Search
            print("\n🎯 Semantic Search:")
            semantic_results = searcher.semantic_search(query, top=2)
            for i, result in enumerate(semantic_results[:1], 1):
                reranker = result.get('reranker_score', 0)
                score_info = f"Score: {result['score']:.3f}"
                if reranker > 0:
                    score_info += f", Reranker: {reranker:.3f}"
                print(f"  {i}. {result['title']} ({score_info})")
                if result.get('captions'):
                    print(f"     Caption: {result['captions'][0][:100]}...")
                else:
                    print(f"     {result['chunk'][:100]}...")
            
            print("\n" + "="*50)
    
    except Exception as e:
        print(f"Demo error: {e}")


def main():
    """Main function for the search utility."""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_search_capabilities()
    else:
        interactive_search()


if __name__ == "__main__":
    main()