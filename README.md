# Microsoft Agent Framework Quick Start

This project demonstrates how to create and use a simple AI agent using the Microsoft Agent Framework with Azure AI as the backend.

## Overview

This quick start guide implements the [Microsoft Agent Framework Python tutorial](https://learn.microsoft.com/en-us/agent-framework/tutorials/quick-start?pivots=programming-language-python) using `uv` for package management.

The sample creates a basic agent using `ChatAgent` with `AzureAIAgentClient` and custom instructions to tell jokes.

## Prerequisites

Before you begin, ensure you have the following:

1. **Python 3.10 or later** - This project uses Python 3.12
2. **uv** - Fast Python package installer and resolver ([install uv](https://github.com/astral-sh/uv))
3. **Azure AI project** with a deployed model (e.g., `gpt-4o-mini`)
4. **Azure CLI** installed and authenticated (`az login`)

> **Note**: This demo uses Azure CLI credentials for authentication. Make sure you're logged in with `az login` and have access to the Azure AI project.

## Setup

### 1. Install Dependencies

The project uses `uv` for dependency management. All required packages are already configured in `pyproject.toml`.

To install dependencies:

```bash
# The dependencies are already installed if you used uv to set up the project
# If you need to reinstall or sync:
uv sync
```

### 2. Configure Environment Variables

Copy the `.env.example` file to `.env` and fill in your Azure AI project details:

```bash
cp .env.example .env
```

Edit `.env` and set the following variables:

```bash
# Your Azure AI project endpoint
AZURE_AI_PROJECT_ENDPOINT=https://your-project.eastus.api.azureml.ms

# The name of your model deployment
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o-mini
```

### 3. Authenticate with Azure

Make sure you're logged in to Azure CLI:

```bash
az login
```

Verify you have access to your Azure AI project.

## Running the Sample

Run the agent using `uv`:

```bash
uv run main.py
```

Or activate the virtual environment and run directly:

```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python main.py
```

### Expected Output

The agent will use the Azure AI model to generate a joke about a pirate. Example output:

```
Using endpoint: https://your-project.eastus.api.azureml.ms
Using model deployment: gpt-4o-mini

Why couldn't the pirate play cards?
Because he was standing on the deck!
```

## Project Structure

```
agent-framework-quickstart/
├── main.py              # Main application code
├── pyproject.toml       # Project configuration and dependencies
├── .env.example         # Example environment variables
├── .env                 # Your environment variables (not in git)
└── README.md           # This file
```

## How It Works

The sample demonstrates the basic pattern for using Microsoft Agent Framework:

1. **Import required modules**:
   - `ChatAgent` - The main agent class
   - `AzureAIAgentClient` - Client for Azure AI services
   - `AzureCliCredential` - Authentication using Azure CLI

2. **Create an agent** with:
   - A chat client configured with Azure credentials
   - Custom instructions (in this case, "You are good at telling jokes")

3. **Run the agent** with a prompt and get the response

## Troubleshooting

### Authentication Issues

If you get authentication errors:
- Make sure you've run `az login`
- Verify you have the correct permissions on the Azure AI project
- Check that your Azure subscription is active

### Environment Variable Issues

If you get errors about missing environment variables:
- Make sure you've created the `.env` file from `.env.example`
- Verify the values are correct (no trailing spaces, correct URLs)
- The application will print helpful error messages if variables are missing

### Package Issues

If you encounter package installation issues:
- Make sure you're using `uv` version 0.1.0 or later
- Try removing the `.venv` directory and running `uv sync` again
- Check that you have Python 3.10 or later installed

## Next Steps

For more detailed examples and advanced scenarios, see:
- [Azure AI Agent Examples](https://learn.microsoft.com/en-us/azure/ai-services/agents/examples)
- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/en-us/agent-framework/)

## Resources

- [Microsoft Agent Framework Quick Start](https://learn.microsoft.com/en-us/agent-framework/tutorials/quick-start?pivots=programming-language-python)
- [Azure AI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/)
- [uv Documentation](https://github.com/astral-sh/uv)
