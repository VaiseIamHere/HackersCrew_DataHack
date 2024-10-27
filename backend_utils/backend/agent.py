from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
import os
from dotenv import load_dotenv
from typing import List, Optional, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFSummarizer:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the PDF Summarizer with Groq LLM."""
        load_dotenv()
        
        # Set up Groq LLM
        self.llm = ChatGroq(
            groq_api_key=api_key or os.getenv("GROQ_API_KEY"),
            model_name="mixtral-8x7b-32768",  # Using Mixtral model for better performance
            temperature=0.3,
            max_tokens=4096
        )
        
        # Initialize text splitter for chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=400,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
            length_function=len
        )
        
        # Set up prompts
        self.map_prompt = PromptTemplate(
            template="""Summarize the following text excerpt from a document. Focus on key points and main ideas:

{text}

SUMMARY:""",
            input_variables=["text"]
        )
        
        self.combine_prompt = PromptTemplate(
            template="""Combine these document summaries into a coherent summary. 
            Organize the information logically and maintain the key points:

{text}

COMPREHENSIVE SUMMARY:""",
            input_variables=["text"]
        )

    def load_and_split_pdf(self, file_path: str) -> List:
        """Load PDF and split into chunks."""
        try:
            logger.info(f"Loading PDF from {file_path}")
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            
            # Split the document into chunks
            docs = self.text_splitter.split_documents(pages)
            logger.info(f"Split PDF into {len(docs)} chunks")
            return docs
            
        except Exception as e:
            logger.error(f"Error loading PDF: {str(e)}")
            raise

    def summarize_from_file(self, file_path: str, summary_type: str = "map_reduce") -> dict:
        """Summarize a PDF document from a file."""
        try:
            # Load and split the document
            docs = self.load_and_split_pdf(file_path)
            
            if not docs:
                raise ValueError("No text content found in PDF")
            
            # Choose summarization method
            if summary_type == "map_reduce":
                chain = load_summarize_chain(
                    llm=self.llm,
                    chain_type="map_reduce",
                    map_prompt=self.map_prompt,
                    combine_prompt=self.combine_prompt,
                    verbose=True
                )
            else:  # "stuff" method for shorter documents
                chain = load_summarize_chain(
                    llm=self.llm,
                    chain_type="stuff",
                    verbose=True
                )
            
            # Generate summary
            logger.info("Generating summary...")
            summary = chain.invoke(docs)
            
            # Prepare response
            result = {
                "summary": summary.get("output_text", ""),
                "metadata": {
                    "document_chunks": len(docs),
                    "summarization_method": summary_type,
                    "model": self.llm.model_name
                }
            }
            
            logger.info("Summary generated successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error during summarization: {str(e)}")
            return {"summary": "", "metadata": {}, "error": str(e)}

    def summarize_from_link(self, url: str, summary_type: str = "map_reduce") -> dict:
        """Summarize a PDF document from a URL."""
        # This method would need implementation based on how you want to handle URL documents
        # For demonstration, let's assume it's similar to summarizing from a file.
        # You can implement it as needed.
        logger.info(f"Summarizing from URL: {url}")
        # Here you would need to download the PDF and then call summarize_from_file
        # Assuming we have a way to download the PDF to a temporary file
        # This part is left for you to implement as needed.
        return {"summary": "Summary from URL", "metadata": {}, "error": "Not yet implemented"}

def summarize_pdf(source: str, api_key: Optional[str] = None, method: str = "map_reduce") -> dict:
    """
    Summarize a PDF document or URL using Groq LLM.

    Args:
        source (str): Path to the PDF file or URL link.
        api_key (Optional[str]): Groq API key (optional if set in environment).
        method (str): Summarization method to use ('map_reduce' or 'stuff').

    Returns:
        dict: Contains the summary and metadata.
    """
    # Create an instance of PDFSummarizer
    summarizer = PDFSummarizer(api_key=api_key)

    try:
        # Check if the input source is a URL
        if source.startswith("http"):
            # Summarize from the URL
            result = summarizer.summarize_from_link(source, summary_type=method)
        else:
            # Summarize from the local file
            result = summarizer.summarize_from_file(source, summary_type=method)
        
        # Return the result
        return result
        
    except Exception as e:
        # Handle errors
        print(f"Error: {str(e)}")
        return {"summary": "", "metadata": {}, "error": str(e)}

# Example usage
if __name__ == "__main__":
    result = summarize_pdf(r"C:\Harsh\HackersCrew_Datahack\dsa1.pdf", api_key="your_api_key", method="map_reduce")
    print("\n=== Summary ===")
    print(result["summary"])
    print("\n=== Metadata ===")
    for key, value in result["metadata"].items():
        print(f"{key}: {value}")
