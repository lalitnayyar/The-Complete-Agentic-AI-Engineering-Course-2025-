from dataclasses import dataclass
import glob
import os
import random
import logging

# Set up logging for event messages
logger = logging.getLogger(__name__)

class AgentId:
    """Agent identifier for routing messages"""
    def __init__(self, agent_type: str, key: str):
        self.type = agent_type
        self.key = key
    
    def __str__(self):
        return f"{self.type}_{self.key}"

@dataclass
class Message:
    content: str

def find_recipient(runtime=None) -> AgentId:
    """Find a random agent to bounce ideas off of"""
    try:
        # If runtime is provided, use the registered agents
        if runtime and hasattr(runtime, 'agents'):
            available_agents = list(runtime.agents.keys())
            # Filter out the creator agent
            available_agents = [name for name in available_agents if name != "Creator"]
            
            if available_agents:
                agent_name = random.choice(available_agents)
                logger.info(f"🎯 Selecting registered agent for refinement: {agent_name}")
                return AgentId(agent_name, "default")
        
        # Fallback: get agents from files (for backward compatibility)
        agent_files = glob.glob("agent*.py")
        agent_names = [os.path.splitext(file)[0] for file in agent_files]
        
        # Remove the base "agent" file if it exists
        if "agent" in agent_names:
            agent_names.remove("agent")
        
        # Filter out agents that are just files but not yet registered
        # Only include agents that have been created and are likely registered
        available_agents = []
        for name in agent_names:
            # Check if this looks like a numbered agent (agent1, agent2, etc.)
            if name.startswith("agent") and name[5:].isdigit():
                available_agents.append(name)
        
        if not available_agents:
            logger.warning("⚠️ No registered agents found, using default agent1")
            return AgentId("agent1", "default")
        
        agent_name = random.choice(available_agents)
        logger.info(f"🎯 Selecting agent for refinement: {agent_name}")
        return AgentId(agent_name, "default")
    except Exception as e:
        logger.error(f"❌ Exception finding recipient: {e}")
        return AgentId("agent1", "default")
