from pydantic import BaseModel, Field, PrivateAttr
from crewai.tools import BaseTool
from typing import Type
import requests
import json

# Input schema using Pydantic
class DocumentExtracterInput(BaseModel):
    filepath: str = Field(
        title="FilePath",
        description="The Actual path of the file where gradio saves",
    )

class DocumentExtracterTool(BaseTool):
    name: str = "DocumentExtracterTool"
    description: str = "Extracts PDF data"
    args_schema: Type[BaseModel] = DocumentExtracterInput
    def __init__(self):
        """
        Initialize the tool, load the configuration, and set up necessary attributes.
        """
        super().__init__()  # Ensure proper initialization of BaseTool if necessary
    
    def _run(self,filepath: str):

        try:
            url = "Your Url"
            with open(filepath, "rb") as file_obj:
                files = {
                    "file": (filepath.split("/")[-1], file_obj)  # Just like curl does with @
                }
                response = requests.post(url, files=files)
                if(response.text):
                    data = json.loads(response.text)
                    return data.get('data')
                else:
                    return 'No file found'
    
        except Exception as e:
            return str(e)