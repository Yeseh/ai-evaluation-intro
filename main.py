"""
Main entry point for the evaluation-intro project.
Demonstrates Azure AI Search setup for processing markdown files.
"""

from azure_search_setup import main as setup_azure_search


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
