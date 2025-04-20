"""
Document processing functionality for extracting and processing text from PDF documents
"""
import os
import pandas as pd
import PyPDF2
import nltk
from app.config.config import CHUNK_SIZE
from app.utils.text_processing import trim_text, clean_text

class DocumentProcessor:
    """Class for processing PDF documents and extracting content"""
    
    def __init__(self, data_dir):
        """
        Initialize the document processor.
        
        Args:
            data_dir (str): Directory containing PDF documents
        """
        self.data_dir = data_dir
        
    def process_documents(self):
        """
        Process all PDF documents in the data directory.
        
        Returns:
            pd.DataFrame: DataFrame containing document segments
        """
        # Find PDF files in the data directory
        pdf_files = []
        for file in os.listdir(self.data_dir):
            if file.lower().endswith('.pdf'):
                file_path = os.path.join(self.data_dir, file)
                # Use the filename without extension as the document name
                doc_name = os.path.splitext(file)[0]
                pdf_files.append([doc_name, file_path])
        
        # Process each PDF file
        dfs = []
        for doc_name, file_path in pdf_files:
            print(f"Processing {doc_name}...")
            segments = self._extract_segments(doc_name, file_path)
            dfs.append(segments)
        
        # Combine all segments into a single DataFrame
        if dfs:
            return pd.concat(dfs, ignore_index=True)
        else:
            # Return empty DataFrame if no documents found
            return pd.DataFrame(columns=["Article_ID", "Text"])
    
    def _extract_segments(self, doc_name, file_path):
        """
        Extract text segments from a PDF document.
        
        Args:
            doc_name (str): Name of the document
            file_path (str): Path to the PDF file
            
        Returns:
            pd.DataFrame: DataFrame containing document segments
        """
        segments = []
        
        try:
            # Open the PDF file
            with open(file_path, "rb") as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                
                # Extract text from all pages
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                
                # Clean the text
                training_data = clean_text(text)
                
                # Split the text into segments
                sentences = nltk.sent_tokenize(training_data)
                
                # Create segments of CHUNK_SIZE sentences
                for l in range(0, len(sentences), CHUNK_SIZE):
                    trimmed_sentence = trim_text(training_data, l, l + CHUNK_SIZE)
                    
                    # Create a DataFrame row for this segment
                    segments.append(pd.DataFrame({
                        "Article_ID": [f"{doc_name}_{l}"],
                        "Text": [trimmed_sentence]
                    }))
        
        except Exception as e:
            print(f"Error processing {doc_name}: {e}")
        
        # Combine all segments into a single DataFrame
        if segments:
            return pd.concat(segments, ignore_index=True)
        else:
            # Return empty DataFrame if no segments extracted
            return pd.DataFrame(columns=["Article_ID", "Text"]) 