"""
Azure AI Search index and indexer setup for processing markdown files.
This script creates an Azure AI Search index with an indexer that processes
markdown files from an Azure Storage account's knowledge-base folder.
"""

import os
from typing import Optional
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    ComplexField,
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    SemanticSearch,
    SearchIndexer,
    SearchIndexerDataContainer,
    SearchIndexerDataSourceConnection,
    IndexingSchedule,
    SearchIndexerSkillset,
    SearchIndexerStatus,
    VectorSearch,
    VectorSearchProfile,
    HnswAlgorithmConfiguration,
    AzureOpenAIVectorizer,
    AzureOpenAIVectorizerParameters,
    SplitSkill,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    AzureOpenAIEmbeddingSkill,
    SearchIndexerIndexProjection,
    HighWaterMarkChangeDetectionPolicy,
    IndexingParameters,
    IndexingParametersConfiguration,
    SearchIndexerIndexProjectionSelector,
    SearchIndexerIndexProjectionsParameters,
    IndexProjectionMode,
    ConditionalSkill
)
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import config


class AzureSearchIndexManager:
    """Manages Azure AI Search index and indexer for markdown files."""
    
    def __init__(
        self,
        search_service_endpoint: str,
        storage_container_name: str = "evaluation-knowledge-base"
    ):
        """Initialize the Azure Search Index Manager.
        
        Args:
            search_service_name: Name of the Azure Search service
            storage_account_name: Name of the Azure Storage account
            storage_account_key: Access key for Azure Storage account
            storage_container_name: Name of the storage container (default: evaluation-knowledge-base)
        """
        self.search_service_endpoint = search_service_endpoint
        self.storage_container_name = storage_container_name
        
        # Initialize Azure Search clients
        credential = DefaultAzureCredential() 
        
        self.search_index_client = SearchIndexClient(
            endpoint=self.search_service_endpoint,
            credential=credential
        )
        self.search_indexer_client = SearchIndexerClient(
            endpoint=self.search_service_endpoint,
            credential=credential
        )
        
        # Initialize Azure Storage client
        self.storage_connection_string = (
            f"DefaultEndpointsProtocol=https;"
            f"AccountName={config.storage_account_name};"
            f"EndpointSuffix=core.windows.net"
        )
        
        # Define names for Azure Search resources
        self.index_name = "evaluation-knowledge-base-index"
        self.data_source_name = "evaluation-knowledge-base-datasource"
        self.indexer_name = "evaluation-knowledge-base-indexer"

    def create_skillset(self) -> None:
        split_skill = SplitSkill(  
            description="Split skill to chunk documents",
            text_split_mode="pages",
            context="/document",
            maximum_page_length=2000,
            page_overlap_length=500,
            inputs=[
                InputFieldMappingEntry(name="text", source="/document/content"),
            ],
            outputs=[  
                OutputFieldMappingEntry(name="textItems", target_name="pages")  
            ]
        )

        embedding_skill = AzureOpenAIEmbeddingSkill(  
            description="Skill to generate embeddings via Azure OpenAI",  
            context="/document/pages/*",  
            resource_url=config.azure_openai_endpoint,
            deployment_name="text-embedding-3-large",
            model_name="text-embedding-3-large",
            dimensions=3072,
            auth_identity=config.search_service_identity,
            inputs=[  
                InputFieldMappingEntry(name="text", source="/document/pages/*"),  
            ],  
            outputs=[
                OutputFieldMappingEntry(name="embedding", target_name="content_vector")  
            ]
        )

        skillset =  SearchIndexerSkillset(  
            name="markdown-skillset",  
            description="Skillset to chunk documents and generating embeddings",  
            skills=[split_skill, embedding_skill],  
            index_projection=SearchIndexerIndexProjection(  
                selectors=[  
                SearchIndexerIndexProjectionSelector(  
                    target_index_name=self.index_name,
                    parent_key_field_name="parent_id",  
                    source_context="/document/pages/*",  
                    mappings=[
                        InputFieldMappingEntry(name="title", source="/document/metadata_storage_name"),
                        InputFieldMappingEntry(name="chunk", source="/document/pages/*"),  
                        InputFieldMappingEntry(name="content_vector", source="/document/pages/*/content_vector"),
                        # InputFieldMappingEntry(name="header_1", source="/document/header_1"),
                        # InputFieldMappingEntry(name="header_2", source="/document/header_2"),
                        # InputFieldMappingEntry(name="header_3", source="/document/header_3"),
                        # InputFieldMappingEntry(name="header_4", source="/document/header_4"),
                        #metadata
                        InputFieldMappingEntry(name="id", source="/document/metadata_storage_name"),
                        InputFieldMappingEntry(name="file_name", source="/document/metadata_storage_name"),
                        InputFieldMappingEntry(name="file_path", source="/document/metadata_storage_path"),
                        InputFieldMappingEntry(name="folder", source="/document/metadata_storage_path"),
                        InputFieldMappingEntry(name="last_modified", source="/document/metadata_storage_last_modified"),
                    ])
                ],  
                parameters=SearchIndexerIndexProjectionsParameters(  
                    projection_mode=IndexProjectionMode.SKIP_INDEXING_PARENT_DOCUMENTS  
                )  
            )
        )

        print(f"Creating skillset: {skillset.name}")
        self.search_indexer_client.create_or_update_skillset(skillset)
        print(f"Skillset '{skillset.name}' created successfully")


    def create_index(self) -> None:
        """Create the search index for markdown documents."""
        print(f"Creating search index: {self.index_name}")

        fields = [
            SearchField(name="parent_id", type=SearchFieldDataType.String, sortable=True, filterable=True, facetable=True),  
            SearchField(name="title", type=SearchFieldDataType.String, analyzer_name="standard.lucene", sortable=True, filterable=True, facetable=True),  
            SearchField(name="chunk_id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True, analyzer_name="keyword"),  
            SearchField(name="chunk", type=SearchFieldDataType.String, sortable=False, filterable=False, facetable=False),  
            # SearchField(name="header_1", type=SearchFieldDataType.String, sortable=False, filterable=True, facetable=True),  
            # SearchField(name="header_2", type=SearchFieldDataType.String, sortable=False, filterable=True, facetable=True),  
            # SearchField(name="header_3", type=SearchFieldDataType.String, sortable=False, filterable=True, facetable=True),  
            # SearchField(name="header_4", type=SearchFieldDataType.String, sortable=False, filterable=True, facetable=True),  
            SearchField(name="id", type=SearchFieldDataType.String, sortable=False, filterable=True, facetable=True),  
            SimpleField(name="file_path", type=SearchFieldDataType.String, filterable=True),
            SimpleField(name="file_name", type=SearchFieldDataType.String, filterable=True),
            SimpleField(name="folder", type=SearchFieldDataType.String, filterable=True, facetable=True),
            SimpleField(name="last_modified", type=SearchFieldDataType.DateTimeOffset, filterable=True, sortable=True),
            SearchField(name="content_vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single), vector_search_dimensions=3072, vector_search_profile_name="myHnswProfile"),
        ]

        vector_search=VectorSearch(
            profiles=[  
                VectorSearchProfile(  
                    name="myHnswProfile",
                    algorithm_configuration_name="myHnsw",
                    vectorizer_name="myOpenAI",
                )
            ],  
            algorithms=[  
                HnswAlgorithmConfiguration(name="myHnsw"),
            ],  
            vectorizers=[  
                AzureOpenAIVectorizer(  
                    vectorizer_name="myOpenAI",
                    parameters=AzureOpenAIVectorizerParameters(  
                        resource_url=config.azure_openai_endpoint,
                        deployment_name="text-embedding-3-large",
                        model_name="text-embedding-3-large",
                        auth_identity=config.search_service_identity
                    ),
                ),  
            ],  
        )

        semantic_search=SemanticSearch(
            configurations=[
                SemanticConfiguration(
                    name="default",
                    prioritized_fields=SemanticPrioritizedFields(
                        title_field=SemanticField(field_name="title"),
                        content_fields=[SemanticField(field_name="chunk")],
                    )
                )
            ])
        
        # Create the search index
        index = SearchIndex(
            name=self.index_name, 
            vector_search=vector_search,
            semantic_search=semantic_search,
            fields=fields)
        
        try:
            result = self.search_index_client.create_or_update_index(index)
            print(f"Index '{result.name}' created successfully")
        except Exception as e:
            print(f"Error creating index: {e}")
            raise
    
    def create_data_source(self) -> None:
        """Create the data source connection to Azure Storage."""
        print(f"Creating data source: {self.data_source_name}")
        print(config.search_service_identity)
        
        # Create data source connection
        data_source = SearchIndexerDataSourceConnection(
            name=self.data_source_name,
            type="azureblob",
            connection_string=f"ResourceId={config.storage_endpoint_id}",
            data_change_detection_policy=HighWaterMarkChangeDetectionPolicy(high_water_mark_column_name="metadata_storage_last_modified"),
            container=SearchIndexerDataContainer(
                name=self.storage_container_name,
                query="knowledge-base"  # Process files in the knowledge-base folder
            ),
            description="Data source for markdown files in knowledge-base folder",
            identity=config.search_service_identity
        )
        
        try:

            result = self.search_indexer_client.create_or_update_data_source_connection(data_source)
            print(f"Data source '{result.name}' created successfully")
        except Exception as e:
            print(f"Error creating data source: {e}")
            raise
    
    def create_indexer(self) -> None:
        """Create the indexer to process markdown files."""
        print(f"Creating indexer: {self.indexer_name}")
        
        indexer_parameters = IndexingParameters(
            configuration=IndexingParametersConfiguration(
                indexed_file_name_extensions=".md",
                parsing_mode="markdown",
                query_timeout=None # type: ignore
            ))
        
        # Create indexer
        indexer = SearchIndexer(
            name=self.indexer_name,
            data_source_name=self.data_source_name,
            target_index_name=self.index_name,
            description="Indexer for markdown files in knowledge-base folder",
            skillset_name="markdown-skillset",
            parameters=indexer_parameters,
        )
        
        try:
            result = self.search_indexer_client.create_or_update_indexer(indexer)
            print(f"Indexer '{result.name}' created successfully")
        except Exception as e:
            print(f"Error creating indexer: {e}")
            raise
    
    def run_indexer(self) -> None:
        """Run the indexer to start processing documents."""
        print(f"Running indexer: {self.indexer_name}")
        
        try:
            self.search_indexer_client.run_indexer(self.indexer_name)
            print(f"Indexer '{self.indexer_name}' started successfully")
        except Exception as e:
            print(f"Error running indexer: {e}")
            raise
    
    def get_indexer_status(self) -> Optional[SearchIndexerStatus]:
        """Get the status of the indexer."""
        try:
            status = self.search_indexer_client.get_indexer_status(self.indexer_name)
            return status
        except Exception as e:
            print(f"Error getting indexer status: {e}")
            return None
    
    def setup_complete_search_solution(self) -> None:
        """Set up the complete Azure AI Search solution."""
        print("Setting up Azure AI Search solution for markdown files...")
        print("=" * 60)
        
        try:
            # Create index
            self.create_index()
            print()
            
            # Create data source
            self.create_data_source()
            print()

            # Create skillset
            self.create_skillset()
            print()
            
            # Create indexer
            self.create_indexer()
            print()
            
            # Run indexer
            self.run_indexer()
            print()
            
            print("Azure AI Search solution setup completed successfully!")
            print(f"Index name: {self.index_name}")
            print(f"Data source: {self.data_source_name}")
            print(f"Indexer: {self.indexer_name}")
            print(f"Skillset: markdown-skillset")
            print("The indexer will process markdown files from the knowledge-base folder.")
            
        except Exception as e:
            print(f"Error during setup: {e}")
            raise


def load_environment_variables() -> dict:
    """Load environment variables from .env file."""
    load_dotenv()
    
    required_vars = [
        "AZURE_SEARCH_SERVICE_ENDPOINT",
        "AZURE_STORAGE_ACCOUNT_NAME",
    ]
    
    env_vars = {}
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        env_vars[var] = value
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return env_vars


def main():
    """Main function to set up Azure AI Search index and indexer."""
    try:
        # Load environment variables
        print("Loading environment variables...")
        env_vars = load_environment_variables()
        
        # Create Azure Search Index Manager
        manager = AzureSearchIndexManager(
            search_service_endpoint=env_vars["AZURE_SEARCH_SERVICE_ENDPOINT"],
            storage_container_name=os.getenv("AZURE_STORAGE_CONTAINER_NAME", "evaluation-knowledge-base")
        )
        
        # Set up the complete search solution
        manager.setup_complete_search_solution()
        
        # Display status
        print("\nChecking indexer status...")
        status = manager.get_indexer_status()
        if status:
            print(f"Indexer status: {status.status}")
            if status.last_result:
                print(f"Last run: {status.last_result.start_time}")
                print(f"Items processed: {status.last_result.item_count}")
                print(f"Items failed: {status.last_result.failed_item_count}")
        
    except Exception as e:
        print(f"Error: {e}")
        raise
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())