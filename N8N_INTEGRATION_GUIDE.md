# N8N Integration Guide - Vedantu Chat Dashboard

## Overview
This guide explains how to integrate N8N workflows with the Vedantu Chat Dashboard application through webhooks.

---

## Architecture

### Flow Diagram

```
┌─────────────────────────┐
│  Chat Dashboard (UI)    │
│  - Agent sends message  │
└────────────┬────────────┘
             │
             └──→ POST /api/send-message
                   ├─ Store message locally
                   └─ Forward to N8N webhook
                        │
                        ▼
            ┌────────────────────────┐
            │   N8N Workflow         │
            │   - Process message    │
            │   - Call AI/APIs       │
            │   - Generate response  │
            └────────┬───────────────┘
                     │
                     └──→ POST /api/webhook/response
                          ├─ Store response
                          └─ Queue for polling
                               │
                               ▼
                   ┌──────────────────────┐
                   │  Chat Dashboard (UI) │
                   │  - Poll messages     │
                   │  - Display response  │
                   └──────────────────────┘
```

---

## Endpoint Details

### `/api/webhook/response` - Receive Bot Response

**HTTP Method**: `POST`

**URL**: `https://vedantu-c-desicrew.run.app/api/webhook/response`
(or `http://localhost:5000/api/webhook/response` for local development)

**Content-Type**: `application/json`

#### Request Body (JSON)

```json
{
  "chatId": "1139898947",
  "message": "Your response text here",
  "sender": "bot"
}
```

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chatId` | string | ✅ Yes | Unique chat session identifier |
| `message` | string | ✅ Yes | The response message to send to the user |
| `sender` | string | ❌ No | Who sent the message (default: `"system"`, use `"bot"` for AI responses) |

#### Response (Success)

**Status Code**: `200 OK`

```json
{
  "success": true,
  "message": "Response received"
}
```

#### Response (Error)

**Status Code**: `400 Bad Request`

```json
{
  "error": "Missing chatId"
}
```

---

## How It Works

### Step 1: Agent Sends Message
```
User Action: Agent types message in chat interface and clicks send
```

### Step 2: Dashboard Forwards to N8N
```javascript
// chat.html sends message
POST /api/send-message
{
  "chatId": "1139898947",
  "message": "User's question here",
  "sender": "agent"
}
```

### Step 3: Dashboard Payload Sent to N8N
```python
# app.py sends to N8N
webhook_url = 'https://vikramautomation.app.n8n.cloud/webhook/vedantu-chat'
payload = {
  'chatId': '1139898947',
  'sender': 'agent',
  'message': 'User question',
  'timestamp': '2025-12-20T10:30:00.000Z',
  'agentId': 'agent'
}
```

### Step 4: N8N Processes & Responds
```
N8N Workflow:
1. Receive message from Dashboard
2. Call AI API (Gemini, etc.)
3. Generate response
4. Send back to Dashboard via webhook
```

### Step 5: N8N Calls Dashboard Webhook
```bash
curl -X POST https://vedantu-c-desicrew.run.app/api/webhook/response \
  -H "Content-Type: application/json" \
  -d '{
    "chatId": "1139898947",
    "message": "This is the AI response",
    "sender": "bot"
  }'
```

### Step 6: Dashboard Stores & Displays
```
- Message stored in pending_responses
- Chat UI polls /api/poll-messages/<chat_id>
- Message appears in chat interface
```

---

## N8N Workflow Example

### Configuration

#### Trigger: Webhook
- **Method**: POST
- **Path**: `/webhook/vedantu-chat`
- **Authentication**: None (public webhook)

#### Input Mapping
Capture these fields from the incoming webhook:

```
{
  "chatId": {{ $json.chatId }},
  "sender": {{ $json.sender }},
  "message": {{ $json.message }},
  "timestamp": {{ $json.timestamp }},
  "agentId": {{ $json.agentId }}
}
```

#### Process (Example Steps)
1. **Receive** webhook from Dashboard
2. **Call AI API** (Gemini, GPT, Sarvam, etc.)
3. **Transform** response
4. **Send Response Back** via HTTP POST

#### Response Step
Use **HTTP Request** node to call Dashboard webhook:

**Method**: POST  
**URL**: `https://vedantu-c-desicrew.run.app/api/webhook/response`

**Body** (JSON):
```json
{
  "chatId": "{{ $json.chatId }}",
  "message": "{{ $json.aiResponse }}",
  "sender": "bot"
}
```

---

## N8N Workflow (JSON Format)

If you want to import this directly into N8N:

```json
{
  "nodes": [
    {
      "parameters": {
        "path": "vedantu-chat"
      },
      "name": "Webhook - Receive Message",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "url": "https://api.gemini.example.com/v1/messages",
        "method": "POST",
        "headers": {
          "Authorization": "Bearer {{ $json.apiKey }}"
        },
        "body": {
          "content": "{{ $json.message }}"
        }
      },
      "name": "Call AI API",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [450, 300]
    },
    {
      "parameters": {
        "url": "https://vedantu-c-desicrew.run.app/api/webhook/response",
        "method": "POST",
        "headers": {
          "Content-Type": "application/json"
        },
        "body": {
          "chatId": "{{ $json.chatId }}",
          "message": "{{ $json.aiResponse }}",
          "sender": "bot"
        }
      },
      "name": "Send Response Back",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [650, 300]
    }
  ],
  "connections": {
    "Webhook - Receive Message": {
      "main": [
        [
          {
            "node": "Call AI API",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Call AI API": {
      "main": [
        [
          {
            "node": "Send Response Back",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

---

## Test the Integration

### Using cURL

```bash
# Test webhook response endpoint
curl -X POST http://localhost:5000/api/webhook/response \
  -H "Content-Type: application/json" \
  -d '{
    "chatId": "1139898947",
    "message": "Hello from N8N!",
    "sender": "bot"
  }'
