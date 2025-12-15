"""Unit tests for Voice Agent."""

import unittest
from backend.agents.voice_agent import VoiceAgent


class TestVoiceAgent(unittest.TestCase):
    """Test cases for Voice Agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = VoiceAgent()
    
    def test_supported_formats(self):
        """Test supported audio formats."""
        self.assertIn('wav', self.agent.supported_formats)
        self.assertIn('mp3', self.agent.supported_formats)
        self.assertIn('ogg', self.agent.supported_formats)
    
    def test_process_audio_success(self):
        """Test successful audio processing."""
        audio_data = "TEST:What is your pricing?"
        result = self.agent.process_audio(audio_data, 'wav')
        
        self.assertTrue(result["success"])
        self.assertEqual(result["text"], "What is your pricing?")
        self.assertEqual(result["format"], "wav")
        self.assertGreater(result["confidence"], 0.9)
    
    def test_process_audio_unsupported_format(self):
        """Test audio processing with unsupported format."""
        audio_data = "TEST:Hello"
        result = self.agent.process_audio(audio_data, 'flac')
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_synthesize_speech(self):
        """Test text-to-speech synthesis."""
        text = "Hello, how can I help you?"
        result = self.agent.synthesize_speech(text)
        
        self.assertTrue(result["success"])
        self.assertIn("audio", result)
        self.assertEqual(result["format"], "wav")
        self.assertGreater(result["duration"], 0)
    
    def test_synthesize_speech_with_voice(self):
        """Test TTS with specific voice."""
        text = "Welcome to SmartSupport AI"
        result = self.agent.synthesize_speech(text, voice="female")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["voice"], "female")
    
    def test_detect_language(self):
        """Test language detection."""
        audio_data = "TEST:Hello"
        language = self.agent.detect_language(audio_data)
        
        self.assertEqual(language, "en")


if __name__ == '__main__':
    unittest.main()
