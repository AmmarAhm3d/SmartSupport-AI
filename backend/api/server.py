"""REST API for SmartSupport AI platform."""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.agents import AgentOrchestrator

app = Flask(__name__)

# Restrict CORS to trusted origins
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*")
if allowed_origins == "*":
    # Allow all for development, but log a warning
    CORS(app)
else:
    CORS(app, origins=[origin.strip() for origin in allowed_origins.split(",")])

# Initialize orchestrator
orchestrator = AgentOrchestrator()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "SmartSupport AI",
        "version": "1.0.0"
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle text-based chat requests.
    
    Expected JSON body:
    {
        "query": "customer question",
        "session_id": "optional-session-id"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "error": "Missing 'query' in request body"
            }), 400
        
        query = data['query']
        
        # Validate query
        if not isinstance(query, str) or len(query) > 1000:
            return jsonify({
                "error": "Invalid query or query too long (maximum 1000 characters allowed)"
            }), 400
        
        session_id = data.get('session_id')
        
        result = orchestrator.handle_text_request(query, session_id)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route('/api/voice', methods=['POST'])
def voice():
    """
    Handle voice-based requests.
    
    Expected JSON body:
    {
        "audio_data": "base64-encoded-audio",
        "format": "wav",
        "session_id": "optional-session-id"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'audio_data' not in data:
            return jsonify({
                "error": "Missing 'audio_data' in request body"
            }), 400
        
        audio_data = data['audio_data']
        
        # Limit: 10 MB base64-encoded audio (~7.5 MB raw)
        MAX_AUDIO_DATA_SIZE = 10 * 1024 * 1024  # 10 MB
        if len(audio_data) > MAX_AUDIO_DATA_SIZE:
            return jsonify({
                "error": "audio_data payload too large (limit is 10 MB base64-encoded)"
            }), 413
        
        audio_format = data.get('format', 'wav')
        session_id = data.get('session_id')
        
        result = orchestrator.handle_voice_request(audio_data, audio_format, session_id)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route('/api/analytics', methods=['GET'])
def analytics():
    """Get platform analytics."""
    try:
        stats = orchestrator.get_analytics()
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset analytics history (for testing)."""
    try:
        orchestrator.clear_history()
        return jsonify({
            "message": "History cleared successfully"
        })
    
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
