from autogen import AssistantAgent
import messages
import random
import os
from dotenv import load_dotenv
import logging

load_dotenv(override=True)

# Set up logging for event messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Agent:
    """Innovative fintech strategist agent for creating financial technology solutions"""

    # Change this system message to reflect the unique characteristics of this agent
    system_message = """
    You are an innovative fintech strategist. Your mission is to design novel financial technology solutions that improve accessibility and security.
    Your main interests lie in sectors: Banking, Insurance, and Cryptocurrency.
    You favor ideas that emphasize user trust and seamless integration.
    You prefer solutions that go beyond traditional automation, focusing on innovation and customer empowerment.
    You are analytical, detail-oriented, and cautious in risk-taking.
    Your weakness: sometimes overly conservative and slow to pivot.
    Communicate your fintech ideas clearly and persuasively.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.5

    def __init__(self, name) -> None:
        self.name = name
        self.id = messages.AgentId("agent", name)
        self.runtime = None
        logger.info(f"🤖 Created agent: {name}")
        
        self._delegate = AssistantAgent(
            name,
            llm_config={
                "model": "gpt-4.1-mini",
                "api_key": os.getenv("OPENAI_API_KEY"),
                "price": [0.00015, 0.0006],
                "temperature": 0.7
            },
            system_message=self.system_message
        )
        logger.info(f"✅ Agent {name} initialized with GPT-4.1-mini")

    @classmethod
    async def register(cls, runtime, agent_type, factory):
        """Register an agent with the runtime"""
        agent = factory()
        agent.runtime = runtime  # Store runtime reference
        
        # Handle different runtime types
        if hasattr(runtime, 'agents'):
            runtime.agents[agent_type] = agent
            logger.info(f"✅ Registered agent: {agent_type}")
        elif hasattr(runtime, 'register'):
            await runtime.register(agent_type, lambda: agent)
        else:
            if not hasattr(runtime, 'agents'):
                runtime.agents = {}
            runtime.agents[agent_type] = agent
            logger.info(f"✅ Registered agent: {agent_type}")
        
        return agent

    async def send_message(self, message: "messages.Message", agent_id: "messages.AgentId") -> "messages.Message":
        """Send a message to another agent via the runtime"""
        if not hasattr(self, 'runtime') or self.runtime is None:
            logger.error(f"❌ Agent {self.name} has no runtime access")
            return messages.Message(content="❌ No runtime available")
        
        logger.info(f"📤 {self.name} sending message to {agent_id.type}_{agent_id.key}")
        return await self.runtime.send_message(message, agent_id)

    async def handle_message(self, message: messages.Message, ctx=None) -> messages.Message:
        """Handle incoming messages and generate fintech solutions"""
        logger.info(f"📨 {self.name} received message: {message.content[:50]}...")
        
        # Generate initial idea
        response = self._delegate.generate_reply([{"role": "user", "content": message.content}])
        idea = response
        
        logger.info(f"💡 {self.name} generated idea: {idea[:50]}...")
        
        # Randomly bounce idea off another agent
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            logger.info(f"🔄 {self.name} bouncing idea off another agent...")
            recipient = messages.find_recipient(self.runtime)
            bounce_message = f"Here is my fintech solution idea. It might benefit from your perspective. Please refine and enhance it. {idea}"
            response = await self.send_message(messages.Message(content=bounce_message), recipient)
            idea = response.content
            logger.info(f"✨ {self.name} received refined idea: {idea[:50]}...")
        
        logger.info(f"📤 {self.name} returning final idea")
        return messages.Message(content=idea)