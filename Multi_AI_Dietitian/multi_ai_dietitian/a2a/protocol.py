from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
from enum import Enum
import json
import uuid
from datetime import datetime


class MessageType(Enum):
    # Core protocol messages
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    ERROR = "error"
    
    # Agent-specific messages
    PREFERENCE_UPDATE = "preference_update"
    GOAL_ANALYSIS = "goal_analysis"
    FOOD_SUGGESTION = "food_suggestion"
    SAFETY_CHECK = "safety_check"
    ADAPTATION_REQUEST = "adaptation_request"
    MOTIVATION_MESSAGE = "motivation_message"
    CULTURAL_ADAPTATION = "cultural_adaptation"
    BUDGET_CHECK = "budget_check"
    TIMING_SUGGESTION = "timing_suggestion"
    SUSTAINABILITY_CHECK = "sustainability_check"
    MEDICAL_ALERT = "medical_alert"
    FEEDBACK_PROCESSING = "feedback_processing"
    EMERGENCY_ALERT = "emergency_alert"
    # Analysis-specific messages
    MEAL_ANALYSIS = "meal_analysis"
    DAILY_NUTRITION_ANALYSIS = "daily_nutrition_analysis"
    PROGRESS_ANALYSIS = "progress_analysis"
    COST_ANALYSIS = "cost_analysis"


class Priority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class A2AMessage:
    """Base A2A message structure"""
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    message_type: MessageType = MessageType.REQUEST
    priority: Priority = Priority.NORMAL
    sender: str = ""
    recipient: str = ""
    content: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "timestamp": self.timestamp.isoformat(),
            "message_type": self.message_type.value,
            "priority": self.priority.value,
            "sender": self.sender,
            "recipient": self.recipient,
            "content": self.content,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> A2AMessage:
        return cls(
            message_id=data.get("message_id", str(uuid.uuid4())),
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else datetime.now(),
            message_type=MessageType(data["message_type"]),
            priority=Priority(data["priority"]),
            sender=data["sender"],
            recipient=data["recipient"],
            content=data["content"],
            metadata=data["metadata"]
        )


# New lightweight A2A protocol for LangGraph integration
@dataclass
class AgentMessage:
    topic: str
    sender: str
    recipients: List[str]
    payload: Dict[str, Any]
    severity: Priority = Priority.NORMAL


@dataclass
class SystemState:
    profile: Dict[str, Any] = field(default_factory=dict)
    goals: Dict[str, Any] = field(default_factory=dict)
    plan: Dict[str, Any] = field(default_factory=dict)
    analysis_results: Dict[str, Any] = field(default_factory=dict)
    safety_flags: List[str] = field(default_factory=list)
    events: List[Dict[str, Any]] = field(default_factory=list)


class Agent(ABC):
    """Base agent class for A2A protocol"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.message_queue: List[A2AMessage] = []
        self.conversation_history: List[A2AMessage] = []
    
    @abstractmethod
    def process_message(self, message: A2AMessage) -> A2AMessage:
        """Process incoming message and return response"""
        pass
    
    def send_message(self, recipient: str, message_type: MessageType, 
                    content: Dict[str, Any], priority: Priority = Priority.NORMAL) -> A2AMessage:
        """Send a message to another agent"""
        message = A2AMessage(
            sender=self.agent_id,
            recipient=recipient,
            message_type=message_type,
            priority=priority,
            content=content
        )
        return message
    
    def receive_message(self, message: A2AMessage) -> None:
        """Receive and queue a message"""
        self.message_queue.append(message)
        self.conversation_history.append(message)
    
    def get_pending_messages(self) -> List[A2AMessage]:
        """Get all pending messages for this agent"""
        return self.message_queue.copy()
    
    def clear_message_queue(self) -> None:
        """Clear the message queue"""
        self.message_queue.clear()


class A2AOrchestrator:
    """Orchestrates communication between agents"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.message_history: List[A2AMessage] = []
    
    def register_agent(self, agent: Agent) -> None:
        """Register an agent with the orchestrator"""
        self.agents[agent.agent_id] = agent
    
    def send_message(self, message: A2AMessage) -> A2AMessage:
        """Send a message between agents"""
        if message.recipient not in self.agents:
            raise ValueError(f"Recipient agent {message.recipient} not found")
        
        recipient_agent = self.agents[message.recipient]
        recipient_agent.receive_message(message)
        
        # Process the message
        response = recipient_agent.process_message(message)
        
        # Record in history
        self.message_history.extend([message, response])
        
        return response
    
    def broadcast_message(self, sender: str, message_type: MessageType, 
                         content: Dict[str, Any], priority: Priority = Priority.NORMAL) -> List[A2AMessage]:
        """Broadcast a message to all agents except sender"""
        responses = []
        for agent_id, agent in self.agents.items():
            if agent_id != sender:
                message = A2AMessage(
                    sender=sender,
                    recipient=agent_id,
                    message_type=message_type,
                    priority=priority,
                    content=content
                )
                response = self.send_message(message)
                responses.append(response)
        return responses
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            agent_id: {
                "pending_messages": len(agent.get_pending_messages()),
                "conversation_history_length": len(agent.conversation_history)
            }
            for agent_id, agent in self.agents.items()
        }
