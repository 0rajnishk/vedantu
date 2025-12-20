# ⚡ QUICK REFERENCE CARD

## Your Setup
```
Sheet ID: 1-aRmuDOSu38Oid975ZiAvS3XER-cpO-ldsmfPz46kP8
API Key: ❌ Not needed (public sheet)
Status: ✅ Ready to use
```

---

## One-Command Start

```bash
python app.py
```

Then visit: `http://localhost:5000/dashboard`

---

## Login Credentials

```
User: agent
Pass: agent123
```

---

## Dashboard Features

| Feature | Shortcut |
|---------|----------|
| View all chats | Dashboard → Table |
| Open chat | Click "Open Chat" button |
| See context | Goes to chat interface → Top section |
| Refresh data | Click "Refresh Sheets" button |

---

## What Shows on Dashboard

```
Sno | Chat ID | Name | Class | Exam | Board | Type | Time | Action
```

---

## What Shows in Chat Interface

### Top Section (Context):
- Previous conversations for this Chat ID
- What user asked (User Intent)
- What bot said (AI Response)
- Topic area (Doubt)

### Main Chat Area:
- Live message history
- Agent can send messages
- Connected/disconnected status

---

## Google Sheet Required Format

**Columns (in order):**
1. Sno
2. Chat ID ⭐
3. Name
4. Type (Parent/Student/Visitor)
5. User Intent
6. AI Response
7. Class
8. Target Exam
9. School Board
10. School Medium
11. Location
12. Doubt
13. Free Content
14. Ranking
15. Agent Transferred
16. Time Stamp
17. Conversation State

---

## API Endpoints

```
GET  /api/chat-sessions              → All chats
GET  /api/chat-context/{id}          → Context for chat ID
POST /api/refresh-sheets             → Refresh cache
POST /api/send-message               → Send message
GET  /api/get-messages/{id}          → Get messages
GET  /api/poll-messages/{id}         → Poll new messages
```

---

## Files Changed

```
✅ app.py                    (Google Sheets integration)
✅ templates/dashboard.html  (New table columns)
✅ templates/chat.html       (Context display)
```

---

## Common Tasks

### Add new chat to dashboard
→ Add row to Google Sheet → Click "Refresh Sheets"

### See previous conversation
→ Open chat → Check top context section

### Update chat context
→ Edit Google Sheet → Click "Refresh Sheets"

---

## Troubleshooting 🔧

| Problem | Solution |
|---------|----------|
| Nothing showing | Sheet not public? Make it public |
| Wrong columns | Check column order matches list above |
| No context | Chat ID might not match exactly |
| Slow loading | Click "Refresh Sheets" to clear cache |
| "No chats" | Add data to Google Sheet |

---

## Testing (Copy-Paste)

### PowerShell:
```powershell
# Get chats
Invoke-RestMethod http://localhost:5000/api/chat-sessions `
  -Method Get -SessionVariable s; Invoke-RestMethod `
  http://localhost:5000/api/chat-sessions -WebSession $s
```

### Or just open:
```
http://localhost:5000/api/chat-sessions
```

---

## Performance

- **Load time**: 1-2 seconds (first time)
- **Cache**: 5 minutes
- **Dashboard refresh**: Every 10 seconds
- **Message poll**: Every 2 seconds

---

## Key Points

✅ No API key needed (sheet is public)  
✅ Two backup methods for fetching data  
✅ Auto-fallback if API fails  
✅ Works offline with cached data  
✅ Real-time message updates  

---

## Next: Customize SHEET_NAME

If your sheet name is NOT "Sheet1":

1. Open Google Sheet
2. Check sheet tab name at bottom
3. Edit `app.py` line 17:
   ```python
   SHEET_NAME = 'Your Sheet Name Here'
   ```
4. Save and restart

---

**Last Updated**: December 20, 2025  
**Ready**: ✅ YES
