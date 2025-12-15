"""Unit tests for NLP Agent."""

import unittest
from backend.agents.nlp_agent import NLPAgent


class TestNLPAgent(unittest.TestCase):
    """Test cases for NLP Agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = NLPAgent()
    
    def test_greeting_detection(self):
        """Test greeting detection."""
        result = self.agent.process_query("Hello")
        self.assertEqual(result["intent"], "greeting")
        self.assertIn("Hello", result["response"])
        
        result = self.agent.process_query("Hi there")
        self.assertEqual(result["intent"], "greeting")
    
    def test_pricing_intent(self):
        """Test pricing intent detection."""
        queries = [
            "What is your pricing?",
            "How much does it cost?",
            "Tell me about your fees"
        ]
        
        for query in queries:
            result = self.agent.process_query(query)
            self.assertEqual(result["intent"], "pricing")
            self.assertIn("$29", result["response"])
            self.assertGreater(result["confidence"], 0.3)
    
    def test_features_intent(self):
        """Test features intent detection."""
        result = self.agent.process_query("What features do you offer?")
        self.assertEqual(result["intent"], "features")
        self.assertIn("multi-agent", result["response"].lower())
    
    def test_support_intent(self):
        """Test support intent detection."""
        result = self.agent.process_query("I need help with an issue")
        self.assertEqual(result["intent"], "support")
        self.assertIn("24/7", result["response"])
    
    def test_hours_intent(self):
        """Test hours intent detection."""
        result = self.agent.process_query("When are you available?")
        self.assertEqual(result["intent"], "hours")
        self.assertIn("24/7", result["response"])
    
    def test_demo_intent(self):
        """Test demo intent detection."""
        result = self.agent.process_query("Can I try a demo?")
        self.assertEqual(result["intent"], "demo")
        self.assertIn("trial", result["response"].lower())
    
    def test_integration_intent(self):
        """Test integration intent detection."""
        result = self.agent.process_query("What integrations do you support?")
        self.assertEqual(result["intent"], "integration")
        self.assertIn("API", result["response"])
    
    def test_unknown_query(self):
        """Test unknown query handling."""
        result = self.agent.process_query("xyz random stuff abc")
        self.assertEqual(result["intent"], "unknown")
        self.assertEqual(result["confidence"], 0.0)
    
    def test_sentiment_positive(self):
        """Test positive sentiment detection."""
        sentiment = self.agent.analyze_sentiment("This is great! Thank you!")
        self.assertEqual(sentiment, "positive")
    
    def test_sentiment_negative(self):
        """Test negative sentiment detection."""
        sentiment = self.agent.analyze_sentiment("This is terrible and awful")
        self.assertEqual(sentiment, "negative")
    
    def test_sentiment_neutral(self):
        """Test neutral sentiment detection."""
        sentiment = self.agent.analyze_sentiment("What is your pricing?")
        self.assertEqual(sentiment, "neutral")


if __name__ == '__main__':
    unittest.main()
