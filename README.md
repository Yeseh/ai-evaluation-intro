# AI Agent Evaluation Demo

A demonstration repository showcasing how to evaluate AI agents using Azure AI Search and Azure AI Foundry. This demo shows practical examples of building knowledge-based AI agents and evaluating their performance using various metrics.

Perfect for presentations, workshops, or learning about AI agent evaluation in practice!

## 🎯 What This Demo Shows

- **Knowledge Base Setup**: How to index markdown documents with Azure AI Search
- **AI Agent Creation**: Building agents that can search and reason over knowledge bases
- **Individual Evaluations**: Testing specific aspects like groundedness, intent resolution, and content safety
- **Document Retrieval Quality**: Measuring how well your agent finds relevant information
- **Batch Evaluation**: Running evaluations at scale with multiple test cases
- **Interactive Examples**: Jupyter notebooks you can run step-by-step

## 🚀 Quick Start

### What You'll Need

- Azure subscription with these services:
  - Azure AI Search (free tier works!)
  - Azure Storage Account
  - Azure AI Foundry project
  - Azure OpenAI service
- Python 3.12+

### 5-Minute Setup

1. **Clone and install:**
   ```bash
   git clone <this-repo>
   cd evaluation-intro
   pip install -e .
   ```

2. **Configure your Azure services:**
   ```bash
   cp .env.template .env
   # Edit .env with your Azure credentials (see below)
   ```

3. **Run the demos:**
   ```bash
   # Set up the knowledge base index
   python main.py
   
   # Open the interactive demos
   jupyter notebook demo_ai_foundry.ipynb
   ```

### Environment Configuration

Copy `.env.template` to `.env` and fill in your Azure service details:

```env
# Azure AI Search - Get from Azure Portal
AZURE_SEARCH_SERVICE_NAME=your-search-service-name
AZURE_SEARCH_ADMIN_KEY=your-admin-key

# Azure Storage - Any storage account works
AZURE_STORAGE_ACCOUNT_NAME=your-storage-account
AZURE_STORAGE_ACCOUNT_KEY=your-storage-key
AZURE_STORAGE_CONTAINER_NAME=knowledge-base

# Azure OpenAI - For the LLM models
AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key

# Azure AI Foundry - For evaluation features
FOUNDRY_PROJECT_ENDPOINT=https://your-project.cognitiveservices.azure.com/
FOUNDRY_PROJECT_NAME=your-project-name
RESOURCE_GROUP_NAME=your-resource-group
SUBSCRIPTION_ID=your-subscription-id
```

## 📚 Demo Scenarios

This demo uses a fictional consulting company (Meridian Strategic Consulting) knowledge base with realistic documents about:
- Expert profiles and skills
- Service offerings
- Industry expertise
- Project methodologies
- Case studies

### Scenario 1: Basic Knowledge Search
```bash
python search_knowledge_base.py
# Try: "Who are the AI experts?" or "What services do you offer?"
```

### Scenario 2: AI Agent with Knowledge Base
Open `demo_ai_foundry.ipynb` and run the cells to see:
- How to create an AI agent with knowledge base access
- Agent responding to complex queries like "I need a consultant with AI/ML expertise for healthcare"

### Scenario 3: Evaluation in Action
The notebook demonstrates:
- **Intent Resolution**: Does the agent understand what you're asking?
- **Groundedness**: Are responses based on actual knowledge base content?
- **Content Safety**: Are responses appropriate and safe?
- **Retrieval Quality**: How well does the search find relevant documents?
- **Batch Evaluation**: Testing multiple scenarios at once

## 🎓 Learning Objectives

After running this demo, you'll understand:

- **RAG Patterns**: How to combine search with LLMs for knowledge-based answers
- **Agent Architecture**: Building agents that can use tools (like search) to answer questions
- **Evaluation Strategies**: Multiple ways to measure AI agent performance
- **Azure AI Services**: Practical integration of Search, OpenAI, and AI Foundry
- **Quality Metrics**: What makes a good vs. poor agent response

## 💡 Demo Tips

**First time running?**
1. Make sure all Azure services are created and running
2. Run `python main.py` first to set up the search index
3. Start with `demo_ai_foundry.ipynb` - it has the most complete examples

**Having issues?**
- Check your `.env` file - most problems are configuration-related
- Ensure your Azure OpenAI deployment uses "gpt-4" or similar model
- The knowledge base documents are included locally, so no Azure Storage needed for basic demo

**Want to go deeper?**
- Try different queries to see how evaluation scores change
- Modify the agent instructions and see the impact
- Add your own test cases to `eval.jsonl`

## 📊 What Gets Evaluated

| Demo Section | What It Shows | Why It Matters |
|--------------|---------------|----------------|
| **Intent Resolution** | Does the agent understand the question? | Avoid irrelevant responses |
| **Groundedness** | Are answers based on actual documents? | Prevent hallucination |
| **Content Safety** | Are responses appropriate? | Ensure professional, safe outputs |
| **Retrieval Quality** | Does search find the right documents? | Better search = better answers |
| **Batch Evaluation** | How does it perform across many test cases? | Real-world performance assessment |

## 📁 Demo Structure

```
├── demo_ai_foundry.ipynb          # 👈 START HERE - Main demo notebook
├── demo_llm_as_judge.ipynb        # Alternative evaluation approaches
├── demo_semantic_similarity.ipynb # Similarity-based evaluation
├── main.py                        # Setup script (run first)
├── search_knowledge_base.py       # Search utilities
├── eval.jsonl                     # Sample test cases
├── config.py                      # Configuration
└── knowledge-base/                # Sample documents
    ├── people-expertise/          # Expert profiles, skills
    ├── core-business/             # Services, industry info
    ├── methodologies/             # How-to guides
    └── market-intelligence/       # Industry analysis
```

## 🔧 Customizing the Demo

Want to adapt this for your own use case?

- **Replace knowledge-base/**: Add your own markdown documents
- **Update eval.jsonl**: Create test cases relevant to your domain
- **Modify agent instructions**: Change the agent's role and behavior
- **Add new evaluators**: Test different aspects of performance

## 🎤 Using This for Presentations

This demo is perfect for:
- **Workshops**: Hands-on AI evaluation training
- **Technical talks**: Live coding demonstrations
- **Sales demos**: Showing Azure AI capabilities
- **Learning sessions**: Understanding RAG evaluation patterns

**Presentation flow:**
1. Show the problem: "How do you know if your AI agent is good?"
2. Demo the agent: Run a few queries, show responses
3. Introduce evaluation: "Let's measure the quality..."
4. Walk through metrics: Intent, groundedness, safety, retrieval
5. Show batch evaluation: "Now let's test 100 cases at once"

**Sample queries that work well:**
- "I need an AI expert for a healthcare project"
- "What's your experience with financial services?"
- "How do you approach digital transformation?"

## 🤝 Contributing

Found a bug or want to improve the demo? PRs welcome! This is meant to be a learning resource for the community.

## 📄 License

This demo is provided as-is for educational and demonstration purposes. Feel free to use it in your own presentations and workshops!