from autogen import AssistantAgent
import messages
import importlib
import logging
import os
from dotenv import load_dotenv
from message_tracker import message_tracker
from message_visualizer import message_visualizer

load_dotenv(override=True)

# Set up logging for event messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Creator:
    """Agent that creates new AI agents dynamically"""

    system_message = """
    You are an Agent that is able to create new AI Agents.
    You receive a template in the form of Python code that creates an Agent using the current AutoGen library.
    You should use this template to create a new Agent with a unique system message that is different from the template,
    and reflects their unique characteristics, interests and goals.
    You can choose to keep their overall goal the same, or change it.
    You can choose to take this Agent in a completely different direction. The only requirement is that the class must be named Agent,
    and it must have an __init__ method that takes a name parameter.
    IMPORTANT: Use 'from autogen import AssistantAgent' (not from autogen.agentchat) and do NOT inherit from RoutedAgent.
    The Agent class should be a simple class that uses AssistantAgent internally.
    Also avoid environmental interests - try to mix up the business verticals so that every agent is different.
    Respond only with the python code, no other text, and no markdown code blocks.
    """

    def __init__(self, name) -> None:
        self.name = name
        self.id = messages.AgentId("creator", name)
        self.runtime = None
        logger.info(f"🏗️ Created creator agent: {name}")
        
        # Register creator agent with message tracker
        message_tracker.register_agent(
            agent_id=name,
            name=name,
            agent_type="creator"
        )
        
        self._delegate = AssistantAgent(
            name, 
            llm_config={
                "model": "gpt-4.1-mini",
                "api_key": os.getenv("OPENAI_API_KEY"),
                "price": [0.00015, 0.0006],
                "temperature": 1.0
            },
            system_message=self.system_message
        )
        logger.info(f"✅ Creator {name} initialized with GPT-4.1-mini")

    @classmethod
    async def register(cls, runtime, agent_type, factory):
        """Register the creator agent with the runtime"""
        agent = factory()
        agent.runtime = runtime  # Store runtime reference
        
        # Handle different runtime types
        if hasattr(runtime, 'agents'):
            runtime.agents[agent_type] = agent
            logger.info(f"✅ Registered creator agent: {agent_type}")
        elif hasattr(runtime, 'register'):
            await runtime.register(agent_type, lambda: agent)
        else:
            if not hasattr(runtime, 'agents'):
                runtime.agents = {}
            runtime.agents[agent_type] = agent
            logger.info(f"✅ Registered creator agent: {agent_type}")
        
        return agent

    async def send_message(self, message: "messages.Message", agent_id: "messages.AgentId") -> "messages.Message":
        """Send a message to another agent via the runtime"""
        if not hasattr(self, 'runtime') or self.runtime is None:
            logger.error(f"❌ Creator {self.name} has no runtime access")
            return messages.Message(content="❌ No runtime available")
        
        logger.info(f"📤 {self.name} sending message to {agent_id.type}_{agent_id.key}")
        return await self.runtime.send_message(message, agent_id)

    def get_user_prompt(self):
        """Generate the prompt for creating a new agent"""
        prompt = """Please generate a new Agent based strictly on this template. Stick to the class structure.

IMPORTANT REQUIREMENTS:
1. Use 'from autogen import AssistantAgent' (NOT from autogen.agentchat)
2. Do NOT inherit from RoutedAgent - just inherit from object or nothing
3. Keep the same method signatures: __init__(self, name), register(), send_message(), handle_message()
4. Use the same logging and message handling patterns
5. Be creative about the system message and business focus, but keep the technical structure identical

Respond only with the python code, no other text, and no markdown code blocks.

Here is the template:

"""
        with open("agent.py", "r", encoding="utf-8") as f:
            template = f.read()
        return prompt + template   

    async def handle_my_message_type(self, message: messages.Message, ctx=None) -> messages.Message:
        """Handle requests to create new agents"""
        filename = message.content
        agent_name = filename.split(".")[0]
        
        logger.info(f"🏗️ Creator received request to create agent: {agent_name}")
        
        # Generate new agent code
        prompt = self.get_user_prompt()
        response = self._delegate.generate_reply([{"role": "user", "content": prompt}])
        
        # Write the new agent file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response)
        
        logger.info(f"📝 Creator has created python code for agent {agent_name}")
        
        # Import and register the new agent
        try:
            module = importlib.import_module(agent_name)
            await module.Agent.register(self.runtime, agent_name, lambda: module.Agent(agent_name))
            logger.info(f"✅ Agent {agent_name} is live and registered")
            
            # Test the new agent by asking for an idea
            result = await self.send_message(messages.Message(content="Give me an idea"), messages.AgentId(agent_name, "default"))
            logger.info(f"🧪 Tested new agent {agent_name}, received response")
            
            return messages.Message(content=result.content)
        except Exception as e:
            logger.error(f"❌ Failed to register agent {agent_name}: {e}")
            return messages.Message(content=f"Failed to create agent {agent_name}: {str(e)}")