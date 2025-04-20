# PetroRAG

A Retrieval Augmented Generation (RAG) system designed specifically for petroleum engineering reports. PetroRAG processes PDF reports, breaks them into manageable segments, and provides a conversational interface for querying information from these documents.

## Features

- PDF document processing and text extraction
- Text chunking and embedding generation
- Semantic search for finding relevant information
- Conversational interface for asking questions about petroleum engineering reports
- User-friendly web interface
- Conversation memory using LangChain for context-aware responses

## Quick Start

### Prerequisites

- Python 3.8 or higher
- An OpenAI API key

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/petrorag.git
   cd petrorag
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on the `.env-sample` and add your OpenAI API key:
   ```
   cp .env-sample .env
   ```
   Then edit the `.env` file with your text editor to add your OpenAI API key.

5. Place your PDF reports in the `data` directory.

### Running the Application

Run the main application:
```
python app.py
```

The application will process your PDF documents, generate embeddings, and start a web server. Access the chat interface at http://127.0.0.1:5000.

## Project Structure

- `app/` - Main application package
  - `api/` - API endpoints
  - `core/` - Core functionality including RAG engine and chat memory
  - `data/` - Data processing utilities
  - `models/` - Database models
  - `utils/` - Utility functions
  - `config/` - Configuration
  - `logging/` - Logging configuration
  - `static/` - Static files (CSS, JavaScript)
- `templates/` - HTML templates
- `data/` - Directory for storing PDF reports
- `logs/` - Application logs

## Usage

1. Place your petroleum engineering PDF reports in the `data` directory.
2. Start the application.
3. Open your browser and go to http://127.0.0.1:5000.
4. Ask questions about the reports in the chat interface.

## Conversation Memory

PetroRAG uses LangChain's conversation memory capabilities to maintain context between user interactions. This allows the chatbot to:

- Remember previous questions and answers
- Provide more coherent responses to follow-up questions
- Understand references to earlier parts of the conversation

The memory feature can be enabled or disabled via the `USE_MEMORY` environment variable in your `.env` file:

```
USE_MEMORY=True  # Enable conversation memory
MAX_HISTORY=10   # Maximum number of conversation exchanges to remember
MEMORY_MAX_TOKENS=1000  # Maximum tokens to use for memory context
```

You can clear the conversation memory at any time by clicking the "Clear Chat" button in the interface.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 