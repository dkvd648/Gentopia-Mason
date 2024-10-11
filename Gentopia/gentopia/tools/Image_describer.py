import requests
from PIL import Image
import pytesseract
from io import BytesIO
from gentopia.tools.basetool import *
from typing import Optional, Type
from pydantic import BaseModel, Field

class ImageDescriberArgs(BaseModel):
    image_url: str = Field(..., description="The URL of the image to describe")

class ImageDescriber(BaseTool):
    """Tool that downloads an image from a URL, describes it, and extracts text using OCR."""

    name = "Image_describer"
    description = ("A tool that downloads an image from a URL and provides basic information about it, "
                   "as well as extracting text from it using OCR. Input should be a URL to the image.")

    args_schema: Optional[Type[BaseModel]] = ImageDescriberArgs

    def _run(self, image_url: str) -> str:
        """Download the image from the provided URL and describe it."""
        try:
            # Download the image
            response = requests.get(image_url)
            if response.status_code == 200:
                # Open the image in memory
                img = Image.open(BytesIO(response.content))
                
                # Describe basic properties
                description = (f"Image format: {img.format}\n"
                               f"Image size: {img.size}\n"
                               f"Image mode: {img.mode}\n")

                # Extract text using OCR
                ocr_text = pytesseract.image_to_string(img)
                description += f"\nExtracted Text (if any):\n{ocr_text if ocr_text.strip() else 'No text found'}"
                
                return description
            else:
                return f"Failed to download the image. Status code: {response.status_code}"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        """Async method not implemented."""
        raise NotImplementedError
    