import os
from dotenv import load_dotenv
from azure.search.documents.indexes.models import SearchIndexerDataUserAssignedIdentity
from azure.identity import DefaultAzureCredential
from azure.identity.aio import DefaultAzureCredential as AsyncDefaultAzureCredential

load_dotenv(override=True)

credential = DefaultAzureCredential()
async_credential = AsyncDefaultAzureCredential()
search_service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
search_service_identity = SearchIndexerDataUserAssignedIdentity(resource_id=os.environ["AZURE_SEARCH_SERVICE_IDENTITY_ID"])
project_endpoint = os.environ["PROJECT_ENDPOINT"]

tenant_id = os.environ["AZURE_TENANT_ID"]
resource_group_name = os.environ["AZURE_RESOURCE_GROUP_NAME"]
storage_account_name = os.environ["AZURE_STORAGE_ACCOUNT_NAME"]
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
storage_endpoint_id = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Storage/storageAccounts/{storage_account_name}/blobServices/default"

azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]