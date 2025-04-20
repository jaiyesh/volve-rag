"""
RAG (Retrieval Augmented Generation) engine for the PetroRAG application
"""
import pandas as pd
import numpy as np
from openai import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from app.config.config import OPENAI_API_KEY, LLM_MODEL, MAX_CONTEXT_SECTIONS, USE_MEMORY, MEMORY_MAX_TOKENS
from app.core.embedding_manager import EmbeddingManager
from app.utils.text_processing import vector_similarity

class RAGEngine:
    """Class for the RAG engine"""
    
    def __init__(self, document_df=None, embeddings=None):
        """
        Initialize the RAG engine.
        
        Args:
            document_df (pd.DataFrame, optional): DataFrame containing document segments
            embeddings (dict, optional): Dictionary mapping indices to embeddings
        """
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.embedding_manager = EmbeddingManager()
        self.document_df = document_df
        self.embeddings = embeddings
        
        # Initialize LangChain components
        self.llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name=LLM_MODEL)
        
        # Dictionary to store conversation chains by session ID
        self.conversations = {}
    
    def get_conversation_chain(self, session_id):
        """
        Get or create a conversation chain for a session.
        
        Args:
            session_id (str): Session identifier
            
        Returns:
            ConversationChain: Conversation chain for the session
        """
        if session_id not in self.conversations:
            # Define prompt template with context
            template = """
            You are a helpful assistant specializing in petroleum engineering.
            
            {history}
            
            Context:
            {context}
            
            Human: {input}
            AI Assistant:"""
            
            prompt = PromptTemplate(
                input_variables=["history", "context", "input"],
                template=template
            )
            
            # Initialize memory with correct configuration to match prompt variables
            memory = ConversationBufferMemory(
                return_messages=True, 
                ai_prefix="AI Assistant", 
                human_prefix="Human",
                memory_key="history"
            )
            
            # Create conversation chain with input variables mapping
            conversation = ConversationChain(
                llm=self.llm,
                prompt=prompt,
                memory=memory,
                verbose=False,
                input_key="input"
            )
            
            self.conversations[session_id] = conversation
        
        return self.conversations[session_id]
    
    def find_relevant_documents(self, query, top_n=MAX_CONTEXT_SECTIONS):
        """
        Find the most relevant document sections for a query.
        
        Args:
            query (str): The query to find relevant documents for
            top_n (int, optional): Number of top documents to return
            
        Returns:
            list: List of (similarity_score, document_index) tuples
        """
        # Get query embedding
        query_embedding = self.embedding_manager.get_embedding(query)
        
        # Calculate similarities
        document_similarities = sorted([
            (vector_similarity(query_embedding, doc_embedding), doc_index)
            for doc_index, doc_embedding in self.embeddings.items()
        ], reverse=True)
        
        # Return top N results
        return document_similarities[:top_n]
    
    def extract_context_sections(self, query):
        """
        Extract relevant context sections for a query.
        
        Args:
            query (str): The user's query
            
        Returns:
            str: Formatted context sections
        """
        # Find relevant documents
        relevant_docs = self.find_relevant_documents(query)
        
        # Extract the text of relevant documents
        context_sections = [
            self.document_df.loc[doc_idx].Text.replace("\n", " ")
            for _, doc_idx in relevant_docs
        ]
        
        # Format context sections
        formatted_context = ""
        for i, section in enumerate(context_sections):
            formatted_context += f"Document {i+1}:\n{section}\n\n"
        
        return formatted_context
    
    def answer_query(self, query, session_id=None):
        """
        Answer a query using the RAG pipeline.
        
        Args:
            query (str): The user's query
            session_id (str, optional): Session identifier for memory
            
        Returns:
            str: The generated answer
        """
        # If no session ID is provided or memory is disabled, use stateless mode
        if session_id is None or not USE_MEMORY:
            return self._answer_query_stateless(query)
        
        try:
            # Extract context
            context = self.extract_context_sections(query)
            
            # Get conversation chain for session
            conversation = self.get_conversation_chain(session_id)
            
            # Generate answer using conversation chain with context
            # Pass input and context separately to match prompt template
            response = conversation.predict(input=query, context=context)
            
            return response
        except Exception as e:
            import traceback
            error_msg = f"Error in memory-based query: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)  # Print to console
            raise Exception(f"Memory processing error: {str(e)}")
    
    def _answer_query_stateless(self, query):
        """
        Answer a query without using memory (stateless mode).
        
        Args:
            query (str): The user's query
            
        Returns:
            str: The generated answer
        """
        # Find relevant documents
        relevant_docs = self.find_relevant_documents(query)
        
        # Extract the text of relevant documents
        context_sections = [
            self.document_df.loc[doc_idx].Text.replace("\n", " ")
            for _, doc_idx in relevant_docs
        ]
        
        # Construct prompt
        prompt = self._construct_stateless_prompt(query, context_sections)
        
        # Generate answer
        completion = self.client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant specializing in petroleum engineering."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return completion.choices[0].message.content
    
    def _construct_stateless_prompt(self, query, context_sections):
        """
        Construct a prompt for stateless mode.
        
        Args:
            query (str): The user's query
            context_sections (list): List of context sections to include
            
        Returns:
            str: The constructed prompt
        """
        # Create the header
        header = (
            "Answer the question as truthfully as possible using the provided context, "
            "and if the answer is not contained within the text below, say \"I don't Know.\"\n\n"
            "Context:\n"
        )
        
        # Add context sections
        sections_text = ""
        for section in context_sections:
            sections_text += f"\n* {section}\n"
        
        # Combine everything into a prompt
        prompt = header + sections_text + f"\n\nQuestion: {query}\nAnswer:"
        
        return prompt
    
    def clear_memory(self, session_id):
        """
        Clear memory for a session.
        
        Args:
            session_id (str): Session identifier
        """
        if session_id in self.conversations:
            self.conversations[session_id].memory.clear()
            # Optionally, remove the conversation chain completely
            del self.conversations[session_id] 