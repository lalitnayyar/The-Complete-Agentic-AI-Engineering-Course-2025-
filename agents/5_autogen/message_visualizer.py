#!/usr/bin/env python3
"""
Message Visualization System for Multi-Agent Communication
Provides real-time visualization of message flows and agent interactions
"""

import time
import json
from datetime import datetime
from typing import Dict, List, Any
import logging
from message_tracker import message_tracker, MessageExchange

logger = logging.getLogger(__name__)

class MessageVisualizer:
    """Real-time message flow visualization system"""
    
    def __init__(self):
        self.display_width = 80
        self.animation_speed = 0.1
        logger.info("🎨 Message Visualizer initialized")
    
    def display_message_flow(self, exchange: MessageExchange, show_content: bool = True):
        """Display a single message flow with visual effects"""
        print("\n" + "=" * self.display_width)
        print("📨 MESSAGE FLOW VISUALIZATION")
        print("=" * self.display_width)
        
        # Originator info
        print(f"👤 ORIGINATOR: {exchange.originator.name}")
        print(f"   🆔 ID: {exchange.originator.id}")
        print(f"   🏷️ Type: {exchange.originator.type}")
        print(f"   📊 Messages Sent: {exchange.originator.message_count}")
        print(f"   🕐 Last Seen: {exchange.originator.last_seen}")
        
        # Visual arrow with animation
        self._animate_arrow()
        
        # Target info
        print(f"🎯 TARGET: {exchange.target.name}")
        print(f"   🆔 ID: {exchange.target.id}")
        print(f"   🏷️ Type: {exchange.target.type}")
        print(f"   📊 Messages Received: {exchange.target.message_count}")
        print(f"   🕐 Last Seen: {exchange.target.last_seen}")
        
        # Message details
        print(f"\n📝 MESSAGE DETAILS:")
        print(f"   🏷️ Type: {exchange.message_type}")
        print(f"   📏 Length: {exchange.content_length} characters")
        print(f"   🕐 Timestamp: {exchange.timestamp}")
        print(f"   💬 Conversation: {exchange.conversation_id[:8]}")
        print(f"   📊 Status: {exchange.status}")
        
        if show_content and exchange.content:
            print(f"\n💬 CONTENT:")
            self._display_content(exchange.content)
        
        if exchange.response_time_ms > 0:
            print(f"\n⏱️ RESPONSE TIME: {exchange.response_time_ms:.2f}ms")
        
        print("=" * self.display_width)
    
    def display_conversation_thread(self, conversation_id: str, max_messages: int = 20):
        """Display a complete conversation thread"""
        exchanges = message_tracker.get_conversation_flow(conversation_id)
        if not exchanges:
            print(f"❌ No conversation found with ID: {conversation_id}")
            return
        
        print("\n" + "=" * self.display_width)
        print(f"💬 CONVERSATION THREAD: {conversation_id[:8]}")
        print("=" * self.display_width)
        
        # Show conversation summary
        print(f"📊 Total Messages: {len(exchanges)}")
        print(f"👥 Participants: {len(set(e['originator']['id'] for e in exchanges) | set(e['target']['id'] for e in exchanges))}")
        
        # Show message flow
        for i, exchange_data in enumerate(exchanges[-max_messages:], 1):
            print(f"\n📨 MESSAGE {i}:")
            print(f"   👤 {exchange_data['originator']['name']} → {exchange_data['target']['name']}")
            print(f"   🏷️ {exchange_data['message_type']} | {exchange_data['content_length']} chars")
            print(f"   🕐 {exchange_data['timestamp']} | ⏱️ {exchange_data['response_time_ms']:.2f}ms")
            print(f"   📊 Status: {exchange_data['status']}")
            
            if exchange_data['content']:
                content_preview = exchange_data['content'][:100] + "..." if len(exchange_data['content']) > 100 else exchange_data['content']
                print(f"   💬 {content_preview}")
        
        print("=" * self.display_width)
    
    def display_agent_network(self):
        """Display agent network visualization"""
        print("\n" + "=" * self.display_width)
        print("🕸️ AGENT NETWORK VISUALIZATION")
        print("=" * self.display_width)
        
        # Get all unique agents
        all_agents = set()
        for exchange in message_tracker.exchanges:
            all_agents.add(exchange.originator.id)
            all_agents.add(exchange.target.id)
        
        # Create network connections
        connections = {}
        for agent_id in all_agents:
            connections[agent_id] = set()
        
        for exchange in message_tracker.exchanges:
            connections[exchange.originator.id].add(exchange.target.id)
            connections[exchange.target.id].add(exchange.originator.id)
        
        # Display network
        for agent_id in all_agents:
            agent = message_tracker.agents.get(agent_id)
            agent_name = agent.name if agent else agent_id
            
            print(f"\n🤖 {agent_name} ({agent_id})")
            connected_agents = connections[agent_id]
            
            if connected_agents:
                print("   🔗 Connected to:")
                for connected_id in connected_agents:
                    connected_agent = message_tracker.agents.get(connected_id)
                    connected_name = connected_agent.name if connected_agent else connected_id
                    print(f"      • {connected_name} ({connected_id})")
            else:
                print("   🔗 No connections")
        
        print("=" * self.display_width)
    
    def display_real_time_dashboard(self, refresh_interval: float = 2.0):
        """Display real-time updating dashboard"""
        try:
            while True:
                # Clear screen (works on most terminals)
                print("\033[2J\033[H", end="")
                
                # Display dashboard
                dashboard = message_tracker.generate_message_dashboard()
                print(dashboard)
                
                # Display recent exchanges with visual effects
                print("\n🎬 LIVE MESSAGE FLOW:")
                print("-" * 40)
                recent_exchanges = sorted(message_tracker.exchanges, key=lambda x: x.timestamp, reverse=True)[:5]
                for exchange in recent_exchanges:
                    status_emoji = "✅" if exchange.status == "processed" else "⏳" if exchange.status == "sent" else "❌"
                    print(f"{status_emoji} {exchange.originator.name} → {exchange.target.name} "
                          f"[{exchange.message_type}] {exchange.response_time_ms:.1f}ms")
                
                print(f"\n🔄 Refreshing in {refresh_interval}s... (Ctrl+C to stop)")
                time.sleep(refresh_interval)
                
        except KeyboardInterrupt:
            print("\n👋 Dashboard stopped by user")
    
    def display_message_statistics(self):
        """Display detailed message statistics"""
        print("\n" + "=" * self.display_width)
        print("📊 MESSAGE STATISTICS")
        print("=" * self.display_width)
        
        stats = message_tracker.message_stats
        print(f"📈 Total Exchanges: {stats['total_exchanges']}")
        print(f"✅ Successful: {stats['successful_exchanges']}")
        print(f"❌ Failed: {stats['failed_exchanges']}")
        print(f"⏱️ Average Response Time: {stats['average_response_time']:.2f}ms")
        print(f"🔥 Most Active Agent: {stats['most_active_agent']}")
        print(f"💬 Longest Conversation: {stats['longest_conversation']} messages")
        
        # Agent-specific statistics
        print(f"\n👥 AGENT STATISTICS:")
        activity_summary = message_tracker.get_agent_activity_summary()
        for agent_id, data in activity_summary.items():
            agent = data['agent_info']
            print(f"\n🤖 {agent['name']} ({agent['type']}):")
            print(f"   📤 Messages Sent: {data['total_messages_sent']}")
            print(f"   📥 Messages Received: {data['total_messages_received']}")
            print(f"   ⏱️ Avg Response Time: {data['average_response_time']:.2f}ms")
            print(f"   💬 Conversations: {data['conversation_count']}")
            print(f"   🕐 Last Active: {data['last_activity']}")
        
        print("=" * self.display_width)
    
    def _animate_arrow(self):
        """Animate arrow for visual effect"""
        arrow_steps = ["→", "→", "→", "→", "→"]
        for step in arrow_steps:
            print(f"   {step}", end="", flush=True)
            time.sleep(self.animation_speed)
        print()
    
    def _display_content(self, content: str, max_width: int = 70):
        """Display content with proper wrapping"""
        words = content.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= max_width:
                current_line += " " + word if current_line else word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        for line in lines:
            print(f"   {line}")
    
    def export_visualization_data(self, filename: str = None) -> str:
        """Export visualization data to file"""
        if filename is None:
            filename = f"message_visualization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        visualization_data = {
            "export_timestamp": datetime.now().isoformat(),
            "agent_network": self._get_agent_network_data(),
            "conversation_flows": self._get_conversation_flows_data(),
            "statistics": message_tracker.message_stats
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(visualization_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📁 Visualization data exported to: {filename}")
        return filename
    
    def _get_agent_network_data(self) -> Dict[str, Any]:
        """Get agent network data for export"""
        all_agents = set()
        for exchange in message_tracker.exchanges:
            all_agents.add(exchange.originator.id)
            all_agents.add(exchange.target.id)
        
        connections = {}
        for agent_id in all_agents:
            connections[agent_id] = set()
        
        for exchange in message_tracker.exchanges:
            connections[exchange.originator.id].add(exchange.target.id)
            connections[exchange.target.id].add(exchange.originator.id)
        
        return {
            "agents": {aid: message_tracker.agents[aid].__dict__ for aid in all_agents if aid in message_tracker.agents},
            "connections": {aid: list(conns) for aid, conns in connections.items()}
        }
    
    def _get_conversation_flows_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get conversation flows data for export"""
        flows = {}
        for conversation_id in message_tracker.conversations:
            flows[conversation_id] = message_tracker.get_conversation_flow(conversation_id)
        return flows

# Global visualizer instance
message_visualizer = MessageVisualizer()
