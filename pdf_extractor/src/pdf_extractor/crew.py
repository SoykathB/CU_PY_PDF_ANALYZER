# src/latest_ai_development/crew.py
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
import os
from sentence_transformers import SentenceTransformer
from chromadb import EmbeddingFunction
import numpy as np
import yaml
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from pdf_extractor.src.pdf_extractor.tools.custom_tool import DocumentExtracterInput, DocumentExtracterTool
pdf_path = ''
llm = LLM(
            model="hosted_vllm/Llama-3.1-8B-Instruct",
            base_url="Your LLM Url",
            api_key="nokeyforyou",
            temperature=0.1,
            top_p=0.95
        )

class SentenceTransformersEmbedder(EmbeddingFunction):
    def __init__(self, model_name: str = "all-mpnet-base-v2"):
        self.model = SentenceTransformer(model_name,device="cpu")

    def __call__(self, texts):
        embeddings = self.model.encode(texts)
        return [np.array(x) for x in embeddings]
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
        text_source = TextFileKnowledgeSource(
                            file_paths=["gst_rules.txt"]
                        )
        self.agents.append(
            Agent(
                llm=llm,
                # config=self.agents_config.get('invoice_processor'),
                role= self.agents_config.get('invoice_processor').get('role'),
                goal=self.agents_config.get('invoice_processor').get('goal'),
                backstory=self.agents_config.get('invoice_processor').get('backstory'),
                verbose=True,
                result_as_answer = True,
                max_iter=1,
                memory=True,
                tools=[DocumentExtracterTool()],
                args_schema=DocumentExtracterInput,
                knowledge_sources=[text_source],
                embedder={
                    "provider": "custom",
                    "config": {
                        "embedder": SentenceTransformersEmbedder("all-mpnet-base-v2")
                    }
                }
            )
        )


        self.tasks.append(
            Task(
                description=self.tasks_config.get('analyze_invoice_from_pdf').get("description"),
                expected_output=self.tasks_config.get('analyze_invoice_from_pdf').get("expected_output"),
                agent=self.agents[0]
            )
        )
        
        self.crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
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
    
    def kickoff(self,inputs):
        return self.crew.kickoff(inputs=inputs)