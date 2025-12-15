"""Integration tests for API endpoints."""

import unittest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.api.server import app


class TestAPIEndpoints(unittest.TestCase):
    """Test cases for REST API endpoints."""
    
    def setUp(self):
        """Set up test client."""
        self.app = app
        self.client = self.app.test_client()
        self.app.testing = True
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = self.client.get('/api/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "SmartSupport AI")
    
    def test_chat_endpoint_success(self):
        """Test chat endpoint with valid request."""
        response = self.client.post(
            '/api/chat',
            data=json.dumps({
                "query": "What is your pricing?",
                "session_id": "test-123"
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("response", data)
        self.assertIn("confidence", data)
        self.assertIn("intent", data)
        self.assertEqual(data["session_id"], "test-123")
    
    def test_chat_endpoint_missing_query(self):
        """Test chat endpoint with missing query."""
        response = self.client.post(
            '/api/chat',
            data=json.dumps({}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)
    
    def test_voice_endpoint_success(self):
        """Test voice endpoint with valid request."""
        response = self.client.post(
            '/api/voice',
            data=json.dumps({
                "audio_data": "TEST:What are your features?",
                "format": "wav",
                "session_id": "voice-test-123"
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn("transcription", data)
        self.assertIn("response_text", data)
    
    def test_voice_endpoint_missing_audio(self):
        """Test voice endpoint with missing audio data."""
        response = self.client.post(
            '/api/voice',
            data=json.dumps({}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)
    
    def test_analytics_endpoint(self):
        """Test analytics endpoint."""
        # First make some requests
        self.client.post(
            '/api/chat',
            data=json.dumps({"query": "Hello"}),
            content_type='application/json'
        )
        
        # Get analytics
        response = self.client.get('/api/analytics')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_requests", data)
        self.assertIn("average_response_time_ms", data)
        self.assertGreater(data["total_requests"], 0)
    
    def test_reset_endpoint(self):
        """Test reset endpoint."""
        # Make a request
        self.client.post(
            '/api/chat',
            data=json.dumps({"query": "Hello"}),
            content_type='application/json'
        )
        
        # Reset
        response = self.client.post('/api/reset')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", data)
        
        # Verify analytics are cleared
        analytics_response = self.client.get('/api/analytics')
        analytics_data = json.loads(analytics_response.data)
        self.assertEqual(analytics_data["total_requests"], 0)


if __name__ == '__main__':
    unittest.main()
