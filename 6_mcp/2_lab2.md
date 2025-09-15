# Lab 2: MCP Server and Client - Flow of Events & Real-Time Analogies

## Table of Contents
1. [Overview](#overview)
2. [Flow of Events](#flow-of-events)
3. [Real-Time Analogies](#real-time-analogies)
4. [Code Walkthrough](#code-walkthrough)
5. [Key Concepts](#key-concepts)
6. [Troubleshooting](#troubleshooting)

---

## Overview

This lab demonstrates how to create and use MCP (Model Context Protocol) servers and clients. We'll build a financial account management system that can be accessed through different interfaces.

**What we're building:**
- An MCP Server that exposes account management tools
- An MCP Client that can interact with the server
- An Agent that uses these tools to manage accounts

---

## Flow of Events

### 1. **Initial Setup Phase**
```
User → Jupyter Notebook → Python Environment → Account System
```

**What happens:**
- Load environment variables
- Import necessary libraries
- Initialize the account system
- Create or retrieve an existing account

**Real-time analogy:** Like setting up your banking app on your phone - you need to log in, verify your identity, and connect to your bank's systems.

### 2. **Direct Account Operations Phase**
```
User → Account Object → Database/Storage → Response
```

**What happens:**
- Create account: `Account.get("Lalit")`
- Buy shares: `account.buy_shares("AMZN", 3, "rationale")`
- Get reports: `account.report()`
- List transactions: `account.list_transactions()`

**Real-time analogy:** Like using your bank's mobile app directly - you can check balance, transfer money, or view transaction history without talking to anyone.

### 3. **MCP Server Creation Phase**
```
Python Code → MCP Server Process → Tool Registration → Client Connection
```

**What happens:**
- Start MCP server process using `uv run accounts_server.py`
- Server registers available tools (get_balance, buy_shares, etc.)
- Server waits for client connections
- Client connects and discovers available tools

**Real-time analogy:** Like opening a customer service center - you set up the phone lines, train staff on available services, and wait for customers to call.

### 4. **MCP Client Interaction Phase**
```
Agent → MCP Client → MCP Server → Account System → Response
```

**What happens:**
- Agent receives user request
- Agent identifies which tools to use
- Client sends tool call to MCP server
- Server executes the operation
- Response flows back through the chain

**Real-time analogy:** Like calling customer service - you explain what you need, the representative uses their tools/systems to help you, and they provide the answer.

---

## Real-Time Analogies

### 🏦 **Banking System Analogy**

**MCP Server = Bank's Customer Service System**
- Has specific tools (check balance, transfer money, open account)
- Can only do what it's programmed to do
- Handles multiple requests simultaneously
- Provides standardized responses

**MCP Client = Your Banking App**
- Knows how to communicate with the bank's systems
- Translates your requests into the right format
- Handles the technical details of communication
- Presents results in a user-friendly way

**Agent = Personal Banking Assistant**
- Understands your natural language requests
- Decides which banking services to use
- Coordinates multiple operations if needed
- Provides personalized responses

### 🍕 **Restaurant Ordering System Analogy**

**MCP Server = Restaurant Kitchen System**
- Has specific tools (take order, check inventory, prepare food)
- Each tool has specific inputs and outputs
- Can handle multiple orders simultaneously
- Provides status updates

**MCP Client = Order Management App**
- Knows how to communicate with the kitchen
- Translates customer requests into kitchen instructions
- Tracks order status
- Handles payment processing

**Agent = Waiter/Order Taker**
- Understands customer requests in natural language
- Knows which kitchen tools to use for each request
- Can coordinate multiple items in an order
- Provides friendly, personalized service

### 🏠 **Smart Home System Analogy**

**MCP Server = Home Automation Hub**
- Has specific tools (turn on lights, adjust temperature, lock doors)
- Each tool controls specific devices
- Can handle multiple commands simultaneously
- Provides status feedback

**MCP Client = Home Control App**
- Knows how to communicate with the hub
- Translates user commands into device instructions
- Manages device states
- Provides real-time updates

**Agent = Smart Home Assistant**
- Understands voice commands and text requests
- Decides which devices to control
- Can coordinate multiple devices for scenes
- Provides personalized automation

---

## Code Walkthrough

### **Phase 1: Direct Account Management**
```python
# Create account directly
account = Account.get("Lalit")

# Use account methods directly
account.buy_shares("AMZN", 3, "Because this bookstore website looks promising")
account.report()
account.list_transactions()
```

**What's happening:**
- Direct object-oriented programming
- No network communication
- Immediate execution
- Synchronous operations

### **Phase 2: MCP Server Setup**
```python
# Start MCP server process
params = {"command": "uv", "args": ["run", "accounts_server.py"]}

# Connect to server
async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as server:
    mcp_tools = await server.list_tools()
```

**What's happening:**
- Process spawning (like starting a service)
- Inter-process communication
- Tool discovery
- Asynchronous operations

### **Phase 3: Agent with MCP Server**
```python
# Create agent with MCP server
agent = Agent(
    name="account_manager", 
    instructions=instructions, 
    model=model, 
    mcp_servers=[mcp_server]
)

# Run agent with user request
result = await Runner.run(agent, request)
```

**What's happening:**
- Natural language processing
- Tool selection and execution
- MCP protocol communication
- Response generation

### **Phase 4: MCP Client Implementation**
```python
# Get tools from MCP client
mcp_tools = await list_accounts_tools()
openai_tools = await get_accounts_tools_openai()

# Use tools with agent
agent = Agent(name="account_manager", instructions=instructions, model=model, tools=openai_tools)
result = await Runner.run(agent, request)
```

**What's happening:**
- Client-server architecture
- Tool abstraction
- Protocol translation
- Service integration

---

## Key Concepts

### **1. MCP Protocol**
- **Purpose:** Standardized way for AI systems to communicate with external tools
- **Benefits:** Interoperability, reusability, modularity
- **Components:** Servers, clients, tools, resources

### **2. Tool Registration**
- **Server Side:** Expose functions as callable tools
- **Client Side:** Discover and use available tools
- **Schema:** Define input/output formats

### **3. Asynchronous Operations**
- **Why:** Handle multiple operations simultaneously
- **How:** Use `async/await` patterns
- **Benefits:** Better performance, responsiveness

### **4. Agent Integration**
- **Natural Language:** Convert user requests to tool calls
- **Tool Selection:** Choose appropriate tools for tasks
- **Response Generation:** Create user-friendly responses

---

## Troubleshooting

### **Common Issues:**

1. **MCP Server Won't Start**
   - Check if `uv` is installed
   - Verify `accounts_server.py` exists
   - Check file permissions

2. **Connection Timeout**
   - Increase `client_session_timeout_seconds`
   - Check server process status
   - Verify network connectivity

3. **Tool Not Found**
   - Check tool registration
   - Verify server is running
   - Check tool names match

4. **Permission Denied**
   - Check file permissions
   - Verify user ownership
   - Check directory access

### **Debugging Steps:**

1. **Test Server Manually**
   ```bash
   uv run accounts_server.py
   ```

2. **Check Tool List**
   ```python
   tools = await server.list_tools()
   print([tool.name for tool in tools])
   ```

3. **Verify Connection**
   ```python
   async with MCPServerStdio(params=params) as server:
       print("Connected successfully")
   ```

---

## Real-World Applications

### **Financial Services**
- Portfolio management
- Trading systems
- Risk assessment
- Compliance reporting

### **E-commerce**
- Product management
- Order processing
- Inventory control
- Customer service

### **IoT Systems**
- Device control
- Sensor monitoring
- Automation rules
- Alert management

### **Content Management**
- Document processing
- Media management
- Publishing workflows
- Search and retrieval

---

## Best Practices

### **1. Error Handling**
- Always wrap MCP calls in try-catch blocks
- Provide meaningful error messages
- Implement retry logic for transient failures

### **2. Security**
- Validate all inputs
- Implement authentication
- Use secure communication channels
- Audit tool usage

### **3. Performance**
- Use connection pooling
- Implement caching where appropriate
- Monitor response times
- Optimize tool implementations

### **4. Monitoring**
- Log all tool calls
- Track success/failure rates
- Monitor resource usage
- Set up alerts for failures

---

## Conclusion

MCP provides a powerful way to extend AI systems with external capabilities. By understanding the flow of events and using real-world analogies, we can better grasp how these systems work and how to build robust, scalable solutions.

The key is to think of MCP as a standardized way for AI systems to "talk" to external services, much like how we use APIs to connect different applications in the real world.

---

*This guide covers the essential concepts and practical implementation of MCP servers and clients. For more advanced topics, refer to the official MCP documentation and community resources.*
