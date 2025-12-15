"""NLP Agent for processing text-based customer inquiries."""

import re
from typing import Dict, Tuple, Any


class NLPAgent:
    """Agent for natural language processing and understanding."""
    
    def __init__(self):
        """Initialize NLP agent with knowledge base."""
        self.knowledge_base = {
            "pricing": {
                "keywords": ["price", "cost", "pricing", "fee", "charge", "payment"],
                "response": "Our pricing starts at $29/month for basic plan, $79/month for professional, and $199/month for enterprise. All plans include 24/7 support."
            },
            "features": {
                "keywords": ["feature", "functionality", "capability", "what can", "able to"],
                "response": "SmartSupport AI offers multi-agent support, voice AI, NLP processing, 24/7 availability, ticket management, and analytics dashboard."
            },
            "support": {
                "keywords": ["help", "support", "assist", "problem", "issue", "bug"],
                "response": "Our support team is available 24/7 via chat, email at support@smartsupport.ai, or phone at 1-800-SMART-AI."
            },
            "hours": {
                "keywords": ["hours", "available", "when", "open", "schedule"],
                "response": "Our AI agents are available 24/7, 365 days a year. Human support is available Monday-Friday 9am-6pm EST."
            },
            "demo": {
                "keywords": ["demo", "trial", "test", "try"],
                "response": "Yes! We offer a 14-day free trial with full access to all features. No credit card required."
            },
            "integration": {
                "keywords": ["integrat", "api", "connect", "plugin"],  # Use stem to match integration/integrations/integrate
                "response": "We support integrations with Slack, Zendesk, Salesforce, and offer a REST API for custom integrations."
            }
        }
        
        self.greeting_patterns = [
            r'\b(hi|hello|hey|greetings)\b',
            r'\bgood\s+(morning|afternoon|evening)\b'
        ]
        
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a customer query and return appropriate response.
        
        Args:
            query: Customer question or inquiry
            
        Returns:
            Dictionary with response, confidence, and intent
        """
        if not isinstance(query, str) or query is None:
            return {
                "response": "I'm not sure I understand. Could you please rephrase your question? You can ask about pricing, features, support, hours, demos, or integrations.",
                "confidence": 0.0,
                "intent": "unknown"
            }
        
        query_lower = query.lower().strip()
        
        # Check for greetings
        if self._is_greeting(query_lower):
            return {
                "response": "Hello! I'm your AI assistant. How can I help you today?",
                "confidence": 1.0,
                "intent": "greeting"
            }
        
        # Find matching intent
        intent, confidence = self._find_intent(query_lower)
        
        if confidence > 0.0:  # Lower threshold - any match is good
            response = self.knowledge_base[intent]["response"]
            return {
                "response": response,
                "confidence": confidence,
                "intent": intent
            }
        else:
            return {
                "response": "I'm not sure I understand. Could you please rephrase your question? You can ask about pricing, features, support, hours, demos, or integrations.",
                "confidence": 0.0,
                "intent": "unknown"
            }
    
    def _is_greeting(self, text: str) -> bool:
        """Check if text is a greeting."""
        for pattern in self.greeting_patterns:
            if re.search(pattern, text):
                return True
        return False
    
    def _find_intent(self, query: str) -> Tuple[str, float]:
        """Find the best matching intent for the query."""
        best_intent = None
        best_score = 0.0
        best_position = float('inf')
        
        for intent, data in self.knowledge_base.items():
            keywords = data["keywords"]
            matches = 0
            earliest_position = float('inf')
            
            # Check for keyword matches in the query
            for keyword in keywords:
                if keyword in query:
                    matches += 1
                    # Track earliest position of matched keyword
                    pos = query.find(keyword)
                    if pos < earliest_position:
                        earliest_position = pos
            
            if matches > 0:
                # Better scoring: weight by number of matches
                # This gives higher scores for more keyword matches
                score = min(matches / 2.0, 1.0)  # Cap at 1.0
                
                # Use position as tiebreaker - prefer intents with keywords earlier in query
                if score > best_score or (score == best_score and earliest_position < best_position):
                    best_score = score
                    best_intent = intent
                    best_position = earliest_position
        
        return best_intent or "unknown", best_score
    
    def analyze_sentiment(self, text: str) -> str:
        """
        Analyze sentiment of customer message.
        
        Args:
            text: Customer message
            
        Returns:
            Sentiment classification: positive, negative, or neutral
        """
        if not isinstance(text, str) or text is None:
            raise ValueError("Input 'text' must be a non-None string.")
        
        text_lower = text.lower()
        
        positive_words = ["good", "great", "excellent", "thanks", "thank", "love", "amazing", "perfect"]
        negative_words = ["bad", "terrible", "awful", "hate", "poor", "wrong", "issue", "problem"]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
