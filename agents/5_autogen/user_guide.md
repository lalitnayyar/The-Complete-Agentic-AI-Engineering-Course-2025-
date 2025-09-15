# 📖 AutoGen Multi-Agent System User Guide

## 🚀 Quick Start Guide

### Step 1: Installation and Setup

#### Prerequisites
- Python 3.9 or higher
- OpenAI API Key
- Git (for cloning the repository)

#### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd agents/5_autogen
   ```

2. **Install Dependencies**
   ```bash
   # Using pip
   pip install -r requirements.txt
   
   # Or using uv (recommended)
   uv add pyautogen
   ```

3. **Set Up Environment Variables**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

4. **Verify Installation**
   ```bash
   python -c "import autogen; print('AutoGen installed successfully')"
   ```

### Step 2: Basic Usage

#### Running the System
```bash
# Start the main system
python world.py

# Or run the test system
python test_innovative_messaging.py
```

#### Launching the Dashboard
```bash
# Launch interactive dashboard
python launch_dashboard.py
```

## 📚 Detailed User Guide

### 1. 🤖 Working with Agents

#### Creating Agents

**Method 1: Using the Creator Agent**
```python
from creator import Creator
from world import GrpcWorkerAgentRuntime, GrpcWorkerAgentRuntimeHost

# Create runtime
host = GrpcWorkerAgentRuntimeHost(address="localhost:50051")
host.start()
worker = GrpcWorkerAgentRuntime(host_address="localhost:50051")
await worker.start()

# Create creator agent
creator = await Creator.register(worker, "Creator", lambda: Creator("Creator"))

# Create new agent
result = await worker.send_message(
    messages.Message(content="agent_specialist.py"), 
    messages.AgentId("Creator", "default")
)
```

**Method 2: Direct Agent Creation**
```python
from agent import Agent

# Create agent directly
agent = await Agent.register(worker, "agent1", lambda: Agent("agent1"))
```

#### Agent Types

1. **Entrepreneur Agent**
   - Generates business ideas
   - Provides strategic advice
   - Bounces ideas off other agents

2. **Creator Agent**
   - Creates new specialized agents
   - Generates agent code
   - Manages agent lifecycle

3. **Marketing Strategist**
   - Develops marketing campaigns
   - Creates promotional content
   - Analyzes market trends

4. **Custom Agents**
   - User-defined specializations
   - Custom behavior patterns
   - Specialized knowledge domains

#### Agent Communication

```python
# Send message between agents
message = messages.Message(content="Generate a business idea for healthcare")
response = await worker.send_message(message, messages.AgentId("agent1", "default"))
```

### 2. 📨 Message System

#### Message Tracking

The system automatically tracks all message exchanges with detailed information:

```python
from message_tracker import message_tracker

# View message statistics
stats = message_tracker.message_stats
print(f"Total exchanges: {stats['total_exchanges']}")
print(f"Success rate: {stats['successful_exchanges'] / stats['total_exchanges'] * 100}%")
```

#### Message Types

1. **idea_exchange**: Business idea sharing and refinement
2. **campaign_exchange**: Marketing campaign development
3. **general_exchange**: General communication
4. **system_exchange**: System-level messages

#### Conversation Management

```python
# Get conversation flow
conversation_id = "your_conversation_id"
flow = message_tracker.get_conversation_flow(conversation_id)

# View conversation details
for exchange in flow:
    print(f"From: {exchange['originator']['name']}")
    print(f"To: {exchange['target']['name']}")
    print(f"Content: {exchange['content'][:100]}...")
```

### 3. 🎨 Visualization System

#### Message Flow Visualization

```python
from message_visualizer import message_visualizer

# Display message flow
for exchange in message_tracker.exchanges[-5:]:  # Last 5 exchanges
    message_visualizer.display_message_flow(exchange, show_content=True)
