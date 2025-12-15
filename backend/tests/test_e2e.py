"""
Comprehensive end-to-end test for SmartSupport AI platform.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.agents import NLPAgent, AgentOrchestrator


class TestE2ESmartSupportAI(unittest.TestCase):
    """End-to-end integration tests."""
    
    def setUp(self):
        """Set up test orchestrator."""
        self.orchestrator = AgentOrchestrator()
    
    def test_complete_text_conversation(self):
        """Test a complete customer support conversation."""
        # Greeting
        result = self.orchestrator.handle_text_request("Hello!")
        self.assertEqual(result["intent"], "greeting")
        
        # Inquiry about pricing
        result = self.orchestrator.handle_text_request("What is your pricing?")
        self.assertEqual(result["intent"], "pricing")
        self.assertIn("$29", result["response"])
        
        # Inquiry about features
        result = self.orchestrator.handle_text_request("What features do you offer?")
        self.assertEqual(result["intent"], "features")
        
        # Positive feedback
        result = self.orchestrator.handle_text_request("That's great, thank you!")
        self.assertEqual(result["sentiment"], "positive")
        
        # Verify analytics
        analytics = self.orchestrator.get_analytics()
        self.assertEqual(analytics["total_requests"], 4)
        self.assertEqual(analytics["text_requests"], 4)
        self.assertGreater(analytics["average_response_time_ms"], 0)
    
    def test_voice_to_text_flow(self):
        """Test voice input processing flow."""
        # Voice request
        result = self.orchestrator.handle_voice_request(
            "TEST:What are your integration options?",
            "wav"
        )
        
        self.assertTrue(result["success"])
        self.assertIn("integration", result["transcription"].lower())
        self.assertIn("response_text", result)
        self.assertIn("response_audio", result)
    
    def test_multi_modal_session(self):
        """Test mixing text and voice in the same session."""
        session_id = "test-multi-modal-123"
        
        # Start with text
        text_result = self.orchestrator.handle_text_request(
            "What is your pricing?",
            session_id=session_id
        )
        self.assertEqual(text_result["session_id"], session_id)
        
        # Continue with voice
        voice_result = self.orchestrator.handle_voice_request(
            "TEST:Tell me about support options",
            "wav",
            session_id=session_id
        )
        self.assertEqual(voice_result["session_id"], session_id)
        
        # Verify both requests tracked
        analytics = self.orchestrator.get_analytics()
        self.assertGreaterEqual(analytics["text_requests"], 1)
        self.assertGreaterEqual(analytics["voice_requests"], 1)
    
    def test_nlp_accuracy(self):
        """Test NLP agent accuracy on various queries."""
        test_cases = [
            ("How much does it cost?", "pricing"),
            ("What can your platform do?", "features"),
            ("I need technical support", "support"),
            ("Are you available on weekends?", "hours"),
            ("Can I test it first?", "demo"),
            ("Do you integrate with Slack?", "integration"),
        ]
        
        for query, expected_intent in test_cases:
            result = self.orchestrator.handle_text_request(query)
            self.assertEqual(
                result["intent"], 
                expected_intent,
                f"Query '{query}' should match intent '{expected_intent}'"
            )
    
    def test_sentiment_analysis_accuracy(self):
        """Test sentiment analysis accuracy."""
        nlp_agent = NLPAgent()
        
        test_cases = [
            ("This is amazing! Thank you so much!", "positive"),
            ("I'm having terrible issues with your service", "negative"),
            ("What is the current status?", "neutral"),
        ]
        
        for text, expected_sentiment in test_cases:
            sentiment = nlp_agent.analyze_sentiment(text)
            self.assertEqual(
                sentiment,
                expected_sentiment,
                f"Text '{text}' should have sentiment '{expected_sentiment}'"
            )
    
    def test_performance_requirements(self):
        """Test that system meets performance requirements."""
        # Make multiple requests and check average response time
        for i in range(10):
            self.orchestrator.handle_text_request("What is your pricing?")
        
        analytics = self.orchestrator.get_analytics()
        
        # Response time should be very fast (< 100ms for simple queries)
        self.assertLess(
            analytics["average_response_time_ms"],
            100,
            "Average response time should be under 100ms"
        )
    
    def test_scale_handling(self):
        """Test system can handle multiple requests."""
        # Simulate 100 customer requests
        for i in range(100):
            self.orchestrator.handle_text_request(f"Query number {i}")
        
        analytics = self.orchestrator.get_analytics()
        self.assertEqual(analytics["total_requests"], 100)


if __name__ == '__main__':
    unittest.main()
