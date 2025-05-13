"""
CrewAI integration for Synapse Protocol
"""

import os
from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.outputs import LLMResult

class CrewManager:
    """Manages CrewAI agents and their interactions."""
    
    def __init__(self, api_key: str, environment: str = "sandbox"):
        """
        Initialize the CrewAI manager.
        
        Args:
            api_key: OpenAI API key
            environment: 'sandbox' or 'production'
        """
        self.api_key = api_key
        self.environment = environment
        self.llm = ChatOpenAI(
            api_key=api_key,
            model="gpt-3.5-turbo",
            temperature=0.7
        )
        
    def create_agent(self, role: str, goal: str, backstory: str) -> Agent:
        """
        Create a new agent.
        
        Args:
            role: Agent's role
            goal: Agent's goal
            backstory: Agent's backstory
            
        Returns:
            Created agent
        """
        return Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            llm=self.llm,
            verbose=True
        )
        
    def create_task(self, description: str, agent: Agent) -> Task:
        """
        Create a new task.
        
        Args:
            description: Task description
            agent: Agent to perform the task
            
        Returns:
            Created task
        """
        return Task(
            description=description,
            agent=agent
        )
        
    def create_crew(self, agents: List[Agent], tasks: List[Task]) -> Crew:
        """
        Create a new crew.
        
        Args:
            agents: List of agents
            tasks: List of tasks
            
        Returns:
            Created crew
        """
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
    def execute_crew(self, crew: Crew) -> Dict[str, Any]:
        """
        Execute a crew's tasks.
        
        Args:
            crew: Crew to execute
            
        Returns:
            Execution results
        """
        return crew.kickoff()
        
    def create_payment_crew(self) -> Crew:
        """
        Create a crew for handling payments.
        
        Returns:
            Payment handling crew
        """
        # Create payment processing agents
        validator = self.create_agent(
            role="Payment Validator",
            goal="Validate payment requests and ensure they meet all requirements",
            backstory="Expert in payment validation and risk assessment"
        )
        
        processor = self.create_agent(
            role="Payment Processor",
            goal="Process valid payments and ensure successful completion",
            backstory="Experienced in handling various payment methods and currencies"
        )
        
        auditor = self.create_agent(
            role="Payment Auditor",
            goal="Audit completed payments and ensure compliance",
            backstory="Specialist in payment auditing and compliance verification"
        )
        
        # Create payment processing tasks
        validation_task = self.create_task(
            description="Validate payment request details and check for potential issues",
            agent=validator
        )
        
        processing_task = self.create_task(
            description="Process the payment and ensure successful completion",
            agent=processor
        )
        
        audit_task = self.create_task(
            description="Audit the completed payment and verify compliance",
            agent=auditor
        )
        
        # Create and return the payment crew
        return self.create_crew(
            agents=[validator, processor, auditor],
            tasks=[validation_task, processing_task, audit_task]
        ) 