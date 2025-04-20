"""
Chat memory management for PetroRAG
"""
import time

class ChatMemory:
    """Class for managing chat memory/history"""
    
    def __init__(self, max_history=10):
        """
        Initialize the chat memory.
        
        Args:
            max_history (int): Maximum number of exchanges to keep in history
        """
        self.histories = {}  # Dictionary to store chat histories by session ID
        self.max_history = max_history
    
    def add_exchange(self, session_id, query, response):
        """
        Add a query-response exchange to the chat history.
        
        Args:
            session_id (str): Session identifier
            query (str): User query
            response (str): System response
        """
        if session_id not in self.histories:
            self.histories[session_id] = []
        
        # Add the exchange with timestamp
        self.histories[session_id].append({
            'query': query,
            'response': response,
            'timestamp': time.time()
        })
        
        # Trim history if needed
        if len(self.histories[session_id]) > self.max_history:
            self.histories[session_id] = self.histories[session_id][-self.max_history:]
    
    def get_history(self, session_id):
        """
        Get the chat history for a session.
        
        Args:
            session_id (str): Session identifier
            
        Returns:
            list: List of exchanges for the session
        """
        return self.histories.get(session_id, [])
    
    def clear_history(self, session_id):
        """
        Clear the chat history for a session.
        
        Args:
            session_id (str): Session identifier
        """
        if session_id in self.histories:
            del self.histories[session_id]
    
    def format_history_for_prompt(self, session_id, max_tokens=1000):
        """
        Format chat history for inclusion in a prompt.
        
        Args:
            session_id (str): Session identifier
            max_tokens (int): Approximate maximum number of tokens to include
            
        Returns:
            str: Formatted chat history
        """
        history = self.get_history(session_id)
        if not history:
            return ""
        
        formatted_history = "Chat History:\n"
        
        # Start from the most recent exchanges and work backward
        # This is a simple approximation of token count (4 chars ≈ 1 token)
        token_count = 0
        included_exchanges = []
        
        for exchange in reversed(history[:-1]):  # Exclude the most recent exchange
            exchange_text = f"User: {exchange['query']}\nSystem: {exchange['response']}\n"
            estimated_tokens = len(exchange_text) // 4
            
            if token_count + estimated_tokens > max_tokens:
                break
                
            token_count += estimated_tokens
            included_exchanges.append(exchange_text)
        
        # Reverse back to chronological order
        for exchange_text in reversed(included_exchanges):
            formatted_history += exchange_text
        
        return formatted_history 