```

### Expected Response
```json
{
  "success": true,
  "message": "Response received"
}
```

### Using Postman

1. **Create Request**
   - Method: `POST`
   - URL: `http://localhost:5000/api/webhook/response`

2. **Headers**
   - `Content-Type`: `application/json`

3. **Body** (raw JSON)
   ```json
   {
     "chatId": "1139898947",
     "message": "Test message from N8N",
     "sender": "bot"
   }
   ```

4. **Send** and verify response

---

## Error Handling

### Common Errors

#### 1. Missing chatId
**Status**: 400  
**Error**: `{ "error": "Missing chatId" }`  
**Fix**: Include `chatId` in request body

#### 2. Invalid JSON
**Status**: 400  
**Error**: Request body parsing fails  
**Fix**: Ensure valid JSON format, correct headers

#### 3. Server Error
**Status**: 500  
**Error**: Internal server error  
**Fix**: Check server logs, verify endpoint availability

#### 4. Connection Timeout
**Status**: Connection refused  
**Fix**: Verify URL is correct, server is running, firewall allows traffic

---

## Important Fields

### chatId
- **Type**: String
- **Required**: Yes
- **Example**: `"1139898947"`, `"555555"`, `"5287164993"`
- **Format**: Any unique identifier for the chat session
- **Source**: From dashboard chat sessions (Google Sheets)

### message
- **Type**: String
- **Required**: Yes
- **Example**: `"Electromagnetic Induction occurs when..."`
- **Max Length**: No hard limit (keep under 5000 chars for performance)
- **Content**: The actual response text to display

### sender
- **Type**: String
- **Required**: No
- **Default**: `"system"`
- **Allowed Values**: 
  - `"bot"` - AI/bot response
  - `"agent"` - Human agent response
  - `"system"` - System message

---

## Data Flow Example

### Message from Dashboard → N8N

```json
{
  "chatId": "1139898947",
  "sender": "agent",
  "message": "What is Electromagnetic Induction?",
  "timestamp": "2025-12-20T10:30:45.123Z",
  "agentId": "agent"
}
```

### Response from N8N → Dashboard

```json
{
  "chatId": "1139898947",
  "message": "Electromagnetic Induction (EMI) is the process by which a changing magnetic field induces an electric field. When the magnetic flux through a circuit changes, an electromotive force (EMF) is induced.",
  "sender": "bot"
}
```

---

## Security Considerations

### Authentication
- Currently: **No authentication** on `/api/webhook/response`
- Recommendation: Add API key validation for production

### Future Enhancement
```python
# Add this check to app.py
WEBHOOK_API_KEY = os.environ.get('WEBHOOK_API_KEY', 'default-key')

@app.route('/api/webhook/response', methods=['POST'])
def webhook_response():
    api_key = request.headers.get('X-API-Key')
    if not api_key or api_key != WEBHOOK_API_KEY:
        return jsonify({'error': 'Unauthorized'}), 401
    # ... rest of code
```

### In N8N
Add header to request:
```
X-API-Key: {{ $json.apiKey }}
```

---

## Production Deployment

### Endpoint URL
```
https://vedantu-c-desicrew.run.app/api/webhook/response
```

### Rate Limiting
- No built-in rate limiting (add if needed)
- Recommend: Max 100 requests/minute per chatId

### Timeouts
- N8N webhook timeout: 60 seconds (default)
- Dashboard expects response within 5 minutes

---

## Troubleshooting

### Messages not appearing in chat?
1. Verify `chatId` matches active chat
2. Check server logs: `docker logs vedantu-app`
3. Verify webhook response status is 200
4. Check browser console for polling errors

### N8N webhook not triggering?
1. Verify webhook path is correct
2. Check N8N workflow is active
3. Verify incoming data matches expected format
4. Check N8N execution logs

### Response stuck pending?
1. Dashboard polls `/api/poll-messages/<chatId>`
2. Messages stay in queue until fetched
3. Check network tab in browser dev tools

---

## Support & Debugging

### Enable Debug Logging (Server)
```python
# In app.py
import logging
logging.basicConfig(level=logging.DEBUG)
app.logger.debug(f"Webhook response: {data}")
```

### Check Server Logs
```bash
# Docker
docker logs vedantu-app -f

# Local
python app.py  # Shows all print statements
```

### Test Locally
```bash
# Start Flask
python app.py

# In another terminal, test
curl -X POST http://localhost:5000/api/webhook/response \
  -H "Content-Type: application/json" \
  -d '{"chatId":"test123","message":"Hello","sender":"bot"}'
```

---

## Contact & Questions

For questions about the integration:
- Check server logs
- Verify webhook payload format
- Test with cURL/Postman first
- Check browser network tab for request details

---

**Last Updated**: December 20, 2025  
**Version**: 1.0
