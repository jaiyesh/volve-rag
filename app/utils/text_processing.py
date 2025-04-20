"""
Text processing utilities for the PetroRAG application
"""
import nltk
import numpy as np

# Download NLTK data if needed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def trim_text(text, n_start, n_end):
    """
    Trim text to a specific range of sentences.
    
    Args:
        text (str): The text to trim
        n_start (int): The start index of the sentences to keep
        n_end (int): The end index of the sentences to keep
        
    Returns:
        str: The trimmed text
    """
    sentences = nltk.sent_tokenize(text)
    trimmed_sentences = sentences[n_start:n_end]
    trimmed_sentence = " ".join(trimmed_sentences)
    return trimmed_sentence

def clean_text(text):
    """
    Clean text by removing unnecessary whitespace and line breaks.
    
    Args:
        text (str): The text to clean
        
    Returns:
        str: The cleaned text
    """
    return text.replace("\n", " ").strip()

def vector_similarity(x, y):
    """
    Calculate the dot product between two vectors.
    
    Args:
        x (list or numpy.ndarray): First vector
        y (list or numpy.ndarray): Second vector
        
    Returns:
        float: The similarity score
    """
    return np.dot(np.array(x), np.array(y)) 