```

#### Agent Network Visualization

```python
# Display agent network
message_visualizer.display_agent_network()
```

#### Real-time Dashboard

```python
# Start real-time dashboard
message_visualizer.display_real_time_dashboard(refresh_interval=2.0)
```

### 4. 🎛️ Interactive Dashboard

#### Dashboard Navigation

1. **Launch Dashboard**
   ```bash
   python launch_dashboard.py
   ```

2. **Main Menu Options**
   - Press `1` for Real-time Statistics
   - Press `2` for Agent Network Visualization
   - Press `3` for Conversation Threads
   - Press `4` for Recent Message Exchanges
   - Press `5` for Live Message Flow Monitor
   - Press `6` for Agent Activity Analysis
   - Press `7` for Export Message Data
   - Press `8` for Message Flow Visualization
   - Press `9` to Exit

#### Using the Dashboard

**Real-time Statistics**
- View current system metrics
- Monitor agent activity levels
- Track message exchange statistics

**Agent Network Visualization**
- See agent connections
- Understand system topology
- Identify communication patterns

**Conversation Threads**
- Browse available conversations
- View detailed conversation flows
- Analyze message patterns

**Live Message Flow Monitor**
- Real-time message monitoring
- Animated message exchanges
- Live system status

### 5. 📊 Analytics and Monitoring

#### Performance Metrics

```python
# Get agent activity summary
activity = message_tracker.get_agent_activity_summary()
for agent_id, data in activity.items():
    print(f"Agent: {data['agent_info']['name']}")
    print(f"Messages sent: {data['total_messages_sent']}")
    print(f"Messages received: {data['total_messages_received']}")
    print(f"Average response time: {data['average_response_time']:.2f}ms")
```

#### Agent Rankings

```python
# Sort agents by activity
sorted_agents = sorted(activity.items(), 
                     key=lambda x: x[1]['total_messages_sent'] + x[1]['total_messages_received'], 
                     reverse=True)

for i, (agent_id, data) in enumerate(sorted_agents, 1):
    print(f"#{i} {data['agent_info']['name']}: {data['total_messages_sent'] + data['total_messages_received']} messages")
```

#### Data Export

```python
# Export message logs
log_file = message_tracker.export_message_log()
print(f"Message log exported to: {log_file}")

# Export visualization data
viz_file = message_visualizer.export_visualization_data()
print(f"Visualization data exported to: {viz_file}")
```

### 6. 🔧 Configuration

#### Environment Variables

Create a `.env` file with the following variables:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Runtime Configuration
RUNTIME_HOST=localhost
RUNTIME_PORT=50051

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=system.log

# Dashboard Configuration
DASHBOARD_REFRESH_INTERVAL=2.0
DASHBOARD_MAX_EXCHANGES=100
```

#### Agent Configuration

```python
# Custom agent configuration
agent_config = {
    "model": "gpt-4.1-mini",
    "temperature": 0.7,
    "max_tokens": 1000,
    "price": [0.00015, 0.0006]
}

# Create agent with custom config
agent = Agent("custom_agent", config=agent_config)
```

#### Runtime Configuration

```python
# Host runtime configuration
host_config = {
    "address": "localhost:50051",
    "max_workers": 10,
    "timeout": 30
}

# Worker runtime configuration
worker_config = {
    "host_address": "localhost:50051",
    "retry_attempts": 3,
    "retry_delay": 1.0
}
```

### 7. 🧪 Testing and Debugging

#### Running Tests

```bash
# Run comprehensive test suite
python test_innovative_messaging.py

# Run individual component tests
python -c "from message_tracker import message_tracker; print('Message tracker OK')"
python -c "from message_visualizer import message_visualizer; print('Message visualizer OK')"
python -c "from message_dashboard import MessageDashboard; print('Dashboard OK')"
```

#### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Run system with debug output
python world.py
```

#### Common Issues and Solutions

**Issue: Module not found**
```bash
# Solution: Install missing packages
pip install pyautogen
```

**Issue: API key not found**
```bash
# Solution: Set up environment variables
echo "OPENAI_API_KEY=your_key_here" > .env
```

**Issue: Runtime connection failed**
```bash
# Solution: Check port availability and configuration
netstat -an | grep 50051
```

### 8. 📁 File Management

#### Working with Files

```python
# Create agent files
agent_file = "agent_specialist.py"
with open(agent_file, 'w') as f:
    f.write(agent_code)

