"""Agent Orchestrator for coordinating multiple AI agents."""

import time
from typing import Dict, Any
from .nlp_agent import NLPAgent
from .voice_agent import VoiceAgent


class AgentOrchestrator:
    """Orchestrates multiple agents to handle customer service requests."""
    
    def __init__(self):
        """Initialize orchestrator with all agents."""
        self.nlp_agent = NLPAgent()
        self.voice_agent = VoiceAgent()
        self.request_history = []
        
    def handle_text_request(self, query: str, session_id: str = None) -> Dict[str, Any]:
        """
        Handle text-based customer request.
        
        Args:
            query: Customer text query
            session_id: Optional session identifier
            
        Returns:
            Response dictionary with answer and metadata
        """
        start_time = time.time()
        
        # Process with NLP agent
        nlp_result = self.nlp_agent.process_query(query)
        
        # Analyze sentiment
        sentiment = self.nlp_agent.analyze_sentiment(query)
        
        # Calculate response time
        response_time = time.time() - start_time
        
        result = {
            "type": "text",
            "query": query,
            "response": nlp_result["response"],
            "confidence": nlp_result["confidence"],
            "intent": nlp_result["intent"],
            "sentiment": sentiment,
            "response_time_ms": round(response_time * 1000, 2),
            "session_id": session_id,
            "timestamp": time.time()
        }
        
        # Store in history
        self._add_to_history(result)
        
        return result
    
    def handle_voice_request(self, audio_data: str, audio_format: str = 'wav', 
                            session_id: str = None) -> Dict[str, Any]:
        """
        Handle voice-based customer request.
        
        Args:
            audio_data: Base64 encoded audio
            audio_format: Audio format
            session_id: Optional session identifier
            
        Returns:
            Response dictionary with answer and metadata
        """
        start_time = time.time()
        
        # Step 1: Transcribe audio to text
        transcription = self.voice_agent.process_audio(audio_data, audio_format)
        
        if not transcription["success"]:
            return {
                "success": False,
                "error": transcription.get("error", "Transcription failed")
            }
        
        # Step 2: Process transcribed text with NLP
        query_text = transcription["text"]
        nlp_result = self.nlp_agent.process_query(query_text)
        
        # Step 3: Convert response to speech
        tts_result = self.voice_agent.synthesize_speech(nlp_result["response"])
        
        # Calculate response time
        response_time = time.time() - start_time
        
        result = {
            "type": "voice",
            "transcription": query_text,
            "response_text": nlp_result["response"],
            "response_audio": tts_result["audio"],
            "confidence": nlp_result["confidence"],
            "intent": nlp_result["intent"],
            "response_time_ms": round(response_time * 1000, 2),
            "session_id": session_id,
            "timestamp": time.time(),
            "success": True
        }
        
        # Store in history
        self._add_to_history(result)
        
        return result
    
    def get_analytics(self) -> Dict[str, Any]:
        """
        Get analytics about agent performance.
        
        Returns:
            Analytics dictionary with metrics
        """
        if not self.request_history:
            return {
                "total_requests": 0,
                "average_response_time_ms": 0,
                "intent_distribution": {},
                "sentiment_distribution": {}
            }
        
        total_requests = len(self.request_history)
        
        # Calculate average response time
        avg_response_time = sum(
            req.get("response_time_ms", 0) for req in self.request_history
        ) / total_requests
        
        # Intent distribution
        intent_dist = {}
        for req in self.request_history:
            intent = req.get("intent", "unknown")
            intent_dist[intent] = intent_dist.get(intent, 0) + 1
        
        # Sentiment distribution
        sentiment_dist = {}
        for req in self.request_history:
            sentiment = req.get("sentiment", "neutral")
            sentiment_dist[sentiment] = sentiment_dist.get(sentiment, 0) + 1
        
        return {
            "total_requests": total_requests,
            "average_response_time_ms": round(avg_response_time, 2),
            "intent_distribution": intent_dist,
            "sentiment_distribution": sentiment_dist,
            "voice_requests": sum(1 for r in self.request_history if r.get("type") == "voice"),
            "text_requests": sum(1 for r in self.request_history if r.get("type") == "text")
        }
    
    def _add_to_history(self, request: Dict):
        """Add request to history, keeping last 1000 requests."""
        self.request_history.append(request)
        if len(self.request_history) > 1000:
            self.request_history.pop(0)
    
    def clear_history(self):
        """Clear request history."""
        self.request_history = []
