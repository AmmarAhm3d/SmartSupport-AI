"""Unit tests for Agent Orchestrator."""

import unittest
from backend.agents.orchestrator import AgentOrchestrator


class TestAgentOrchestrator(unittest.TestCase):
    """Test cases for Agent Orchestrator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.orchestrator = AgentOrchestrator()
    
    def test_initialization(self):
        """Test orchestrator initialization."""
        self.assertIsNotNone(self.orchestrator.nlp_agent)
        self.assertIsNotNone(self.orchestrator.voice_agent)
        self.assertEqual(len(self.orchestrator.request_history), 0)
    
    def test_handle_text_request(self):
        """Test text request handling."""
        result = self.orchestrator.handle_text_request(
            "What is your pricing?",
            session_id="test-session"
        )
        
        self.assertEqual(result["type"], "text")
        self.assertEqual(result["query"], "What is your pricing?")
        self.assertIn("response", result)
        self.assertIn("confidence", result)
        self.assertIn("intent", result)
        self.assertIn("sentiment", result)
        self.assertIn("response_time_ms", result)
        self.assertEqual(result["session_id"], "test-session")
        
        # Check history was updated
        self.assertEqual(len(self.orchestrator.request_history), 1)
    
    def test_handle_voice_request(self):
        """Test voice request handling."""
        result = self.orchestrator.handle_voice_request(
            audio_data="TEST:What are your features?",
            audio_format="wav",
            session_id="test-voice-session"
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["type"], "voice")
        self.assertIn("transcription", result)
        self.assertIn("response_text", result)
        self.assertIn("response_audio", result)
        self.assertIn("confidence", result)
        self.assertIn("intent", result)
        self.assertEqual(result["session_id"], "test-voice-session")
        
        # Check history was updated
        self.assertEqual(len(self.orchestrator.request_history), 1)
    
    def test_get_analytics_empty(self):
        """Test analytics with no requests."""
        analytics = self.orchestrator.get_analytics()
        
        self.assertEqual(analytics["total_requests"], 0)
        self.assertEqual(analytics["average_response_time_ms"], 0)
        self.assertEqual(analytics["intent_distribution"], {})
        self.assertEqual(analytics["sentiment_distribution"], {})
    
    def test_get_analytics_with_requests(self):
        """Test analytics with multiple requests."""
        # Make several requests
        self.orchestrator.handle_text_request("What is your pricing?")
        self.orchestrator.handle_text_request("What features do you offer?")
        self.orchestrator.handle_voice_request("TEST:Tell me about support")
        
        analytics = self.orchestrator.get_analytics()
        
        self.assertEqual(analytics["total_requests"], 3)
        self.assertGreater(analytics["average_response_time_ms"], 0)
        self.assertGreater(len(analytics["intent_distribution"]), 0)
        self.assertEqual(analytics["text_requests"], 2)
        self.assertEqual(analytics["voice_requests"], 1)
    
    def test_clear_history(self):
        """Test clearing request history."""
        self.orchestrator.handle_text_request("Hello")
        self.assertEqual(len(self.orchestrator.request_history), 1)
        
        self.orchestrator.clear_history()
        self.assertEqual(len(self.orchestrator.request_history), 0)
    
    def test_history_limit(self):
        """Test history limit of 1000 requests."""
        # This test would be slow with 1001 requests, so we'll mock it
        # by directly manipulating the history
        for i in range(1001):
            self.orchestrator._add_to_history({"id": i})
        
        # Should only keep 1000 most recent
        self.assertEqual(len(self.orchestrator.request_history), 1000)
        # First item should be id=1 (id=0 was removed)
        self.assertEqual(self.orchestrator.request_history[0]["id"], 1)


if __name__ == '__main__':
    unittest.main()
