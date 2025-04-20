"""
Embedding manager for creating and managing document embeddings
"""
import os
import pickle
import pandas as pd
import numpy as np
from openai import OpenAI
from app.config.config import OPENAI_API_KEY, EMBEDDING_MODEL, EMBEDDINGS_FILE

class EmbeddingManager:
    """Class for creating and managing document embeddings"""
    
    def __init__(self):
        """Initialize the embedding manager"""
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = EMBEDDING_MODEL
        
    def get_embedding(self, text):
        """
        Get an embedding for a given text.
        
        Args:
            text (str): The text to embed
            
        Returns:
            list: The embedding vector
        """
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding
    
    def compute_embeddings(self, df):
        """
        Compute embeddings for all documents in the DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame containing document segments
            
        Returns:
            dict: Dictionary mapping indices to embeddings
        """
        embeddings = {}
        for idx, row in df.iterrows():
            print(f"Creating embedding for document {idx + 1}/{len(df)}...")
            embeddings[idx] = self.get_embedding(row.Text)
        return embeddings
    
    def save_embeddings(self, embeddings, file_path=EMBEDDINGS_FILE):
        """
        Save embeddings to disk.
        
        Args:
            embeddings (dict): Dictionary mapping indices to embeddings
            file_path (str): Path to save the embeddings
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Save embeddings
        with open(file_path, 'wb') as f:
            pickle.dump(embeddings, f)
    
    def load_embeddings(self, file_path=EMBEDDINGS_FILE):
        """
        Load embeddings from disk.
        
        Args:
            file_path (str): Path to load the embeddings from
            
        Returns:
            dict: Dictionary mapping indices to embeddings
        """
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        return None 