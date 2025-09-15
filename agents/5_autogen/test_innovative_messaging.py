#!/usr/bin/env python3
"""
Test script for the innovative messaging system
Demonstrates detailed message tracking and visualization
"""

import asyncio
import time
from message_tracker import message_tracker
from message_visualizer import message_visualizer
from agent import Agent
from creator import Creator
from world import GrpcWorkerAgentRuntime, GrpcWorkerAgentRuntimeHost
import messages
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_innovative_messaging():
    """Test the innovative messaging system with detailed tracking"""
    print("🚀 Testing Innovative Messaging System")
    print("=" * 60)
    
    # Create runtime
    host = GrpcWorkerAgentRuntimeHost(address="localhost:50051")
    host.start()
    
    worker = GrpcWorkerAgentRuntime(host_address="localhost:50051")
    await worker.start()
    
    # Create and register agents
    print("\n🤖 Creating and registering agents...")
    
    # Register creator
    creator = await Creator.register(worker, "Creator", lambda: Creator("Creator"))
    creator_id = messages.AgentId("Creator", "default")
    
    # Create a few test agents
    agent1 = await Agent.register(worker, "agent1", lambda: Agent("agent1"))
    agent2 = await Agent.register(worker, "agent2", lambda: Agent("agent2"))
    agent3 = await Agent.register(worker, "agent3", lambda: Agent("agent3"))
    
    print(f"✅ Created {len(message_tracker.agents)} agents")
    
    # Test message exchanges
    print("\n📨 Testing message exchanges...")
    
    # Test 1: Creator creates an agent
    print("\n🧪 Test 1: Creator creates agent")
    result1 = await worker.send_message(messages.Message(content="agent_test.py"), creator_id)
    print(f"✅ Creator test completed")
    
    # Test 2: Agent-to-agent communication
    print("\n🧪 Test 2: Agent-to-agent communication")
    agent1_id = messages.AgentId("agent1", "default")
    agent2_id = messages.AgentId("agent2", "default")
    
    # Send message from agent1 to agent2
    message = messages.Message(content="Generate a business idea for a healthcare startup")
    response = await worker.send_message(message, agent1_id)
    print(f"✅ Agent communication test completed")
    
    # Test 3: Multiple agent interactions
    print("\n🧪 Test 3: Multiple agent interactions")
    for i in range(3):
        agent_id = messages.AgentId(f"agent{(i % 3) + 1}", "default")
        message = messages.Message(content=f"Test message {i+1} for multi-agent interaction")
        response = await worker.send_message(message, agent_id)
        time.sleep(0.5)  # Small delay to see the flow
    
    print(f"✅ Multi-agent interaction test completed")
    
    # Display comprehensive dashboard
    print("\n" + "=" * 80)
    print("📊 COMPREHENSIVE MESSAGE DASHBOARD")
    print("=" * 80)
    
    dashboard = message_tracker.generate_message_dashboard()
    print(dashboard)
    
    # Display agent network
    print("\n🕸️ AGENT NETWORK VISUALIZATION")
    message_visualizer.display_agent_network()
    
    # Display message statistics
    print("\n📈 DETAILED MESSAGE STATISTICS")
    message_visualizer.display_message_statistics()
    
    # Display recent message flows
    print("\n🎬 RECENT MESSAGE FLOWS")
    recent_exchanges = sorted(message_tracker.exchanges, key=lambda x: x.timestamp, reverse=True)[:3]
    for i, exchange in enumerate(recent_exchanges, 1):
        print(f"\n📨 MESSAGE FLOW #{i}:")
        message_visualizer.display_message_flow(exchange, show_content=True)
        time.sleep(1)
    
    # Export data
    print("\n📁 EXPORTING MESSAGE DATA...")
    log_file = message_tracker.export_message_log()
    viz_file = message_visualizer.export_visualization_data()
    print(f"✅ Message log exported to: {log_file}")
    print(f"✅ Visualization data exported to: {viz_file}")
    
    # Cleanup
    await worker.stop()
    await host.stop()
    
    print("\n🎉 Innovative messaging system test completed successfully!")
    print(f"📊 Total message exchanges tracked: {message_tracker.message_stats['total_exchanges']}")
    print(f"👥 Total agents registered: {len(message_tracker.agents)}")
    print(f"💬 Total conversations: {len(message_tracker.conversations)}")

if __name__ == "__main__":
    asyncio.run(test_innovative_messaging())
