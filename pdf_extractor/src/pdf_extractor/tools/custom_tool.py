from pydantic import BaseModel, Field, PrivateAttr
from crewai.tools import BaseTool
from typing import Type
from docling.document_converter import DocumentConverter

# Input schema using Pydantic
class DocumentExtracterInput(BaseModel):
    user_query: str = Field(
        title="User Query",
        description="The user query in normal natural language to understand and fetch the relevant data from identified Databases",
    )
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
    
    def _run(self,user_query: str, filepath: str):
        """
        Run the tool to process the given filepath and user query.

        Args:
            filepath (str): The path to the file to process.
            user_query (str): The user's query for extracting relevant data.

        Returns:
            Any: The result of the document conversion and query processing.
        """
        source = filepath  # document per local path or URL
        converter = DocumentConverter()
        result = converter.convert(source)
        # Optionally, process the result further based on user_query
        return result.document.export_to_markdown()