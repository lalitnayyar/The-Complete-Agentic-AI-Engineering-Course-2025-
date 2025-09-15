from agent import Agent
from creator import Creator
import messages
import asyncio
import logging
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# Set up logging for event messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

HOW_MANY_AGENTS = 20

class GrpcWorkerAgentRuntimeHost:
    """Simulated GRPC Worker Agent Runtime Host for demonstration"""
    def __init__(self, address: str):
        self.address = address
        self.agents = {}
        self.running = False
        logger.info(f"🌐 Created distributed runtime host at {address}")
    
    def start(self):
        """Start the distributed runtime host"""
        self.running = True
        logger.info(f"🚀 Distributed runtime host started at {self.address}")
        logger.info("📡 Ready to accept agent registrations and messages")
    
    async def stop(self):
        """Stop the distributed runtime host"""
        self.running = False
        logger.info("⏹️ Distributed runtime host stopped")
    
    async def register_agent(self, agent_type: str, agent_factory):
        """Register an agent with the distributed runtime"""
        agent = agent_factory()
        self.agents[agent_type] = agent
        logger.info(f"✅ Registered agent: {agent_type}")
        return agent
    
    def register_agent_from_worker(self, agent_type: str, agent):
        """Register an agent from a worker runtime"""
        self.agents[agent_type] = agent
        logger.info(f"✅ Host registered agent from worker: {agent_type}")
    
    async def send_message(self, message, agent_id):
        """Send a message to a specific agent in the distributed runtime"""
        if not self.running:
            logger.warning("⚠️ Distributed runtime not started")
            return message
        
        agent_key = f"{agent_id.type}_{agent_id.key}" if hasattr(agent_id, 'type') else str(agent_id)
        agent = self.agents.get(agent_key)
        
        if not agent:
            logger.error(f"❌ Agent {agent_key} not found in distributed runtime")
            return messages.Message(content=f"Agent {agent_key} not found")
        
        logger.info(f"📨 Distributed message sent to {agent_key}: {message.content[:50]}...")
        
        # Create message context
        ctx = messages.MessageContext() if hasattr(messages, 'MessageContext') else None
        
        # Find and call the appropriate message handler
        if hasattr(agent, 'handle_my_message_type'):
            response = await agent.handle_my_message_type(message, ctx)
        elif hasattr(agent, 'handle_message'):
            response = await agent.handle_message(message, ctx)
        else:
            response = messages.Message(content=f"Distributed agent {agent.name} received: {message.content}")
        
        logger.info(f"📤 Distributed response from {agent_key}: {response.content[:50]}...")
        return response

class GrpcWorkerAgentRuntime:
    """Simulated GRPC Worker Agent Runtime for demonstration"""
    def __init__(self, host_address: str):
        self.host_address = host_address
        self.agents = {}
        self.running = False
        logger.info(f"🔧 Created worker runtime connecting to {host_address}")
    
    async def start(self):
        """Start the worker runtime"""
        self.running = True
        logger.info(f"🚀 Worker runtime started, connected to {self.host_address}")
    
    async def stop(self):
        """Stop the worker runtime"""
        self.running = False
        logger.info("⏹️ Worker runtime stopped")
    
    async def register(self, agent_type: str, agent_factory, host=None):
        """Register an agent with the worker runtime"""
        agent = agent_factory()
        self.agents[agent_type] = agent
        logger.info(f"✅ Worker registered agent: {agent_type}")
        
        # Also register with host if provided
        if host:
            host.register_agent_from_worker(agent_type, agent)
        
        return agent
    
    async def send_message(self, message, agent_id):
        """Send a message to a specific agent in the worker runtime"""
        if not self.running:
            logger.warning("⚠️ Worker runtime not started")
            return message
        
        # Try different key formats for agent lookup
        agent_key = f"{agent_id.type}_{agent_id.key}" if hasattr(agent_id, 'type') else str(agent_id)
        agent = self.agents.get(agent_key)
        
        # If not found, try just the type (for cases where agent is registered by type only)
        if not agent:
            agent = self.agents.get(agent_id.type)
        
        # If still not found, try just the key
        if not agent:
            agent = self.agents.get(agent_id.key)
        
        # Debug: Print available agents
        if not agent:
            logger.error(f"❌ Agent {agent_key} not found in worker runtime")
            logger.info(f"Available agents: {list(self.agents.keys())}")
            logger.info(f"Looking for: type='{agent_id.type}', key='{agent_id.key}'")
            return messages.Message(content=f"Agent {agent_key} not found")
        
        logger.info(f"📨 Worker message sent to {agent_key}: {message.content[:50]}...")
        
        # Create message context
        ctx = messages.MessageContext() if hasattr(messages, 'MessageContext') else None
        
        # Find and call the appropriate message handler
        if hasattr(agent, 'handle_my_message_type'):
            response = await agent.handle_my_message_type(message, ctx)
        elif hasattr(agent, 'handle_message'):
            response = await agent.handle_message(message, ctx)
        else:
            response = messages.Message(content=f"Worker agent {agent.name} received: {message.content}")
        
        logger.info(f"📤 Worker response from {agent_key}: {response.content[:50]}...")
        return response

async def create_and_message(worker, creator_id, i: int):
    """Create a new agent and get an idea from it"""
    try:
        logger.info(f"🏗️ Creating agent {i}...")
        result = await worker.send_message(messages.Message(content=f"agent{i}.py"), creator_id)
        
        # Save the idea to a file
        with open(f"idea{i}.md", "w", encoding="utf-8") as f:
            f.write(result.content)
        
        logger.info(f"💾 Saved idea {i} to idea{i}.md")
    except Exception as e:
        logger.error(f"❌ Failed to create agent {i} due to exception: {e}")

async def main():
    """Main function to orchestrate agent creation"""
    logger.info("🌍 Starting World - Multi-Agent Creation System")
    logger.info(f"🎯 Target: Create {HOW_MANY_AGENTS} agents")
    
    # Create and start the distributed runtime host
    host = GrpcWorkerAgentRuntimeHost(address="localhost:50051")
    host.start() 
    
    # Create and start the worker runtime
    worker = GrpcWorkerAgentRuntime(host_address="localhost:50051")
    await worker.start()
    
    # Register the creator agent
    logger.info("🏗️ Registering Creator agent...")
    result = await Creator.register(worker, "Creator", lambda: Creator("Creator"))
    creator_id = messages.AgentId("Creator", "default")
    
    # Create all agents concurrently
    logger.info(f"🚀 Starting creation of {HOW_MANY_AGENTS} agents...")
    coroutines = [create_and_message(worker, creator_id, i) for i in range(1, HOW_MANY_AGENTS+1)]
    await asyncio.gather(*coroutines)
    
    logger.info("✅ All agents created successfully!")
    
    # Cleanup
    try:
        await worker.stop()
        await host.stop()
        logger.info("🧹 Cleanup completed")
    except Exception as e:
        logger.error(f"❌ Error during cleanup: {e}")

if __name__ == "__main__":
    asyncio.run(main())


