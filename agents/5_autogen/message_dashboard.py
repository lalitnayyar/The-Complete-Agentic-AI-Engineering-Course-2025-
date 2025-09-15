#!/usr/bin/env python3
"""
Interactive Message Dashboard for Multi-Agent System
Provides real-time monitoring and analysis of agent communications
"""

import asyncio
import time
import json
from datetime import datetime
from message_tracker import message_tracker
from message_visualizer import message_visualizer
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MessageDashboard:
    """Interactive message dashboard for monitoring agent communications"""
    
    def __init__(self):
        self.running = False
        logger.info("🎛️ Message Dashboard initialized")
    
    def display_main_menu(self):
        """Display the main dashboard menu"""
        print("\n" + "=" * 80)
        print("🎛️ MULTI-AGENT MESSAGE DASHBOARD")
        print("=" * 80)
        print("1. 📊 Real-time Statistics")
        print("2. 🕸️ Agent Network Visualization")
        print("3. 💬 Conversation Threads")
        print("4. 📨 Recent Message Exchanges")
        print("5. 🔄 Live Message Flow Monitor")
        print("6. 📈 Agent Activity Analysis")
        print("7. 📁 Export Message Data")
        print("8. 🎨 Message Flow Visualization")
        print("9. ❌ Exit")
        print("=" * 80)
    
    def display_real_time_stats(self):
        """Display real-time statistics"""
        print("\n" + "=" * 80)
        print("📊 REAL-TIME MESSAGE STATISTICS")
        print("=" * 80)
        
        stats = message_tracker.message_stats
        print(f"📈 Total Message Exchanges: {stats['total_exchanges']}")
        print(f"✅ Successful Exchanges: {stats['successful_exchanges']}")
        print(f"❌ Failed Exchanges: {stats['failed_exchanges']}")
        print(f"⏱️ Average Response Time: {stats['average_response_time']:.2f}ms")
        print(f"🔥 Most Active Agent: {stats['most_active_agent']}")
        print(f"💬 Longest Conversation: {stats['longest_conversation']} messages")
        
        # Agent activity breakdown
        print(f"\n👥 AGENT ACTIVITY BREAKDOWN:")
        activity_summary = message_tracker.get_agent_activity_summary()
        for agent_id, data in activity_summary.items():
            agent = data['agent_info']
            print(f"   🤖 {agent['name']} ({agent['type']}):")
            print(f"      📤 Sent: {data['total_messages_sent']} | 📥 Received: {data['total_messages_received']}")
            print(f"      ⏱️ Avg Response: {data['average_response_time']:.2f}ms")
            print(f"      💬 Conversations: {data['conversation_count']}")
    
    def display_agent_network(self):
        """Display agent network visualization"""
        message_visualizer.display_agent_network()
    
    def display_conversation_threads(self):
        """Display available conversation threads"""
        print("\n" + "=" * 80)
        print("💬 CONVERSATION THREADS")
        print("=" * 80)
        
        if not message_tracker.conversations:
            print("❌ No conversations found")
            return
        
        print(f"📊 Total Conversations: {len(message_tracker.conversations)}")
        print("\n🔍 Available Conversations:")
        
        for i, (conversation_id, exchange_ids) in enumerate(message_tracker.conversations.items(), 1):
            print(f"   {i}. 💬 {conversation_id[:8]}... ({len(exchange_ids)} messages)")
        
        # Allow user to select a conversation
        try:
            choice = input(f"\n🎯 Select conversation (1-{len(message_tracker.conversations)}) or 0 to go back: ")
            if choice == "0":
                return
            
            conversation_index = int(choice) - 1
            if 0 <= conversation_index < len(message_tracker.conversations):
                conversation_id = list(message_tracker.conversations.keys())[conversation_index]
                message_visualizer.display_conversation_thread(conversation_id)
            else:
                print("❌ Invalid selection")
        except (ValueError, IndexError):
            print("❌ Invalid input")
    
    def display_recent_exchanges(self):
        """Display recent message exchanges"""
        print("\n" + "=" * 80)
        print("📨 RECENT MESSAGE EXCHANGES")
        print("=" * 80)
        
        recent_exchanges = sorted(message_tracker.exchanges, key=lambda x: x.timestamp, reverse=True)
        
        if not recent_exchanges:
            print("❌ No message exchanges found")
            return
        
        print(f"📊 Total Exchanges: {len(recent_exchanges)}")
        print(f"🔍 Showing last 10 exchanges:\n")
        
        for i, exchange in enumerate(recent_exchanges[:10], 1):
            status_emoji = "✅" if exchange.status == "processed" else "⏳" if exchange.status == "sent" else "❌"
            print(f"{i:2d}. {status_emoji} {exchange.originator.name} → {exchange.target.name}")
            print(f"    🏷️ {exchange.message_type} | {exchange.content_length} chars | {exchange.response_time_ms:.2f}ms")
            print(f"    🕐 {exchange.timestamp} | 💬 {exchange.conversation_id[:8]}")
            print(f"    💬 {exchange.content[:100]}{'...' if len(exchange.content) > 100 else ''}")
            print()
    
    def start_live_monitor(self):
        """Start live message flow monitoring"""
        print("\n" + "=" * 80)
        print("🔄 LIVE MESSAGE FLOW MONITOR")
        print("=" * 80)
        print("🔄 Starting live monitor... (Press Ctrl+C to stop)")
        print("=" * 80)
        
        try:
            message_visualizer.display_real_time_dashboard(refresh_interval=2.0)
        except KeyboardInterrupt:
            print("\n👋 Live monitor stopped")
    
    def display_agent_analysis(self):
        """Display detailed agent activity analysis"""
        print("\n" + "=" * 80)
        print("📈 AGENT ACTIVITY ANALYSIS")
        print("=" * 80)
        
        activity_summary = message_tracker.get_agent_activity_summary()
        
        if not activity_summary:
            print("❌ No agent activity data available")
            return
        
        # Sort agents by total activity
        sorted_agents = sorted(activity_summary.items(), 
                             key=lambda x: x[1]['total_messages_sent'] + x[1]['total_messages_received'], 
                             reverse=True)
        
        print("🏆 AGENT RANKINGS BY ACTIVITY:")
        print("-" * 40)
        
        for i, (agent_id, data) in enumerate(sorted_agents, 1):
            agent = data['agent_info']
            total_activity = data['total_messages_sent'] + data['total_messages_received']
            
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🏅"
            print(f"{medal} #{i} {agent['name']} ({agent['type']})")
            print(f"   📊 Total Activity: {total_activity} messages")
            print(f"   📤 Sent: {data['total_messages_sent']} | 📥 Received: {data['total_messages_received']}")
            print(f"   ⏱️ Avg Response Time: {data['average_response_time']:.2f}ms")
            print(f"   💬 Conversations: {data['conversation_count']}")
            print()
        
        # Performance analysis
        print("📊 PERFORMANCE ANALYSIS:")
        print("-" * 40)
        
        response_times = [data['average_response_time'] for data in activity_summary.values() if data['average_response_time'] > 0]
        if response_times:
            fastest_time = min(response_times)
            slowest_time = max(response_times)
            avg_time = sum(response_times) / len(response_times)
            
            print(f"⚡ Fastest Response Time: {fastest_time:.2f}ms")
            print(f"🐌 Slowest Response Time: {slowest_time:.2f}ms")
            print(f"📊 Average Response Time: {avg_time:.2f}ms")
        
        # Most active agent
        most_active = max(activity_summary.items(), 
                         key=lambda x: x[1]['total_messages_sent'] + x[1]['total_messages_received'])
        print(f"🔥 Most Active Agent: {most_active[1]['agent_info']['name']}")
    
    def export_message_data(self):
        """Export message data to files"""
        print("\n" + "=" * 80)
        print("📁 EXPORT MESSAGE DATA")
        print("=" * 80)
        
        try:
            # Export message log
            log_file = message_tracker.export_message_log()
            print(f"✅ Message log exported to: {log_file}")
            
            # Export visualization data
            viz_file = message_visualizer.export_visualization_data()
            print(f"✅ Visualization data exported to: {viz_file}")
            
            print(f"\n📊 Export Summary:")
            print(f"   📈 Total Exchanges: {message_tracker.message_stats['total_exchanges']}")
            print(f"   👥 Total Agents: {len(message_tracker.agents)}")
            print(f"   💬 Total Conversations: {len(message_tracker.conversations)}")
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
    
    def display_message_flow_viz(self):
        """Display message flow visualization"""
        print("\n" + "=" * 80)
        print("🎨 MESSAGE FLOW VISUALIZATION")
        print("=" * 80)
        
        if not message_tracker.exchanges:
            print("❌ No message exchanges to visualize")
            return
        
        # Show recent exchanges with full visualization
        recent_exchanges = sorted(message_tracker.exchanges, key=lambda x: x.timestamp, reverse=True)[:5]
        
        print("🎬 RECENT MESSAGE FLOWS:")
        print("-" * 40)
        
        for i, exchange in enumerate(recent_exchanges, 1):
            print(f"\n📨 MESSAGE FLOW #{i}:")
            message_visualizer.display_message_flow(exchange, show_content=True)
            time.sleep(1)  # Pause between visualizations
    
    def run_interactive_dashboard(self):
        """Run the interactive dashboard"""
        self.running = True
        
        while self.running:
            try:
                self.display_main_menu()
                choice = input("\n🎯 Select an option (1-9): ").strip()
                
                if choice == "1":
                    self.display_real_time_stats()
                elif choice == "2":
                    self.display_agent_network()
                elif choice == "3":
                    self.display_conversation_threads()
                elif choice == "4":
                    self.display_recent_exchanges()
                elif choice == "5":
                    self.start_live_monitor()
                elif choice == "6":
                    self.display_agent_analysis()
                elif choice == "7":
                    self.export_message_data()
                elif choice == "8":
                    self.display_message_flow_viz()
                elif choice == "9":
                    print("\n👋 Goodbye!")
                    self.running = False
                else:
                    print("❌ Invalid option. Please try again.")
                
                if self.running:
                    input("\n⏸️ Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Dashboard stopped by user")
                self.running = False
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("⏸️ Press Enter to continue...")

def main():
    """Main function to run the dashboard"""
    print("🚀 Starting Multi-Agent Message Dashboard...")
    
    dashboard = MessageDashboard()
    dashboard.run_interactive_dashboard()

if __name__ == "__main__":
    main()
