# src/latest_ai_development/crew.py
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase
import os
import yaml
pdf_path = ''
llm = LLM(
            model="hosted_vllm/Llama-3.1-8B-Instruct",
            base_url="http://10.45.28.219:8701/v1/",
            api_key="nokeyforyou",
            temperature=0.1,
            top_p=0.95
        )
@CrewBase
class PDFEXTRACTOR():
    """LatestAiDevelopment crew"""
    agents = []
    tasks = []
    crew = None
    agents_config = None
    tasks_config = None
    def __init__(self):
        self.agents_config = self.load_agents_config()
        self.tasks_config = self.load_tasks_config()
        self.agents.append(
            Agent(
                llm=llm,
                # config=self.agents_config.get('pdf_data_extractor'),
                role = self.agents_config.get('pdf_data_extractor').get('role'),
                goal= self.agents_config.get('pdf_data_extractor').get('goal'),
                backstory= self.agents_config.get('pdf_data_extractor').get('backstory'),
                verbose=True,
                allow_delegation=False,
                result_as_answer = True,
                max_iter=1,
                max_retry_limit=1,
                memory=False
            )
        )


        self.tasks.append(
            Task(
                description=self.tasks_config.get('extract_pdf_info_task').get("description"),
                expected_output=self.tasks_config.get('extract_pdf_info_task').get("expected_output"),
                agent=self.agents[0]
            )
        )

        self.crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
    
    def load_agents_config(self):
        """
        Load configuration from the default Agents YAML file.
        """
        default_path = "./pdf_extractor/src/pdf_extractor/config/agents.yaml"
        if not os.path.exists(default_path):
            raise FileNotFoundError(f"Configuration file not found at {default_path}")
        with open(default_path, "r") as file:
            text = yaml.safe_load(file)
        return self.remove_newlines(text)
    
    def remove_newlines(self,data):
        if isinstance(data, dict):
            return {k: self.remove_newlines(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.remove_newlines(item) for item in data]
        elif isinstance(data, str):
            return data.replace('\n', '')
        else:
            return data
    
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