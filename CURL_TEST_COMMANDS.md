# Quick Test Commands for Vedantu Chat Dashboard

## Production Endpoint
```
https://vedantu-c-desicrew-2dyglpk7xq-uc.a.run.app/
```

---

## 1. Test Webhook Response Endpoint (N8N Integration)

```bash
curl -X POST https://vedantu-c-desicrew-2dyglpk7xq-uc.a.run.app/api/webhook/response \
  -H "Content-Type: application/json" \
  -d '{
    "chatId": "1139898947",
    "message": "This is a test response from N8N!",
    "sender": "bot"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Response received"
}
```

---

## 2. Test with Different Chat IDs

### Chat ID: 555555
```bash
curl -X POST https://vedantu-c-desicrew-2dyglpk7xq-uc.a.run.app/api/webhook/response \
  -H "Content-Type: application/json" \
  -d '{
    "chatId": "555555",
    "message": "Hello from test - Chat 555555",
    "sender": "bot"
  }'
```

### Chat ID: 5287164993
```bash
curl -X POST https://vedantu-c-desicrew-2dyglpk7xq-uc.a.run.app/api/webhook/response \
  -H "Content-Type: application/json" \
  -d '{
    "chatId": "5287164993",
    "message": "Testing Electromagnetic Induction response",
    "sender": "bot"
  }'
```

---

## 3. Test with Long Message

```bash
curl -X POST https://vedantu-c-desicrew-2dyglpk7xq-uc.a.run.app/api/webhook/response \
  -H "Content-Type: application/json" \
  -d '{
    "chatId": "1139898947",
    "message": "Electromagnetic Induction (EMI) is the process by which a changing magnetic field induces an electric field. When the magnetic flux through a circuit changes, an electromotive force (EMF) is induced. This is the fundamental principle behind transformers, generators, and many other electrical devices. The strength of the induced EMF is proportional to the rate of change of magnetic flux, as described by Faraday'\''s Law of electromagnetic induction.",
    "sender": "bot"
  }'
```

---

## 4. Test Error Case (Missing chatId)

```bash
curl -X POST https://vedantu-c-desicrew-2dyglpk7xq-uc.a.run.app/api/webhook/response \
  -H "Content-Type: application/json" \
  -d '{
    "message": "This should fail",
    "sender": "bot"
  }'
```

**Expected Response (Error):**
```json
{
  "error": "Missing chatId"
}
```

---

## 5. Test with System Sender

```bash
curl -X POST https://vedantu-c-desicrew-2dyglpk7xq-uc.a.run.app/api/webhook/response \
  -H "Content-Type: application/json" \
  -d '{
    "chatId": "1139898947",
    "message": "System message test",
    "sender": "system"
  }'
```

---

## 6. Windows PowerShell Version

If you're using PowerShell on Windows:

```powershell
$uri = "https://vedantu-c-desicrew-2dyglpk7xq-uc.a.run.app/api/webhook/response"
$body = @{
    chatId = "1139898947"
    message = "Test from PowerShell"
    sender = "bot"
} | ConvertTo-Json

Invoke-WebRequest -Uri $uri -Method POST -ContentType "application/json" -Body $body
```

---

## 7. Verify Application is Running

```bash
curl https://vedantu-c-desicrew-2dyglpk7xq-uc.a.run.app/
```

Should redirect to login page (200 status).

---

## 8. Check Auth Status

```bash
curl https://vedantu-c-desicrew-2dyglpk7xq-uc.a.run.app/api/auth/check
```

**Expected Response (Unauthorized):**
```json
{
  "authenticated": false
}
```

---

## How to Use in Production

### Step 1: Test Basic Webhook
Run the first curl command to verify endpoint is working.

### Step 2: Test with Real Chat ID
Use one of the chat IDs from the Google Sheet (1139898947, 555555, 5287164993).

### Step 3: Login & Check Dashboard
1. Go to: `https://vedantu-c-desicrew-2dyglpk7xq-uc.a.run.app/`
2. Login with credentials from terminal
3. Open a chat
4. Send webhook message (via curl)
5. Poll for messages (dashboard automatically does this)
6. Message should appear in chat UI

### Step 4: Use in N8N
Copy the webhook URL and integrate with N8N workflow:
```
https://vedantu-c-desicrew-2dyglpk7xq-uc.a.run.app/api/webhook/response
```

---

## Debugging Tips

### Check Response Headers
```bash
curl -i -X POST https://vedantu-c-desicrew-2dyglpk7xq-uc.a.run.app/api/webhook/response \
  -H "Content-Type: application/json" \
  -d '{"chatId":"1139898947","message":"test","sender":"bot"}'
```

### Verbose Output
```bash
curl -v -X POST https://vedantu-c-desicrew-2dyglpk7xq-uc.a.run.app/api/webhook/response \
  -H "Content-Type: application/json" \
  -d '{"chatId":"1139898947","message":"test","sender":"bot"}'
```

### Save Response to File
```bash
curl -X POST https://vedantu-c-desicrew-2dyglpk7xq-uc.a.run.app/api/webhook/response \
  -H "Content-Type: application/json" \
  -d '{"chatId":"1139898947","message":"test","sender":"bot"}' \
  > response.json
```

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `curl -X POST` | Send webhook response |
| `-H "Content-Type: application/json"` | Set header |
| `-d '{...}'` | JSON body |
| `-i` | Include response headers |
| `-v` | Verbose/debug mode |

---

**Last Updated**: December 20, 2025
