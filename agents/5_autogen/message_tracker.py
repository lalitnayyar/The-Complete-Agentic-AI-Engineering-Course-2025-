#!/usr/bin/env python3
"""
Innovative Message Tracking System for Multi-Agent Communication
Provides detailed visibility into message exchanges with originator and target agent information
"""

import json
import time
import uuid
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class AgentInfo:
    """Detailed information about an agent"""
    id: str
    name: str
    type: str
    status: str = "active"
    created_at: str = ""
    last_seen: str = ""
    message_count: int = 0
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.last_seen:
            self.last_seen = datetime.now().isoformat()

@dataclass
class MessageExchange:
    """Detailed message exchange information"""
    exchange_id: str
    timestamp: str
    originator: AgentInfo
    target: AgentInfo
    message_type: str
    content: str
    content_length: int
    response_time_ms: float
    status: str  # "sent", "delivered", "processed", "failed"
    conversation_id: str
    parent_exchange_id: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class MessageTracker:
    """Advanced message tracking and visualization system"""
    
    def __init__(self, log_file: str = "message_exchanges.json"):
        self.log_file = Path(log_file)
        self.exchanges: List[MessageExchange] = []
        self.agents: Dict[str, AgentInfo] = {}
        self.conversations: Dict[str, List[str]] = {}  # conversation_id -> exchange_ids
        self.message_stats = {
            "total_exchanges": 0,
            "successful_exchanges": 0,
            "failed_exchanges": 0,
            "average_response_time": 0.0,
            "most_active_agent": "",
            "longest_conversation": 0
        }
        
        # Create log directory if it doesn't exist
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info("🔍 Message Tracker initialized")
    
    def register_agent(self, agent_id: str, name: str, agent_type: str) -> AgentInfo:
        """Register a new agent in the tracking system"""
        agent_info = AgentInfo(
            id=agent_id,
            name=name,
            type=agent_type,
            status="active"
        )
        self.agents[agent_id] = agent_info
        logger.info(f"📝 Registered agent: {name} ({agent_id})")
        return agent_info
    
    def start_message_exchange(self, originator_id: str, target_id: str, 
                             message_type: str, content: str, 
                             conversation_id: str = None) -> str:
        """Start tracking a new message exchange"""
        if conversation_id is None:
            conversation_id = str(uuid.uuid4())
        
        exchange_id = str(uuid.uuid4())
        
        # Get or create agent info
        originator = self.agents.get(originator_id)
        target = self.agents.get(target_id)
        
        if not originator:
            originator = AgentInfo(originator_id, originator_id, "unknown")
            self.agents[originator_id] = originator
        
        if not target:
            target = AgentInfo(target_id, target_id, "unknown")
            self.agents[target_id] = target
        
        # Update agent last seen
        originator.last_seen = datetime.now().isoformat()
        originator.message_count += 1
        
        exchange = MessageExchange(
            exchange_id=exchange_id,
            timestamp=datetime.now().isoformat(),
            originator=originator,
            target=target,
            message_type=message_type,
            content=content,
            content_length=len(content),
            response_time_ms=0.0,
            status="sent",
            conversation_id=conversation_id,
            metadata={
                "start_time": time.time(),
                "content_preview": content[:100] + "..." if len(content) > 100 else content
            }
        )
        
        self.exchanges.append(exchange)
        
        # Track conversation
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        self.conversations[conversation_id].append(exchange_id)
        
        # Log the exchange
        self._log_exchange(exchange)
        
        logger.info(f"📤 Message exchange started: {originator.name} → {target.name} [{exchange_id[:8]}]")
        
        return exchange_id
    
    def complete_message_exchange(self, exchange_id: str, status: str = "processed", 
                                response_content: str = None):
        """Mark a message exchange as completed"""
        exchange = self._find_exchange(exchange_id)
        if not exchange:
            logger.warning(f"⚠️ Exchange not found: {exchange_id}")
            return
        
        # Calculate response time
        start_time = exchange.metadata.get("start_time", time.time())
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        exchange.response_time_ms = response_time
        exchange.status = status
        
        if response_content:
            exchange.metadata["response_content"] = response_content
            exchange.metadata["response_length"] = len(response_content)
        
        # Update statistics
        self._update_statistics()
        
        # Log completion
        self._log_exchange(exchange)
        
        logger.info(f"📥 Message exchange completed: {exchange.originator.name} → {exchange.target.name} "
                   f"[{exchange_id[:8]}] - {status} ({response_time:.2f}ms)")
    
    def get_agent_activity_summary(self) -> Dict[str, Any]:
        """Get detailed activity summary for all agents"""
        summary = {}
        for agent_id, agent in self.agents.items():
            agent_exchanges = [e for e in self.exchanges 
                             if e.originator.id == agent_id or e.target.id == agent_id]
            
            summary[agent_id] = {
                "agent_info": asdict(agent),
                "total_messages_sent": len([e for e in agent_exchanges if e.originator.id == agent_id]),
                "total_messages_received": len([e for e in agent_exchanges if e.target.id == agent_id]),
                "average_response_time": self._calculate_agent_avg_response_time(agent_id),
                "conversation_count": len(set(e.conversation_id for e in agent_exchanges)),
                "last_activity": agent.last_seen
            }
        
        return summary
    
    def get_conversation_flow(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Get detailed conversation flow for a specific conversation"""
        if conversation_id not in self.conversations:
            return []
        
        flow = []
        for exchange_id in self.conversations[conversation_id]:
            exchange = self._find_exchange(exchange_id)
            if exchange:
                flow.append({
                    "exchange_id": exchange.exchange_id,
                    "timestamp": exchange.timestamp,
                    "originator": asdict(exchange.originator),
                    "target": asdict(exchange.target),
                    "message_type": exchange.message_type,
                    "content": exchange.content,
                    "content_length": exchange.content_length,
                    "response_time_ms": exchange.response_time_ms,
                    "status": exchange.status,
                    "metadata": exchange.metadata
                })
        
        return flow
    
    def generate_message_dashboard(self) -> str:
        """Generate a real-time message dashboard"""
        dashboard = []
        dashboard.append("=" * 80)
        dashboard.append("🤖 MULTI-AGENT MESSAGE DASHBOARD")
        dashboard.append("=" * 80)
        dashboard.append(f"📊 Total Exchanges: {self.message_stats['total_exchanges']}")
        dashboard.append(f"✅ Successful: {self.message_stats['successful_exchanges']}")
        dashboard.append(f"❌ Failed: {self.message_stats['failed_exchanges']}")
        dashboard.append(f"⏱️ Avg Response Time: {self.message_stats['average_response_time']:.2f}ms")
        dashboard.append(f"🔥 Most Active Agent: {self.message_stats['most_active_agent']}")
        dashboard.append("")
        
        # Agent activity summary
        dashboard.append("👥 AGENT ACTIVITY SUMMARY")
        dashboard.append("-" * 40)
        activity_summary = self.get_agent_activity_summary()
        for agent_id, data in activity_summary.items():
            agent = data['agent_info']
            dashboard.append(f"🤖 {agent['name']} ({agent['type']})")
            dashboard.append(f"   📤 Sent: {data['total_messages_sent']} | 📥 Received: {data['total_messages_received']}")
            dashboard.append(f"   ⏱️ Avg Response: {data['average_response_time']:.2f}ms | 💬 Conversations: {data['conversation_count']}")
            dashboard.append(f"   🕐 Last Active: {data['last_activity']}")
            dashboard.append("")
        
        # Recent exchanges
        dashboard.append("📨 RECENT MESSAGE EXCHANGES")
        dashboard.append("-" * 40)
        recent_exchanges = sorted(self.exchanges, key=lambda x: x.timestamp, reverse=True)[:10]
        for exchange in recent_exchanges:
            status_emoji = "✅" if exchange.status == "processed" else "⏳" if exchange.status == "sent" else "❌"
            dashboard.append(f"{status_emoji} {exchange.originator.name} → {exchange.target.name}")
            dashboard.append(f"   📝 {exchange.message_type} | {exchange.content_length} chars | {exchange.response_time_ms:.2f}ms")
            dashboard.append(f"   🕐 {exchange.timestamp} | 💬 {exchange.conversation_id[:8]}")
            dashboard.append("")
        
        return "\n".join(dashboard)
    
    def export_message_log(self, filename: str = None) -> str:
        """Export complete message log to JSON file"""
        if filename is None:
            filename = f"message_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        log_data = {
            "export_timestamp": datetime.now().isoformat(),
            "statistics": self.message_stats,
            "agents": {aid: asdict(agent) for aid, agent in self.agents.items()},
            "exchanges": [asdict(exchange) for exchange in self.exchanges],
            "conversations": self.conversations
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📁 Message log exported to: {filename}")
        return filename
    
    def _find_exchange(self, exchange_id: str) -> Optional[MessageExchange]:
        """Find an exchange by ID"""
        for exchange in self.exchanges:
            if exchange.exchange_id == exchange_id:
                return exchange
        return None
    
    def _calculate_agent_avg_response_time(self, agent_id: str) -> float:
        """Calculate average response time for an agent"""
        agent_exchanges = [e for e in self.exchanges 
                          if e.originator.id == agent_id and e.response_time_ms > 0]
        if not agent_exchanges:
            return 0.0
        return sum(e.response_time_ms for e in agent_exchanges) / len(agent_exchanges)
    
    def _update_statistics(self):
        """Update message statistics"""
        self.message_stats["total_exchanges"] = len(self.exchanges)
        self.message_stats["successful_exchanges"] = len([e for e in self.exchanges if e.status == "processed"])
        self.message_stats["failed_exchanges"] = len([e for e in self.exchanges if e.status == "failed"])
        
        # Calculate average response time
        completed_exchanges = [e for e in self.exchanges if e.response_time_ms > 0]
        if completed_exchanges:
            self.message_stats["average_response_time"] = sum(e.response_time_ms for e in completed_exchanges) / len(completed_exchanges)
        
        # Find most active agent
        agent_activity = {}
        for exchange in self.exchanges:
            originator_id = exchange.originator.id
            agent_activity[originator_id] = agent_activity.get(originator_id, 0) + 1
        
        if agent_activity:
            most_active_id = max(agent_activity, key=agent_activity.get)
            self.message_stats["most_active_agent"] = self.agents[most_active_id].name
        
        # Find longest conversation
        if self.conversations:
            self.message_stats["longest_conversation"] = max(len(exchanges) for exchanges in self.conversations.values())
    
    def _log_exchange(self, exchange: MessageExchange):
        """Log exchange to file"""
        log_entry = {
            "timestamp": exchange.timestamp,
            "exchange_id": exchange.exchange_id,
            "originator": asdict(exchange.originator),
            "target": asdict(exchange.target),
            "message_type": exchange.message_type,
            "content": exchange.content,
            "content_length": exchange.content_length,
            "response_time_ms": exchange.response_time_ms,
            "status": exchange.status,
            "conversation_id": exchange.conversation_id,
            "metadata": exchange.metadata
        }
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

# Global message tracker instance
message_tracker = MessageTracker()
