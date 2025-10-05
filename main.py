"""
Main entry point for the evaluation-intro project.
Demonstrates Azure AI Search setup for processing markdown files.
"""

import asyncio
import json
from typing import List
import numpy as np
from openai import AzureOpenAI

from azure_search_setup import main as setup_azure_search
from sklearn.metrics.pairwise import cosine_similarity
from search_knowledge_base import KnowledgeBaseSearcher 
from agent_framework.azure import AzureOpenAIChatClient, AzureAIAgentClient
from azure.identity import DefaultAzureCredential
from azure.identity.aio import DefaultAzureCredential as AsyncDefaultAzureCredential
import config

searcher = KnowledgeBaseSearcher()
credential = DefaultAzureCredential()
async_credential = AsyncDefaultAzureCredential()    
openai_client = AzureOpenAI(
    azure_endpoint=config.azure_openai_endpoint,
    azure_ad_token_provider=lambda: credential.get_token("https://cognitiveservices.azure.com/.default").token,
    api_version="2024-02-01"
)

chat_client = AzureOpenAIChatClient(
    credential=credential,
    deployment_name="gpt-5-chat",
    endpoint=config.azure_openai_endpoint
)

agent_client = AzureAIAgentClient(
    project_endpoint=config.foundry_project_endpoint,
    model_deployment_name="gpt-5-chat",
    async_credential=async_credential
)


def generate_embedding(openai_client: AzureOpenAI, text: str) -> List[float]:
    """Generate embedding for text using Azure OpenAI."""
    try:
        response = openai_client.embeddings.create(
            input=text,
            model="text-embedding-3-large"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []


# Get agent responses using our knowledge base searcher
def get_agent_response(query: str) -> str:
    """Get agent response using semantic search."""
    try:
        results = searcher.semantic_search(query, top=3)
        if results:
            # Combine top results into a comprehensive response
            response_parts = []
            for result in results:
                if result.get('captions'):
                    response_parts.extend(result['captions'])
                else:
                    response_parts.append(result['chunk'])
            
            # If we have answers from semantic search, prioritize those
            if results[0].get('answers'):
                return '. '.join(results[0]['answers'])
            
            return '. '.join(response_parts)
        return "No relevant information found."
    except Exception as e:
        print(f"Error getting agent response: {e}")
        return "Error retrieving information."


from search_knowledge_base import KnowledgeBaseSearcher


answer_instructions = """
Answer the question using the provided context

Question: {question}
Exerpts: {context}
"""

class MeridianKnowledgeBaseAgent():
    def __init__(self, instructions: str):
        self.searcher = KnowledgeBaseSearcher()
        self.instructions = instructions

    async def ask(self, query: str) -> str:
        results = self.searcher.semantic_search(query)

        if results:
            context = "\n".join([f"- {res['chunk']}" for res in results])
            prompt = answer_instructions.format(question=query, context=context)
            agent = chat_client.create_agent(instructions=self.instructions)

            response = await agent.run([prompt])

            return response.text
        else:
            return "Could not find anything!"

def show_agent_answer(query, response, reference):
    import textwrap
    print(f"🔍 Query:\n {textwrap.fill(query, width=80)}\n")
    print(f"📝 Agent Response:\n {textwrap.fill(response, width=80)}\n")
    print(f"📚 Reference Answer:\n {textwrap.fill(reference, width=80)}\n")


def main():
    """Main function - sets up Azure AI Search for markdown processing."""
    print("Welcome to evaluation-intro!")
    print("Setting up Azure AI Search for markdown file processing...")
    print()
    
    try:
        # Run the Azure Search setup
        result = setup_azure_search()
        
        if result == 0:
            print("\n✅ Azure AI Search setup completed successfully!")
            print("Your markdown files in the knowledge-base folder will be indexed and searchable.")
        else:
            print("\n❌ Azure AI Search setup failed. Please check your configuration.")
            
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        print("Please ensure your .env file is configured with the correct Azure credentials.")


if __name__ == "__main__":
    main()
