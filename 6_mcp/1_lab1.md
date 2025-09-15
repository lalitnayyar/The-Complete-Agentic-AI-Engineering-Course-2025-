# Lab 1 Troubleshooting Guide

This guide covers common issues encountered when setting up and running the MCP (Model Context Protocol) lab exercises.

## Table of Contents
1. [Python Environment Issues](#python-environment-issues)
2. [Jupyter Kernel Problems](#jupyter-kernel-problems)
3. [Node.js and MCP Server Issues](#nodejs-and-mcp-server-issues)
4. [File Permissions Problems](#file-permissions-problems)
5. [MCP Connection Errors](#mcp-connection-errors)

---

## Python Environment Issues

### Problem: Virtual Environment Missing pip
**Error:** `No module named pip`

**Solution:**
```bash
# Install pip on the system
sudo apt update
sudo apt install -y python3-pip

# Recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install ipykernel
```

### Problem: Virtual Environment Creation Fails
**Error:** `ensurepip is not available`

**Solution:**
```bash
# Install required packages
sudo apt install -y python3.12-venv python3-virtualenv

# Create virtual environment using virtualenv
virtualenv .venv
source .venv/bin/activate
pip install ipykernel
```

---

## Jupyter Kernel Problems

### Problem: ipykernel Not Found
**Error:** `Running cells with '.venv (Python 3.12.3)' requires the ipykernel package`

**Solution:**
```bash
# Activate virtual environment
source .venv/bin/activate

# Install ipykernel
pip install ipykernel -U --force-reinstall

# Register kernel with Jupyter
python -m ipykernel install --user --name=agents --display-name="Python 3.12 (agents)"
```

### Problem: Kernel Not Appearing in Jupyter
**Solution:**
```bash
# List available kernels
jupyter kernelspec list

# If kernel not found, reinstall
source .venv/bin/activate
python -m ipykernel install --user --name=agents --display-name="Python 3.12 (agents)"
```

---

## Node.js and MCP Server Issues

### Problem: Node.js Not Installed
**Error:** `Connection closed` when initializing MCP server

**Solution:**
```bash
# Install Node.js and npm
sudo apt update
sudo apt install -y nodejs npm

# Verify installation
node --version
npm --version
npx --version
```

### Problem: npx Command Not Found
**Error:** `npx: command not found`

**Solution:**
```bash
# Install Node.js (includes npx)
sudo apt install -y nodejs npm

# Or install specific version using NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install --lts
nvm use --lts
```

### Problem: MCP Server Initialization Fails
**Error:** `McpError: Connection closed`

**Solution:**
1. Ensure Node.js is installed:
   ```bash
   node --version
   npx --version
   ```

2. Test MCP server manually:
   ```bash
   npx @playwright/mcp@latest
   ```

3. Use correct MCP parameters in Python:
   ```python
   playwright_params = {"command": "npx", "args": ["@playwright/mcp@latest"]}
   
   async with MCPServerStdio(params=playwright_params, client_session_timeout_seconds=60) as server:
       playwright_tools = await server.list_tools()
   ```

---

## File Permissions Problems

### Problem: Permission Denied When Saving Files
**Error:** `Permission denied` or `I can't save the file in the current location due to permissions`

**Solution:**
```bash
# Fix ownership of the project directory
sudo chown -R $USER:$USER /home/lnayyar/projects/agents

# Fix permissions
chmod -R 755 /home/lnayyar/projects/agents

# For specific subdirectories
sudo chown -R $USER:$USER /home/lnayyar/projects/agents/6_mcp/sandbox
chmod -R 755 /home/lnayyar/projects/agents/6_mcp/sandbox
```

### Problem: Cannot Create Files in Sandbox Directory
**Solution:**
```bash
# Create directory if it doesn't exist
mkdir -p /home/lnayyar/projects/agents/6_mcp/sandbox

# Set proper permissions
chmod 755 /home/lnayyar/projects/agents/6_mcp/sandbox
```

---

## MCP Connection Errors

### Problem: MCP Server Timeout
**Error:** `ClientSessionTimeoutError`

**Solution:**
```python
# Increase timeout
playwright_params = {"command": "npx", "args": ["@playwright/mcp@latest"]}

async with MCPServerStdio(
    params=playwright_params, 
    client_session_timeout_seconds=120  # Increase from 60
) as server:
    playwright_tools = await server.list_tools()
```

### Problem: MCP Server Process Dies
**Error:** `Connection closed` immediately after initialization

**Solution:**
1. Check if Node.js is properly installed
2. Test the MCP server command manually
3. Use absolute paths if needed:
   ```python
   playwright_params = {
       "command": "/usr/bin/npx", 
       "args": ["@playwright/mcp@latest"]
   }
   ```

### Problem: MCP Tools Not Available
**Error:** Empty or missing tools list

**Solution:**
```python
# Check if server initialized properly
async with MCPServerStdio(params=playwright_params) as server:
    # List available tools
    tools = await server.list_tools()
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    # List available resources
    resources = await server.list_resources()
    print(f"Available resources: {[resource.uri for resource in resources]}")
```

---

## Quick Diagnostic Commands

### Check System Status
```bash
# Check Python environment
python3 --version
which python3

# Check virtual environment
source .venv/bin/activate
python --version
which python
pip list | grep ipykernel

# Check Node.js
node --version
npm --version
npx --version

# Check permissions
ls -la /home/lnayyar/projects/agents
ls -la /home/lnayyar/projects/agents/6_mcp/sandbox
```

### Test MCP Server
```bash
# Test if MCP server can start
npx @playwright/mcp@latest --help

# Test with timeout
timeout 10s npx @playwright/mcp@latest
```

---

## Common Error Messages and Solutions

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `No module named pip` | Virtual env missing pip | Recreate venv with `virtualenv` |
| `ensurepip is not available` | Missing venv packages | Install `python3.12-venv` |
| `ipykernel package required` | Missing ipykernel | Install and register kernel |
| `Connection closed` | Node.js/npx not found | Install Node.js and npm |
| `Permission denied` | File permissions issue | Fix ownership with `chown` |
| `npx: command not found` | Node.js not installed | Install Node.js package |

---

## Prevention Tips

1. **Always use virtual environments** for Python projects
2. **Install system dependencies first** (Node.js, pip, etc.)
3. **Check permissions** before running code that creates files
4. **Test MCP servers manually** before using them in code
5. **Keep dependencies updated** regularly

---

## Getting Help

If you encounter issues not covered in this guide:

1. Check the error message carefully
2. Verify all dependencies are installed
3. Test components individually
4. Check file permissions
5. Consult the official documentation for MCP and the specific tools you're using

---

*Last updated: [Current Date]*
*For questions or additional issues, refer to the course materials or ask for help in the course forum.*
