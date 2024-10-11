import requests
from PyPDF2 import PdfReader
from gentopia.tools.basetool import *
from io import BytesIO
from typing import Optional, Type
from pydantic import BaseModel, Field

class ReadPDFArgs(BaseModel):
    file_url: str = Field(..., description="Read the url")

class ReadPDF(BaseTool):

    name = "read_pdf"
    description = ("reads the pdf")

    args_schema: Optional[Type[BaseModel]] = ReadPDFArgs

    def _run(self, file_url: str) -> str:
        try:
            response = requests.get(file_url)
            if response.status_code == 200:
                pdf_content = BytesIO(response.content)
                reader = PdfReader(pdf_content)
                text = []
                for page_num in range(len(reader.pages)):
                    text.append(reader.pages[page_num].extract_text())
                return '\n\n'.join(text) if text else "Empty PDF."
            else:
                return f"Status code: {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        """Async method not implemented."""
        raise NotImplementedError