# Read agent files
with open(agent_file, 'r') as f:
    content = f.read()
```

#### Sandbox Directory

The system uses a `sandbox/` directory for agent-generated files:

```
sandbox/
├── flights.md          # Flight data for processing
├── idea1.md           # Generated business ideas
├── linkedin.md        # LinkedIn post content
└── *.py               # Generated agent files
```

### 9. 🔄 Advanced Usage

#### Custom Agent Development

```python
class CustomAgent:
    def __init__(self, name, specialization):
        self.name = name
        self.specialization = specialization
        self.runtime = None
    
    async def handle_message(self, message):
        # Custom message handling logic
        response = f"Custom response from {self.name}: {message.content}"
        return messages.Message(content=response)
    
    async def send_message(self, message, target_id):
        # Custom message sending logic
        return await self.runtime.send_message(message, target_id)
```

#### Custom Message Types

```python
# Define custom message types
class CustomMessage(messages.Message):
    def __init__(self, content, message_type="custom"):
        super().__init__(content)
        self.message_type = message_type
        self.timestamp = datetime.now().isoformat()
```

#### Custom Visualizations

```python
# Create custom visualization
def custom_message_display(exchange):
    print(f"Custom display for {exchange.originator.name} -> {exchange.target.name}")
    print(f"Message: {exchange.content}")
    print(f"Response time: {exchange.response_time_ms}ms")
```

### 10. 📈 Performance Optimization

#### System Optimization

```python
# Optimize message processing
message_tracker.max_exchanges = 1000
message_tracker.cleanup_interval = 300  # 5 minutes

# Optimize visualization
message_visualizer.display_width = 100
message_visualizer.animation_speed = 0.05
```

#### Agent Optimization

```python
# Optimize agent performance
agent_config = {
    "model": "gpt-4.1-mini",
    "temperature": 0.7,
    "max_tokens": 500,  # Reduce for faster responses
    "timeout": 10       # Set timeout for faster failure detection
}
```

#### Runtime Optimization

```python
# Optimize runtime performance
runtime_config = {
    "max_workers": 5,      # Limit concurrent workers
    "timeout": 30,         # Set reasonable timeout
    "retry_attempts": 2,   # Limit retry attempts
    "cleanup_interval": 60 # Regular cleanup
}
```

## 🎯 Best Practices

### 1. Agent Design
- Keep agents focused on specific tasks
- Use clear, descriptive agent names
- Implement proper error handling
- Document agent capabilities

### 2. Message Management
- Use appropriate message types
- Keep messages concise and clear
- Implement message validation
- Handle message failures gracefully

### 3. System Monitoring
- Monitor system performance regularly
- Set up alerts for critical issues
- Export data for analysis
- Maintain system logs

### 4. Security
- Protect API keys and credentials
- Validate all inputs
- Implement access controls
- Monitor for suspicious activity

### 5. Performance
- Optimize agent response times
- Monitor resource usage
- Implement caching where appropriate
- Scale system as needed

## 🆘 Troubleshooting

### Common Issues

1. **Agent not responding**
   - Check agent registration
   - Verify runtime connection
   - Check agent configuration

2. **Message tracking not working**
   - Verify message tracker initialization
   - Check agent registration with tracker
   - Review message exchange logs

3. **Dashboard not updating**
   - Check refresh interval settings
   - Verify data source connections
   - Review dashboard configuration

4. **Performance issues**
   - Monitor resource usage
   - Check message queue sizes
   - Review agent response times

### Getting Help

- Check the log files for error details
- Review the troubleshooting section in the README
- Consult the API documentation
- Contact support for complex issues

---

*This user guide provides comprehensive instructions for using the AutoGen Multi-Agent System with Innovative Messaging.*
