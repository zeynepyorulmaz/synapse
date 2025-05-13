"""
Agent management module for Synapse Protocol
"""

from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.outputs import LLMResult

class AgentManager:
    """Manages AI agents and their interactions."""
    
    def __init__(self, api_key: str, environment: str = "sandbox"):
        """
        Initialize the agent manager.
        
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
        self.agents: Dict[str, Agent] = {}
        self.crews: Dict[str, Crew] = {}
        
    def create_agent(self, 
                    name: str,
                    role: str,
                    goal: str,
                    backstory: str,
                    tools: Optional[List[Any]] = None) -> Agent:
        """
        Create a new agent.
        
        Args:
            name: Unique identifier for the agent
            role: Agent's role
            goal: Agent's goal
            backstory: Agent's backstory
            tools: List of tools the agent can use
            
        Returns:
            Created agent
        """
        agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            llm=self.llm,
            tools=tools or [],
            verbose=True
        )
        self.agents[name] = agent
        return agent
        
    def create_task(self, 
                   description: str,
                   agent_name: str,
                   expected_output: Optional[str] = None) -> Task:
        """
        Create a new task for an agent.
        
        Args:
            description: Task description
            agent_name: Name of the agent to perform the task
            expected_output: Expected output format
            
        Returns:
            Created task
        """
        if agent_name not in self.agents:
            raise ValueError(f"Agent {agent_name} not found")
            
        return Task(
            description=description,
            agent=self.agents[agent_name],
            expected_output=expected_output
        )
        
    def create_crew(self,
                   name: str,
                   agent_names: List[str],
                   tasks: List[Task],
                   process: Process = Process.sequential) -> Crew:
        """
        Create a new crew of agents.
        
        Args:
            name: Unique identifier for the crew
            agent_names: List of agent names to include
            tasks: List of tasks to perform
            process: Process type (sequential or hierarchical)
            
        Returns:
            Created crew
        """
        agents = [self.agents[name] for name in agent_names if name in self.agents]
        if not agents:
            raise ValueError("No valid agents found")
            
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=process,
            verbose=True
        )
        self.crews[name] = crew
        return crew
        
    def execute_crew(self, crew_name: str) -> Dict[str, Any]:
        """
        Execute a crew's tasks.
        
        Args:
            crew_name: Name of the crew to execute
            
        Returns:
            Execution results
        """
        if crew_name not in self.crews:
            raise ValueError(f"Crew {crew_name} not found")
            
        return self.crews[crew_name].kickoff()
        
    def create_payment_crew(self) -> Crew:
        """
        Create a crew for handling payments.
        
        Returns:
            Payment handling crew
        """
        # Create payment processing agents
        validator = self.create_agent(
            name="validator",
            role="Payment Validator",
            goal="Validate payment requests and ensure they meet all requirements",
            backstory="Expert in payment validation and risk assessment"
        )
        
        processor = self.create_agent(
            name="processor",
            role="Payment Processor",
            goal="Process valid payments and ensure successful completion",
            backstory="Experienced in handling various payment methods and currencies"
        )
        
        auditor = self.create_agent(
            name="auditor",
            role="Payment Auditor",
            goal="Audit completed payments and ensure compliance",
            backstory="Specialist in payment auditing and compliance verification"
        )
        
        # Create payment processing tasks
        validation_task = self.create_task(
            description="Validate payment request details and check for potential issues",
            agent_name="validator",
            expected_output="Validation report with any issues found"
        )
        
        processing_task = self.create_task(
            description="Process the payment and ensure successful completion",
            agent_name="processor",
            expected_output="Payment processing result with transaction details"
        )
        
        audit_task = self.create_task(
            description="Audit the completed payment and verify compliance",
            agent_name="auditor",
            expected_output="Audit report with compliance status"
        )
        
        # Create and return the payment crew
        return self.create_crew(
            name="payment_crew",
            agent_names=["validator", "processor", "auditor"],
            tasks=[validation_task, processing_task, audit_task]
        )
        
    def create_risk_assessment_crew(self) -> Crew:
        """
        Create a crew for risk assessment.
        
        Returns:
            Risk assessment crew
        """
        # Create risk assessment agents
        risk_analyzer = self.create_agent(
            name="risk_analyzer",
            role="Risk Analyzer",
            goal="Analyze payment risks and provide risk assessment",
            backstory="Expert in financial risk analysis and fraud detection"
        )
        
        compliance_checker = self.create_agent(
            name="compliance_checker",
            role="Compliance Checker",
            goal="Verify compliance with regulations and policies",
            backstory="Specialist in financial regulations and compliance requirements"
        )
        
        # Create risk assessment tasks
        analysis_task = self.create_task(
            description="Analyze payment risks and provide detailed assessment",
            agent_name="risk_analyzer",
            expected_output="Risk assessment report with risk levels and recommendations"
        )
        
        compliance_task = self.create_task(
            description="Verify compliance with relevant regulations",
            agent_name="compliance_checker",
            expected_output="Compliance verification report"
        )
        
        # Create and return the risk assessment crew
        return self.create_crew(
            name="risk_crew",
            agent_names=["risk_analyzer", "compliance_checker"],
            tasks=[analysis_task, compliance_task]
        ) 