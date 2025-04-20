"""
API routes for the PetroRAG application
"""
from flask import Blueprint, request, jsonify, session
import uuid
from app.core.rag_engine import RAGEngine
from app.config.config import USE_MEMORY

# Create a blueprint for the API
api_bp = Blueprint('api', __name__)

# Global RAG engine instance
rag_engine = None

@api_bp.route('/query', methods=['POST'])
def query():
    """
    Endpoint for querying the RAG system.
    
    Request body:
        {
            "query": "Your question here"
        }
    
    Returns:
        JSON response with the answer
    """
    # Check if RAG engine is initialized
    global rag_engine
    if rag_engine is None:
        return jsonify({"error": "RAG engine not initialized"}), 500
    
    # Get query from request
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Query parameter missing"}), 400
    
    query = data['query']
    
    # Generate answer (stateless mode only)
    try:
        answer = rag_engine.answer_query(query)
        
        response = {
            "answer": answer
        }
            
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/clear-memory', methods=['POST'])
def clear_memory():
    """
    Endpoint for clearing the conversation memory.
    This endpoint is kept for API compatibility but is non-functional in stateless mode.
    
    Returns:
        JSON response with success status
    """
    return jsonify({"success": True, "message": "Memory functionality is disabled"}), 200

def init_rag_engine(document_df, embeddings):
    """
    Initialize the global RAG engine.
    
    Args:
        document_df (pd.DataFrame): DataFrame containing document segments
        embeddings (dict): Dictionary mapping indices to embeddings
    """
    global rag_engine
    rag_engine = RAGEngine(document_df, embeddings) 