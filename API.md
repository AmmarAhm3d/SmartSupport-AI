# API Documentation

## Base URL
`http://localhost:5000/api`

## Endpoints

### Health Check
Check if the service is running.

**Request:**
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "SmartSupport AI",
  "version": "1.0.0"
}
```

---

### Text Chat
Process a text-based customer inquiry.

**Request:**
```http
POST /api/chat
Content-Type: application/json

{
  "query": "What is your pricing?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "type": "text",
  "query": "What is your pricing?",
  "response": "Our pricing starts at $29/month...",
  "confidence": 0.95,
  "intent": "pricing",
  "sentiment": "neutral",
  "response_time_ms": 12.5,
  "session_id": "session-123",
  "timestamp": 1234567890.123
}
```

**Fields:**
- `query` (required): Customer question
- `session_id` (optional): Session identifier for tracking conversations

---

### Voice Processing
Process a voice-based customer inquiry.

**Request:**
```http
POST /api/voice
Content-Type: application/json

{
  "audio_data": "base64-encoded-audio-data",
  "format": "wav",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "type": "voice",
  "transcription": "What are your features?",
  "response_text": "SmartSupport AI offers...",
  "response_audio": "base64-encoded-audio-response",
  "confidence": 0.95,
  "intent": "features",
  "response_time_ms": 45.2,
  "session_id": "session-123",
  "timestamp": 1234567890.123,
  "success": true
}
```

**Fields:**
- `audio_data` (required): Base64-encoded audio data
- `format` (optional): Audio format (wav, mp3, ogg), defaults to 'wav'
- `session_id` (optional): Session identifier

---

### Analytics
Get platform analytics and performance metrics.

**Request:**
```http
GET /api/analytics
```

**Response:**
```json
{
  "total_requests": 150,
  "average_response_time_ms": 15.5,
  "intent_distribution": {
    "pricing": 45,
    "features": 30,
    "support": 25
  },
  "sentiment_distribution": {
    "positive": 80,
    "neutral": 60,
    "negative": 10
  },
  "voice_requests": 50,
  "text_requests": 100
}
```

---

### Reset Analytics
Clear analytics history (useful for testing).

**Request:**
```http
POST /api/reset
```

**Response:**
```json
{
  "message": "History cleared successfully"
}
```

---

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200 OK`: Successful request
- `400 Bad Request`: Missing required fields or invalid data
- `500 Internal Server Error`: Server-side error

Error response format:
```json
{
  "error": "Error message describing what went wrong"
}
```

---

## Supported Intents

The NLP agent recognizes the following customer intents:

1. **greeting**: Hello, hi, good morning, etc.
2. **pricing**: Questions about costs, plans, fees
3. **features**: Inquiries about capabilities and functionality
4. **support**: Help requests and issue reporting
5. **hours**: Availability and schedule questions
6. **demo**: Trial and testing requests
7. **integration**: API and third-party integration questions

---

## Rate Limiting

Currently, there are no rate limits. In production, consider implementing:
- Per-session rate limiting
- IP-based throttling
- API key authentication
