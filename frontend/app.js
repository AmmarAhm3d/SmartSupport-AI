// SmartSupport AI Frontend Application

const API_BASE_URL = 'http://localhost:5000/api';
let sessionId = generateSessionId();

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadAnalytics();
});

function setupEventListeners() {
    const sendBtn = document.getElementById('sendBtn');
    const userInput = document.getElementById('userInput');
    const voiceBtn = document.getElementById('voiceBtn');
    const refreshBtn = document.getElementById('refreshBtn');

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    voiceBtn.addEventListener('click', handleVoiceInput);
    refreshBtn.addEventListener('click', loadAnalytics);
}

async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const query = userInput.value.trim();

    if (!query) return;

    // Display user message
    addMessage(query, 'user');
    userInput.value = '';

    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                session_id: sessionId
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Display bot response
            addMessage(data.response, 'bot', {
                confidence: data.confidence,
                intent: data.intent,
                responseTime: data.response_time_ms
            });

            // Refresh analytics
            loadAnalytics();
        } else {
            addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        }
    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, I could not connect to the server. Please ensure the backend is running.', 'bot');
    }
}

async function handleVoiceInput() {
    // Simulate voice input for demo
    addMessage('🎤 Voice input (simulated): "What are your pricing options?"', 'user');
    
    try {
        // Simulate voice request with test data
        const response = await fetch(`${API_BASE_URL}/voice`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                audio_data: 'TEST:What are your pricing options?',
                format: 'wav',
                session_id: sessionId
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            addMessage(data.response_text, 'bot', {
                confidence: data.confidence,
                intent: data.intent,
                responseTime: data.response_time_ms,
                type: 'voice'
            });

            // Refresh analytics
            loadAnalytics();
        } else {
            addMessage('Sorry, voice processing failed. Please try text input.', 'bot');
        }
    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, I could not process voice input. Please try again.', 'bot');
    }
}

function addMessage(text, sender, metadata = {}) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    let metaInfo = '';
    if (metadata.confidence !== undefined) {
        metaInfo += `<div class="message-meta">
            Confidence: ${(metadata.confidence * 100).toFixed(0)}% | 
            Intent: ${metadata.intent} | 
            Response: ${metadata.responseTime}ms
            ${metadata.type === 'voice' ? ' | 🎤 Voice' : ''}
        </div>`;
    }

    messageDiv.innerHTML = `
        <div class="message-content">
            <strong>${sender === 'user' ? 'You' : 'AI Assistant'}:</strong> ${text}
            ${metaInfo}
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function loadAnalytics() {
    try {
        const response = await fetch(`${API_BASE_URL}/analytics`);
        const data = await response.json();

        if (response.ok) {
            updateAnalyticsDashboard(data);
        }
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

function updateAnalyticsDashboard(data) {
    // Update metrics
    document.getElementById('totalRequests').textContent = data.total_requests || 0;
    document.getElementById('avgResponseTime').textContent = 
        data.average_response_time_ms ? `${data.average_response_time_ms.toFixed(2)}ms` : '0ms';
    document.getElementById('textRequests').textContent = data.text_requests || 0;
    document.getElementById('voiceRequests').textContent = data.voice_requests || 0;

    // Update intent chart
    updateChart('intentChart', data.intent_distribution || {});

    // Update sentiment chart
    updateChart('sentimentChart', data.sentiment_distribution || {});
}

function updateChart(containerId, chartData) {
    const container = document.getElementById(containerId);
    
    if (Object.keys(chartData).length === 0) {
        container.innerHTML = '<div class="loading">No data yet</div>';
        return;
    }

    const total = Object.values(chartData).reduce((a, b) => a + b, 0);
    
    let html = '';
    for (const [label, value] of Object.entries(chartData)) {
        const percentage = (value / total) * 100;
        html += `
            <div class="chart-bar">
                <div class="chart-label">${label}</div>
                <div class="chart-bar-fill" style="width: ${percentage}%">
                    <div class="chart-bar-value">${value}</div>
                </div>
            </div>
        `;
    }

    container.innerHTML = html;
}

function generateSessionId() {
    return 'session_' + Math.random().toString(36).substring(2, 11);
}
