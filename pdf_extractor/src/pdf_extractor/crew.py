# src/latest_ai_development/crew.py
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
import os
import yaml

from pdf_extractor.src.pdf_extractor.tools.custom_tool import DocumentExtracterInput, DocumentExtracterTool
pdf_path = ''
llm = LLM(
            model="Your using Model",
            base_url="the url for your LLM",
            api_key="Your key",
            temperature=0.1,#set your temperature nd top_p
            top_p=0.95
        )
@CrewBase
class LatestAiDevelopmentCrew():
    """LatestAiDevelopment crew"""
    agents = []
    tasks = []
    crew = None
    agents_config = None
    tasks_config = None
    pdf_source = None
    def __init__(self):

        self.agents_config = self.load_agents_config()
        self.tasks_config = self.load_tasks_config()
        self.pdf_source = PDFKnowledgeSource(
            file_paths=['Circular no. 146022021 GST.pdf','No. 102023 Central Tax.pdf','notfctn-13-central-tax-english-2020.pdf','notfctn-14-central-tax-english-2020.pdf','Rule 46.pdf']
        )
        self.agents.append(
            Agent(
                llm=llm,
                config=self.agents_config.get('pdf_extractor'),
                verbose=True,
                allow_delegation=False,
                result_as_answer = True,
                max_iter=1,
                max_retry_limit=1,
                memory=False,
                tools=[DocumentExtracterTool()],
                args_schema=DocumentExtracterInput,
            )
        )

        self.agents.append(
            Agent(
                llm=llm,
                config=self.agents_config.get('invoice_analyzer'),
                verbose=True,
                allow_delegation=False,
                result_as_answer = True,
                max_iter=2,
                max_retry_limit=2,
                memory=False,
            )
        )

        self.tasks.append(
            Task(
                description=self.tasks_config.get('extract_text').get("description"),
                expected_output=self.tasks_config.get('extract_text').get("expected_output"),
                agent=self.agents[0]
            )
        )

        self.tasks.append(
            Task(
                description=self.tasks_config.get('analyze_invoice_text').get("description"),
                expected_output=self.tasks_config.get('analyze_invoice_text').get("expected_output"),
                agent=self.agents[1]
            )
        )

        self.crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            knowledge_sources=[self.pdf_source]
        )
    
    def load_agents_config(self):
        """
        Load configuration from the default Agents YAML file.
        """
        default_path = "./pdf_extractor/src/pdf_extractor/config/agents.yaml"
        if not os.path.exists(default_path):
            raise FileNotFoundError(f"Configuration file not found at {default_path}")
        with open(default_path, "r") as file:
            return yaml.safe_load(file)
        
    def load_tasks_config(self):
        """
        Load configuration from the default Agents YAML file.
        """
        default_path = "./pdf_extractor/src/pdf_extractor/config/tasks.yaml"
        if not os.path.exists(default_path):
            raise FileNotFoundError(f"Configuration file not found at {default_path}")
        with open(default_path, "r") as file:
            return yaml.safe_load(file)
    
    def kickoff(self,inputs):
        return self.crew.kickoff(inputs=inputs)