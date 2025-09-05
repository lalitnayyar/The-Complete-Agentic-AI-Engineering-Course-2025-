# The Complete Agentic AI Engineering Course 2025

A comprehensive course covering all aspects of building intelligent AI agents and multi-agent systems. This repository contains 6 complete modules with hands-on labs, community contributions, and real-world applications.

## 🚀 Course Overview

This course teaches you how to build sophisticated AI agents using the latest frameworks and techniques. You'll learn to create autonomous systems that can reason, plan, and execute complex tasks across multiple domains.

## 📚 Table of Contents

- [Course Structure](#-course-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Module Details](#-module-details)
- [Features & Functionality](#-features--functionality)
- [User Guide](#-user-guide)
- [Community Contributions](#-community-contributions)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Contributing](#-contributing)
- [License](#-license)

## 🏗️ Course Structure

### Module 1: Foundations
**Path:** `agents/1_foundations/`

**What you'll learn:**
- Basic agent concepts and patterns
- Prompt engineering fundamentals
- Multi-model evaluation and comparison
- Agent orchestration basics

**Labs:**
- `1_lab1.ipynb` - Introduction to AI agents
- `2_lab2.ipynb` - Multi-model evaluation and parallelization
- `3_lab3.ipynb` - Agent orchestration and workflow patterns
- `4_lab4.ipynb` - RAG (Retrieval-Augmented Generation) integration

**Key Features:**
- Multi-LLM support (OpenAI, Anthropic, Google, etc.)
- Parallel processing and evaluation
- Reflection patterns and self-correction
- Tool integration and function calling

### Module 2: OpenAI SDK
**Path:** `agents/2_openai/`

**What you'll learn:**
- Advanced OpenAI SDK usage
- Function calling and tool integration
- Multi-agent coordination
- Deep research and autonomous agents

**Labs:**
- `1_lab1.ipynb` - OpenAI SDK fundamentals
- `2_lab2.ipynb` - Function calling and tools
- `3_lab3.ipynb` - Multi-agent systems
- `4_lab4.ipynb` - Advanced workflows and research agents

**Key Features:**
- Deep research agents with web search
- Email integration and notifications
- Multi-step reasoning and planning
- Advanced prompt chaining

### Module 3: CrewAI
**Path:** `agents/3_crew/`

**What you'll learn:**
- CrewAI framework for multi-agent systems
- Agent collaboration and task distribution
- Memory and knowledge management
- Production-ready agent deployments

**Projects:**
- `coder/` - AI coding assistant crew
- `debate/` - Multi-agent debate system
- `engineering_team/` - Software engineering crew
- `financial_researcher/` - Financial analysis crew
- `stock_picker/` - Investment analysis crew

**Key Features:**
- Crew-based agent coordination
- Task delegation and workflow management
- Memory persistence and learning
- Production deployment patterns

### Module 4: LangGraph
**Path:** `agents/4_langgraph/`

**What you'll learn:**
- State management in agent systems
- Graph-based agent workflows
- Conditional routing and decision making
- Memory and context management

**Labs:**
- `1_lab1.ipynb` - LangGraph fundamentals
- `2_lab2.ipynb` - Tools and memory integration
- `3_lab3.ipynb` - Advanced state management
- `4_lab4.ipynb` - Complex workflow orchestration

**Key Features:**
- Graph-based agent workflows
- State persistence and management
- Conditional routing and branching
- Tool integration and execution

### Module 5: AutoGen
**Path:** `agents/5_autogen/`

**What you'll learn:**
- Microsoft AutoGen framework
- Multi-agent conversations
- Agent coordination and collaboration
- Distributed agent systems

**Labs:**
- `1_lab1_autogen_agentchat.ipynb` - Basic AutoGen setup
- `2_lab2_autogen_agentchat.ipynb` - Multi-agent conversations
- `3_lab3_autogen_core.ipynb` - Core AutoGen features
- `4_lab4_autogen_distributed.ipynb` - Distributed systems

**Key Features:**
- Conversational AI agents
- Multi-agent chat systems
- Distributed agent coordination
- Advanced conversation management

### Module 6: Model Context Protocol (MCP)
**Path:** `agents/6_mcp/`

**What you'll learn:**
- Model Context Protocol implementation
- Server-client agent architecture
- Tool and resource management
- Advanced agent communication

**Labs:**
- `1_lab1.ipynb` - MCP fundamentals
- `2_lab2.ipynb` - Server implementation
- `3_lab3.ipynb` - Client integration
- `4_lab4.ipynb` - Advanced MCP features
- `5_lab5.ipynb` - Production deployment

**Key Features:**
- MCP server and client implementation
- Tool and resource management
- Advanced agent communication
- Production-ready deployments

## 🛠️ Features & Functionality

### Core Capabilities
- **Multi-Agent Systems**: Build sophisticated multi-agent workflows
- **Tool Integration**: Seamless integration with external tools and APIs
- **Memory Management**: Persistent memory and context management
- **Parallel Processing**: Efficient parallel agent execution
- **Error Handling**: Robust error handling and recovery mechanisms
- **Monitoring**: Built-in logging and monitoring capabilities

### Supported Frameworks
- **OpenAI**: GPT models and function calling
- **Anthropic**: Claude models and advanced reasoning
- **Google**: Gemini models and multimodal capabilities
- **CrewAI**: Multi-agent coordination framework
- **LangGraph**: State management and workflow orchestration
- **AutoGen**: Microsoft's multi-agent conversation framework
- **MCP**: Model Context Protocol for agent communication

### Integration Capabilities
- **Web Search**: Real-time web search and information retrieval
- **Email**: Email generation and sending capabilities
- **File Processing**: PDF, document, and image processing
- **Database**: Database integration and querying
- **APIs**: REST API integration and management
- **Notifications**: Push notifications and alerts

## 📖 User Guide

### Prerequisites
- Python 3.9 or higher
- Git
- Jupyter Notebook
- API keys for desired LLM providers

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/lalitnayyar/The-Complete-Agentic-AI-Engineering-Course-2025-.git
cd The-Complete-Agentic-AI-Engineering-Course-2025-
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
# Create .env file
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
```

4. **Start with Module 1:**
```bash
cd agents/1_foundations
jupyter notebook
```

### Getting Started

1. **Begin with Foundations**: Start with `1_foundations/1_lab1.ipynb`
2. **Follow the sequence**: Complete labs in order within each module
3. **Experiment**: Try the community contributions and variations
4. **Build projects**: Use the provided templates to build your own agents

### Quick Start Example

```python
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Simple agent example
def simple_agent(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Use the agent
result = simple_agent("Explain quantum computing in simple terms")
print(result)
```

## 🌟 Community Contributions

The repository includes extensive community contributions showcasing:

### Advanced Implementations
- **Deep Research Agents**: Autonomous research and analysis systems
- **Multi-Model Evaluators**: Comprehensive model comparison tools
- **Workflow Patterns**: Reusable agent workflow templates
- **Integration Examples**: Real-world API and service integrations

### Specialized Applications
- **Financial Analysis**: Stock picking and market analysis agents
- **Code Generation**: AI-powered coding assistants
- **Content Creation**: Blog and article generation systems
- **Customer Service**: Automated customer support agents

### Production Examples
- **Web Applications**: Gradio and Streamlit interfaces
- **API Services**: RESTful agent services
- **Database Integration**: Agent-database interaction patterns
- **Monitoring Systems**: Agent performance and health monitoring

## 📁 Project Structure

```
agents/
├── 1_foundations/           # Basic agent concepts
│   ├── 1_lab1.ipynb        # Introduction to agents
│   ├── 2_lab2.ipynb        # Multi-model evaluation
│   ├── 3_lab3.ipynb        # Agent orchestration
│   ├── 4_lab4.ipynb        # RAG integration
│   ├── app.py              # Web application
│   └── community_contributions/  # Community projects
├── 2_openai/               # OpenAI SDK module
│   ├── 1_lab1.ipynb        # OpenAI fundamentals
│   ├── 2_lab2.ipynb        # Function calling
│   ├── 3_lab3.ipynb        # Multi-agent systems
│   ├── 4_lab4.ipynb        # Advanced workflows
│   └── community_contributions/  # Community projects
├── 3_crew/                 # CrewAI module
│   ├── coder/              # Coding assistant crew
│   ├── debate/             # Debate system crew
│   ├── engineering_team/   # Engineering crew
│   ├── financial_researcher/ # Financial analysis crew
│   ├── stock_picker/       # Investment analysis crew
│   └── community_contributions/  # Community projects
├── 4_langgraph/            # LangGraph module
│   ├── 1_lab1.ipynb        # LangGraph fundamentals
│   ├── 2_lab2.ipynb        # Tools and memory
│   ├── 3_lab3.ipynb        # State management
│   ├── 4_lab4.ipynb        # Complex workflows
│   └── community_contributions/  # Community projects
├── 5_autogen/              # AutoGen module
│   ├── 1_lab1_autogen_agentchat.ipynb  # Basic AutoGen
│   ├── 2_lab2_autogen_agentchat.ipynb  # Multi-agent chat
│   ├── 3_lab3_autogen_core.ipynb       # Core features
│   ├── 4_lab4_autogen_distributed.ipynb # Distributed systems
│   └── community_contributions/  # Community projects
├── 6_mcp/                  # MCP module
│   ├── 1_lab1.ipynb        # MCP fundamentals
│   ├── 2_lab2.ipynb        # Server implementation
│   ├── 3_lab3.ipynb        # Client integration
│   ├── 4_lab4.ipynb        # Advanced features
│   ├── 5_lab5.ipynb        # Production deployment
│   └── community_contributions/  # Community projects
├── guides/                 # Technical guides
│   ├── 01_intro.ipynb      # Course introduction
│   ├── 02_command_line.ipynb # Command line basics
│   ├── 03_git_and_github.ipynb # Git and GitHub
│   ├── 04_technical_foundations.ipynb # Technical foundations
│   ├── 05_notebooks.ipynb  # Jupyter notebooks
│   ├── 06_python_foundations.ipynb # Python basics
│   ├── 07_vibe_coding_and_debugging.ipynb # Coding practices
│   ├── 08_debugging.ipynb  # Debugging techniques
│   ├── 09_ai_apis_and_ollama.ipynb # AI APIs
│   ├── 10_intermediate_python.ipynb # Intermediate Python
│   ├── 11_async_python.ipynb # Async Python
│   └── 12_starting_your_project.ipynb # Project setup
├── assets/                 # Images and resources
├── setup/                  # Setup and troubleshooting
└── requirements.txt        # Python dependencies
```

## 🚀 Getting Started

### For Beginners
1. Start with `guides/01_intro.ipynb` for course overview
2. Complete `guides/06_python_foundations.ipynb` for Python basics
3. Begin Module 1 with `1_foundations/1_lab1.ipynb`
4. Follow the lab sequence in each module

### For Experienced Developers
1. Review the course structure and choose your focus area
2. Start with the module that interests you most
3. Explore community contributions for advanced examples
4. Build your own projects using the provided templates

### For Researchers
1. Examine the community contributions for cutting-edge implementations
2. Study the multi-agent coordination patterns
3. Explore the advanced workflow orchestration examples
4. Use the codebase as a foundation for your research

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Add tests if applicable**
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Contribution Guidelines
- Follow the existing code style
- Add comments and documentation
- Include examples and tests
- Update the README if needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for the GPT models and API
- Anthropic for Claude models
- Google for Gemini models
- CrewAI team for the multi-agent framework
- LangChain team for LangGraph
- Microsoft for AutoGen
- The open-source community for inspiration and contributions

## 📞 Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Discussions**: Join community discussions in GitHub Discussions
- **Documentation**: Check the guides and lab notebooks for detailed instructions

## 🔗 Links

- **Course Repository**: https://github.com/lalitnayyar/The-Complete-Agentic-AI-Engineering-Course-2025-
- **Issues**: https://github.com/lalitnayyar/The-Complete-Agentic-AI-Engineering-Course-2025-/issues
- **Discussions**: https://github.com/lalitnayyar/The-Complete-Agentic-AI-Engineering-Course-2025-/discussions

---

**Happy Learning! 🚀**

Start your journey into the world of intelligent AI agents and build the future of autonomous systems.
