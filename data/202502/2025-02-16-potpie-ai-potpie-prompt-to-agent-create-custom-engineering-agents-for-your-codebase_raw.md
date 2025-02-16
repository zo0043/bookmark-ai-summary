Title: GitHub - potpie-ai/potpie: Prompt-To-Agent : Create custom engineering agents for your codebase

URL Source: https://github.com/potpie-ai/potpie

Markdown Content:
[![Image 16: Momentum logo](https://private-user-images.githubusercontent.com/19893222/382581907-1a0b9824-833b-4c0a-b56d-ede5623295ca.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Mzk3MTQyOTgsIm5iZiI6MTczOTcxMzk5OCwicGF0aCI6Ii8xOTg5MzIyMi8zODI1ODE5MDctMWEwYjk4MjQtODMzYi00YzBhLWI1NmQtZWRlNTYyMzI5NWNhLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTAyMTYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwMjE2VDEzNTMxOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTljMmIxZjFkMDdiMmNiNTdkMjM2OTE4ZGZmOTdjNWU5ZjhmZmQ4OGNmOGU4OTA2NmQ0NGEwMmQxNDNkOTk1YjgmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.FSqPGfj1TH2Cf0dOsW1C1RC5rHzoFPS4cFGXjqMeFu0)](https://potpie.ai/?utm_source=github)

[![Image 17: Apache 2.0](https://camo.githubusercontent.com/b3d6919389bd3d8554048ce1e2a81789c615d682586c17a3975930cdb3d304f1/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f706f747069652d61692f706f74706965)](https://github.com/potpie-ai/potpie/blob/main/LICENSE)[![Image 18: GitHub Repo stars](https://camo.githubusercontent.com/12b0d843b3769d8e772a3c175dea6f9b147283978eb51356bfb6687a21defbf9/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f73746172732f706f747069652d61692f706f74706965)](https://github.com/potpie-ai/potpie)  
[![Image 19: Join our Discord](https://camo.githubusercontent.com/36ac4cd24b3d424cd6d7dea7b67dcb6fa04d36588624b0ce3bfe9bf649eca1a0/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4a6f696e2532306f75722d446973636f72642d3538363546323f7374796c653d666f722d7468652d6261646765266c6f676f3d646973636f7264266c6f676f436f6c6f723d7768697465)](https://discord.gg/ryk5CMD5v6)  
[![Image 20: tweet](https://camo.githubusercontent.com/4f677ce944dfdeb7a8cd741560d35d006363ef6160adeb63ee3d8c73373b1f51/68747470733a2f2f696d672e736869656c64732e696f2f747769747465722f75726c2f687474702f736869656c64732e696f2e7376673f7374796c653d736f6369616c)](https://twitter.com/intent/tweet?text=I%20created%20custom%20engineering%20agents%20for%20my%20codebase%20in%20minutes%20with%20potpie.ai%20@potpiedotai%20!%F0%9F%A5%A7)

Prompt-To-Agent: Create custom engineering agents for your code


-----------------------------------------------------------------

[](https://github.com/potpie-ai/potpie#prompt-to-agent-create-custom-engineering-agents-for-your-code)

Potpie is an open-source platform that creates AI agents specialized in your codebase, enabling automated code analysis, testing, and development tasks. By building a comprehensive knowledge graph of your code, Potpie's agents can understand complex relationships and assist with everything from debugging to feature development.

[![Image 21: Screenshot 2025-01-09 at 2 18 18 PM](https://private-user-images.githubusercontent.com/19893222/401460208-a400b48f-dc4c-47b1-a42b-26eaf062adb2.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Mzk3MTQyOTgsIm5iZiI6MTczOTcxMzk5OCwicGF0aCI6Ii8xOTg5MzIyMi80MDE0NjAyMDgtYTQwMGI0OGYtZGM0Yy00N2IxLWE0MmItMjZlYWYwNjJhZGIyLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTAyMTYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwMjE2VDEzNTMxOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWRkMTE1NTkyODdkZjI1MTAxZGFkMzFhZmQ4N2Q1NWE0NmQyOTE3MTIwODY1OWRlYzlmYzM0NTNkNzRhYmEyZWMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.-88th9apMQvlgxUcMw0C3COVpXNp__3LAI3Yiq4ftzc)](https://private-user-images.githubusercontent.com/19893222/401460208-a400b48f-dc4c-47b1-a42b-26eaf062adb2.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Mzk3MTQyOTgsIm5iZiI6MTczOTcxMzk5OCwicGF0aCI6Ii8xOTg5MzIyMi80MDE0NjAyMDgtYTQwMGI0OGYtZGM0Yy00N2IxLWE0MmItMjZlYWYwNjJhZGIyLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTAyMTYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwMjE2VDEzNTMxOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWRkMTE1NTkyODdkZjI1MTAxZGFkMzFhZmQ4N2Q1NWE0NmQyOTE3MTIwODY1OWRlYzlmYzM0NTNkNzRhYmEyZWMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.-88th9apMQvlgxUcMw0C3COVpXNp__3LAI3Yiq4ftzc)

📚 Table of Contents
--------------------

[](https://github.com/potpie-ai/potpie#-table-of-contents)

*   [🥧 Why Potpie?](https://github.com/potpie-ai/potpie#why-potpie)
*   [🤖 Our Prebuilt Agents](https://github.com/potpie-ai/potpie#prebuilt-agents)
*   [🛠️ Tooling](https://github.com/potpie-ai/potpie#potpies-tooling-system)
*   [🚀 Getting Started](https://github.com/potpie-ai/potpie#getting-started)
*   [💡 Use Cases](https://github.com/potpie-ai/potpie#use-cases)
*   [🛠️ Custom Agents](https://github.com/potpie-ai/potpie#custom-agents-upgrade)
*   [🗝️ Accessing Agents via API Key](https://github.com/potpie-ai/potpie#accessing-agents-via-api-key)
*   [🎨 Make Potpie Your Own](https://github.com/potpie-ai/potpie#make-potpie-your-own)
*   [🤝 Contributing](https://github.com/potpie-ai/potpie#contributing)
*   [📜 License](https://github.com/potpie-ai/potpie#license)
*   [💪 Contributors](https://github.com/potpie-ai/potpie#-thanks-to-all-contributors)

🥧 Why Potpie?
--------------

[](https://github.com/potpie-ai/potpie#-why-potpie)

*   🧠 **Deep Code Understanding**: Built-in knowledge graph captures relationships between code components
*   🤖 **Pre-built & Custom Agents**: Ready-to-use agents for common tasks + build your own
*   🔄 **Seamless Integration**: Works with your existing development workflow
*   📈 **Flexible**: Handles codebases of any size or language

🔌 VSCode Extension
-------------------

[](https://github.com/potpie-ai/potpie#-vscode-extension)

Bring the power of Potpie's AI agents directly into your development environment with our VSCode extension:

*   **Direct Integration**: Access all Potpie agents without leaving your editor
*   **Quick Setup**: Install directly from the [VSCode Marketplace](https://marketplace.visualstudio.com/items?itemName=PotpieAI.potpie-vscode-extension)
*   **Seamless Workflow**: Ask questions, get explanations, and implement suggestions right where you code

🤖 Potpie's Prebuilt Agents
---------------------------

[](https://github.com/potpie-ai/potpie#-potpies-prebuilt-agents)

Potpie offers a suite of specialized codebase agents for automating and optimizing key aspects of software development:

*   **Debugging Agent**: Automatically analyzes stacktraces and provides debugging steps specific to your codebase.
*   **Codebase Q&A Agent**: Answers questions about your codebase and explains functions, features, and architecture.
*   **Code Changes Agent**: Analyzes code changes, identifies affected APIs, and suggests improvements before merging.
*   **Integration Test Agent**: Generates integration test plans and code for flows to ensure components work together properly.
*   **Unit Test Agent**: Automatically creates unit test plan and code for individual functions to enhance test coverage.
*   **LLD Agent**: Creates a low level design for implementing a new feature by providing functional requirements to this agent.
*   **Code Generation Agent**: Generates code for new features, refactors existing code, and suggests optimizations.

🛠️ Potpie's Tooling System
---------------------------

[](https://github.com/potpie-ai/potpie#%EF%B8%8F-potpies-tooling-system)

Potpie provides a set of tools that agents can use to interact with the knowledge graph and the underlying infrastructure:

*   **get\_code\_from\_probable\_node\_name**: Retrieves code snippets based on a probable node name.
*   **get\_code\_from\_node\_id**: Fetches code associated with a specific node ID.
*   **get\_code\_from\_multiple\_node\_ids**: Retrieves code snippets for multiple node IDs simultaneously.
*   **ask\_knowledge\_graph\_queries**: Executes vector similarity searches to obtain relevant information.
*   **get\_nodes\_from\_tags**: Retrieves nodes tagged with specific keywords.
*   **get\_code\_graph\_from\_node\_id/name**: Fetches code graph structures for a specific node.
*   **change\_detection**: Detects changes in the current branch compared to the default branch.
*   **get\_code\_file\_structure**: Retrieves the file structure of the codebase.

🚀 Getting Started
------------------

[](https://github.com/potpie-ai/potpie#-getting-started)

### Prerequisites

[](https://github.com/potpie-ai/potpie#prerequisites)

*   Docker installed and running
*   OpenAI API key
*   Git installed (for repository access)
*   Python 3.10.x

### Setup Steps

[](https://github.com/potpie-ai/potpie#setup-steps)

**Install Python 3.10**

*   Download and install Python 3.10 from the official Python website: [https://www.python.org/downloads/release/python-3100/](https://www.python.org/downloads/release/python-3100/)

1.  **Prepare Your Environment**
    
    *   Create a `.env` file based on the `.env.template`
        
    *   Add the following required configurations:
        
        isDevelopmentMode=enabled
        ENV=development
        OPENAI\_API\_KEY=<your-openai-key\>
        POSTGRES\_SERVER=postgresql://postgres:mysecretpassword@localhost:5432/momentum
        NEO4J\_URI=bolt://127.0.0.1:7687
        NEO4J\_USERNAME=neo4j
        NEO4J\_PASSWORD=mysecretpassword
        REDISHOST=127.0.0.1
        REDISPORT=6379
        BROKER\_URL=redis://127.0.0.1:6379/0
        CELERY\_QUEUE\_NAME=dev
        defaultUsername=defaultuser
        PROJECT\_PATH=projects #repositories will be downloaded/cloned to this path on your system.
        
    *   Create a Virtual Environment using Python 3.10:
        
        python3.10 -m venv venv
        source venv/bin/activate
        
        alternatively, you can also use the `virtualenv` library.
        
    *   Install dependencies in your venv:
        
        pip install -r requirements.txt
        
2.  **Start Potpie**
    
    chmod +x start.sh
    ./start.sh
    
3.  **Authentication Setup** (Skip this step in development mode)
    
    curl -X POST 'http://localhost:8001/api/v1/login' \\
      -H 'Content-Type: application/json' \\
      -d '{
        "email": "your-email",
        "password": "your-password"
      }'
    # Save the bearer token from the response for subsequent requests
    
4.  **Initialize Repository Parsing**
    
    # For development mode:
    curl -X POST 'http://localhost:8001/api/v1/parse' \\
      -H 'Content-Type: application/json' \\
      -d '{
        "repo\_path": "path/to/local/repo",
        "branch\_name": "main"
      }'
    
    # For production mode:
    curl -X POST 'http://localhost:8001/api/v1/parse' \\
      -H 'Content-Type: application/json' \\
      -d '{
        "repo\_name": "owner/repo-name",
        "branch\_name": "main"
      }'
    # Save the project\_id from the response
    
5.  **Monitor Parsing Status**
    
    curl -X GET 'http://localhost:8001/api/v1/parsing-status/your-project-id'
    # Wait until parsing is complete
    
6.  **View Available Agents**
    
    curl -X GET 'http://localhost:8001/api/v1/list-available-agents/?list\_system\_agents=true'
    # Note down the agent\_id you want to use
    
7.  **Create a Conversation**
    
    curl -X POST 'http://localhost:8001/api/v1/conversations/' \\
      -H 'Content-Type: application/json' \\
      -d '{
        "user\_id": "your\_user\_id",
        "title": "My First Conversation",
        "status": "active",
        "project\_ids": \["your-project-id"\],
        "agent\_ids": \["chosen-agent-id"\]
      }'
    # Save the conversation\_id from the response
    
8.  **Start Interacting with Your Agent**
    
    curl -X POST 'http://localhost:8001/api/v1/conversations/your-conversation-id/message/' \\
      -H 'Content-Type: application/json' \\
      -d '{
        "content": "Your question or request here"
      }'
    
9.  **View Conversation History** (Optional)
    
    curl -X GET 'http://localhost:8001/api/v1/conversations/your-conversation-id/messages/?start=0&limit=10'
    

💡 Use Cases
------------

[](https://github.com/potpie-ai/potpie#-use-cases)

*   **Onboarding**: For developers new to a codebase, the codebase QnA agent helps them understand the codebase and get up to speed quickly. Ask it how to setup a new project, how to run the tests etc

> We tried to onboard ourselves with Potpie to the [**AgentOps**](https://github.com/AgentOps-AI/AgentOps) codebase and it worked like a charm : Video [here](https://youtu.be/_mPixNDn2r8).

*   **Codebase Understanding**: Answer questions about any library you're integrating, explain functions, features, and architecture.

> We used the Q&A agent to understand the underlying working of a feature of the [**CrewAI**](https://github.com/CrewAIInc/CrewAI) codebase that was not documented in official docs : Video [here](https://www.linkedin.com/posts/dhirenmathur_what-do-you-do-when-youre-stuck-and-even-activity-7256704603977613312-8X8G).

*   **Low Level Design**: Get detailed implementation plans for new features or improvements before writing code.

> We fed an open issue from the [**Portkey-AI/Gateway**](https://github.com/Portkey-AI/Gateway) project to this agent to generate a low level design for it: Video [here](https://www.linkedin.com/posts/dhirenmathur_potpie-ai-agents-vs-llms-i-am-extremely-activity-7255607456448286720-roOC).

*   **Reviewing Code Changes**: Understand the functional impact of changes and compute the blast radius of modifications.

> Here we analyse a PR from the [**mem0ai/mem0**](https://github.com/mem0ai/mem0) codebase and understand its blast radius : Video [here](https://www.linkedin.com/posts/dhirenmathur_prod-is-down-three-words-every-activity-7257007131613122560-o4A7).

*   **Debugging**: Get step-by-step debugging guidance based on stacktraces and codebase context.
    
*   **Testing**: Generate contextually aware unit and integration test plans and test code that understand your codebase's structure and purpose.
    

🛠️ Custom Agents [Upgrade ✨](https://potpie.ai/pricing)
--------------------------------------------------------

[](https://github.com/potpie-ai/potpie#%EF%B8%8F-custom-agents-upgrade-)

With Custom Agents, you can design personalized tools that handle repeatable tasks with precision. Key components include:

*   **System Instructions**: Define the agent's task, goal, and expected output
*   **Agent Information**: Metadata about the agent's role and context
*   **Tasks**: Individual steps for job completion
*   **Tools**: Functions for querying the knowledge graph or retrieving code

🗝️ Accessing Agents via API Key
--------------------------------

[](https://github.com/potpie-ai/potpie#%EF%B8%8F-accessing-agents-via-api-key)

You can access Potpie Agents through an API key, enabling integration into CI/CD workflows and other automated processes. For detailed instructions, please refer to the [Potpie API documentation](https://docs.potpie.ai/agents/api-access).

*   **Generate an API Key**: Easily create an API key for secure access.
*   **Parse Repositories**: Use the Parse API to analyze code repositories and obtain a project ID.
*   **Monitor Parsing Status**: Check the status of your parsing requests.
*   **Create Conversations**: Initiate conversations with specific agents using project and agent IDs adn get a conversation id.
*   **Send Messages**: Communicate with agents by sending messages within a conversation.

🎨 Make Potpie Your Own
-----------------------

[](https://github.com/potpie-ai/potpie#-make-potpie-your-own)

Potpie is designed to be flexible and customizable. Here are key areas to personalize your own deployment:

### 1\. System Prompts Configuration

[](https://github.com/potpie-ai/potpie#1-system-prompts-configuration)

Modify prompts in `app/modules/intelligence/prompts/system_prompt_setup.py`

### 2\. Add New Agents

[](https://github.com/potpie-ai/potpie#2-add-new-agents)

Create new agents in `app/modules/intelligence/agents/chat_agents` and `app/modules/intelligence/agents/agentic_tools`

### 3\. Agent Behavior Customization

[](https://github.com/potpie-ai/potpie#3-agent-behavior-customization)

Modify guidelines within each agent's prompt in the `app/modules/intelligence/agents` directory

### 4\. Tool Integration

[](https://github.com/potpie-ai/potpie#4-tool-integration)

Edit or add tools in the `app/modules/intelligence/tools` directory

🤝 Contributing
---------------

[](https://github.com/potpie-ai/potpie#-contributing)

We welcome contributions! To contribute:

1.  Fork the repository
2.  Create a new branch (`git checkout -b feature-branch`)
3.  Make your changes
4.  Commit (`git commit -m 'Add new feature'`)
5.  Push to the branch (`git push origin feature-branch`)
6.  Open a Pull Request

See [Contributing Guide](https://github.com/potpie-ai/potpie/blob/main/contributing.md) for more details.

📜 License
----------

[](https://github.com/potpie-ai/potpie#-license)

This project is licensed under the Apache 2.0 License - see the [LICENSE](https://github.com/potpie-ai/potpie/blob/main/LICENSE) file for details.

💪 Thanks To All Contributors
-----------------------------

[](https://github.com/potpie-ai/potpie#-thanks-to-all-contributors)

Thanks for spending your time helping build Potpie. Keep rocking 🥂

[![Image 22: Contributors](https://camo.githubusercontent.com/1eb988a7432176f2509e00bd5b10eeca8e2d6c6b73c87fda0f7fe836bd8eedb0/68747470733a2f2f636f6e7472696275746f72732d696d672e7765622e6170702f696d6167653f7265706f3d706f747069652d61692f706f74706965)](https://camo.githubusercontent.com/1eb988a7432176f2509e00bd5b10eeca8e2d6c6b73c87fda0f7fe836bd8eedb0/68747470733a2f2f636f6e7472696275746f72732d696d672e7765622e6170702f696d6167653f7265706f3d706f747069652d61692f706f74706965)
