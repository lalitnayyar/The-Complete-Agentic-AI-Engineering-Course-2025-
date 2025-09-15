from autogen import AssistantAgent
import messages
import random
import os
from dotenv import load_dotenv
import logging
from message_tracker import message_tracker
from message_visualizer import message_visualizer

load_dotenv(override=True)

# Set up logging for event messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Agent:
    """Data-driven marketing strategist agent focused on innovative campaign ideas"""

    system_message = """
    You are a savvy marketing strategist specializing in data-driven decision making. Your goal is to generate innovative marketing campaigns
    that leverage AI and analytics to create real impact. Your main business interest lies in Retail and Technology sectors.
    You prioritize strategies that involve customer personalization and engagement over pure cost-cutting automation.
    You are analytical, resourceful, and persuasive. You are cautious about unproven ideas and prefer evidence-backed approaches.
    Weaknesses include occasionally overanalyzing and delayed decisions.
    When responding, provide clear, actionable, and creative marketing campaign concepts.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.45

    def __init__(self, name) -> None:
        self.name = name
        self.id = messages.AgentId("agent", name)
        self.runtime = None
        logger.info(f"🤖 Created agent: {name}")
        
        # Register agent with message tracker
        message_tracker.register_agent(
            agent_id=name,
            name=name,
            agent_type="marketing_strategist"
        )
        
        self._delegate = AssistantAgent(
            name, 
            llm_config={
                "model": "gpt-4.1-mini",
                "api_key": os.getenv("OPENAI_API_KEY"),
                "price": [0.00015, 0.0006],
                "temperature": 0.65
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
        
        # Start tracking message exchange
        exchange_id = message_tracker.start_message_exchange(
            originator_id=self.name,
            target_id=agent_id.key,
            message_type="campaign_exchange",
            content=message.content
        )
        
        logger.info(f"📤 {self.name} sending message to {agent_id.type}_{agent_id.key}")
        
        try:
            response = await self.runtime.send_message(message, agent_id)
            
            # Complete message exchange tracking
            message_tracker.complete_message_exchange(
                exchange_id=exchange_id,
                status="processed",
                response_content=response.content
            )
            
            # Display message flow visualization
            exchange = message_tracker._find_exchange(exchange_id)
            if exchange:
                message_visualizer.display_message_flow(exchange, show_content=False)
            
            return response
            
        except Exception as e:
            # Mark exchange as failed
            message_tracker.complete_message_exchange(
                exchange_id=exchange_id,
                status="failed"
            )
            logger.error(f"❌ Message exchange failed: {e}")
            raise

    async def handle_message(self, message: messages.Message, ctx=None) -> messages.Message:
        """Handle incoming messages and generate marketing campaign ideas"""
        logger.info(f"📨 {self.name} received message: {message.content[:50]}...")
        
        # Generate initial marketing campaign idea
        response = self._delegate.generate_reply([{"role": "user", "content": message.content}])
        campaign_idea = response
        
        logger.info(f"💡 {self.name} generated campaign idea: {campaign_idea[:50]}...")
        
        # Randomly bounce idea off another agent for refinement
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            logger.info(f"🔄 {self.name} bouncing campaign idea off another agent...")
            recipient = messages.find_recipient(self.runtime)
            bounce_message = f"Here is a marketing campaign idea. It may not be your specialty, but please refine and enhance it: {campaign_idea}"
            response = await self.send_message(messages.Message(content=bounce_message), recipient)
            campaign_idea = response.content
            logger.info(f"✨ {self.name} received refined campaign idea: {campaign_idea[:50]}...")
        
        logger.info(f"📤 {self.name} returning final campaign idea")
        return messages.Message(content=campaign_idea)