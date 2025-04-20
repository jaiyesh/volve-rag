"""
Main application file for PetroRAG
"""
import os
from flask import Flask, render_template, send_from_directory
import pandas as pd
from app.config.config import DATA_DIR, EMBEDDINGS_FILE, PORT, HOST, DEBUG, SECRET_KEY
from app.core.document_processor import DocumentProcessor
from app.core.embedding_manager import EmbeddingManager
from app.api.routes import api_bp, init_rag_engine
from app.logging.logger import setup_logger

# Create Flask application
app = Flask(__name__, 
            static_folder='app/static',
            template_folder='templates')
app.secret_key = SECRET_KEY

# Set up logging
setup_logger(app)

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')

# Routes
@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    """Serve the favicon"""
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

def initialize_data():
    """
    Initialize data for the application.
    
    - Process documents
    - Create or load embeddings
    - Initialize RAG engine
    """
    app.logger.info('Initializing data...')
    
    # Process documents
    doc_processor = DocumentProcessor(DATA_DIR)
    document_df = doc_processor.process_documents()
    app.logger.info(f'Processed {len(document_df)} document segments')
    
    # Create or load embeddings
    embedding_manager = EmbeddingManager()
    
    if os.path.exists(EMBEDDINGS_FILE):
        app.logger.info('Loading existing embeddings...')
        embeddings = embedding_manager.load_embeddings()
    else:
        app.logger.info('Creating new embeddings...')
        embeddings = embedding_manager.compute_embeddings(document_df)
        embedding_manager.save_embeddings(embeddings)
    
    # Initialize RAG engine
    init_rag_engine(document_df, embeddings)
    app.logger.info('RAG engine initialized')

if __name__ == '__main__':
    # Initialize data
    initialize_data()
    
    # Run the application
    app.run(host=HOST, port=PORT, debug=DEBUG) 