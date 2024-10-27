import requests
import os
from dotenv import load_dotenv
from typing import List, Optional

class PDFSummarizer:
    def __init__(self, api_key: Optional[str] = None):
        load_dotenv()
        
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

    def download_pdf_from_link(self, link: str, save_path: str = "downloaded_pdf.pdf") -> str:
        """
        Download PDF from a provided link.
        
        Args:
            link (str): URL of the PDF file.
            save_path (str): Path where the downloaded PDF will be saved.
        
        Returns:
            str: Path to the saved PDF file.
        """
        try:
            logger.info(f"Downloading PDF from {link}")
            response = requests.get(link)
            response.raise_for_status()  # Ensure we handle errors

            with open(save_path, "wb") as f:
                f.write(response.content)
            
            logger.info(f"PDF successfully downloaded to {save_path}")
            return save_path
        
        except Exception as e:
            logger.error(f"Error downloading PDF: {str(e)}")
            raise

    def summarize_from_link(self, link: str, summary_type: str = "map_reduce", save_path: str = "downloaded_pdf.pdf") -> dict:
        """
        Summarize a PDF from a URL.
        
        Args:
            link (str): URL of the PDF file.
            summary_type (str): Type of summarization ('map_reduce' or 'stuff').
            save_path (str): Local path to save the downloaded PDF.
        
        Returns:
            dict: Contains the summary and metadata.
        """
        try:
            # Download the PDF from the link
            pdf_path = self.download_pdf_from_link(link, save_path)
            
            # Summarize the downloaded PDF
            return self.summarize(pdf_path, summary_type=summary_type)
        
        except Exception as e:
            logger.error(f"Error summarizing PDF from link: {str(e)}")
            raise

def main():
    """Example usage of the PDFSummarizer."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Summarize a PDF document using Groq LLM")
    parser.add_argument("source", help="Path to the PDF file or URL link")
    parser.add_argument("--api_key", help="Groq API key (optional if set in environment)", default=None)
    parser.add_argument("--method", choices=["map_reduce", "stuff"], default="map_reduce",
                      help="Summarization method to use")
    
    args = parser.parse_args()
    
    try:
        summarizer = PDFSummarizer(api_key=args.api_key)

        # Check if the input is a URL or a local file path
        if args.source.startswith("http"):
            result = summarizer.summarize_from_link(args.source, summary_type=args.method)
        else:
            result = summarizer.summarize(args.source, summary_type=args.method)
        
        print("\n=== Summary ===")
        print(result["summary"])
        print("\n=== Metadata ===")
        for key, value in result["metadata"].items():
            print(f"{key}: {value}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
