# Quick Start Guide - Google Sheets Integration

## 5-Minute Setup

### Step 1: Get Your Google Credentials (2 minutes)

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Search for "Google Sheets API" → Enable it
4. Click Credentials → Create API Key → Copy it
5. Open your Google Sheet → Copy the ID from URL: `sheets.googleapis.com/d/{ID}/`

### Step 2: Update app.py (1 minute)

Find this in `app.py`:
```python
GOOGLE_SHEETS_ID = 'your-google-sheet-id-here'
GOOGLE_SHEETS_API_KEY = 'your-google-api-key-here'
SHEET_NAME = 'Sheet1'
```

Replace with your actual values:
```python
GOOGLE_SHEETS_ID = 'abc123def456ghi789jkl'  # Your sheet ID
GOOGLE_SHEETS_API_KEY = 'AIzaSyD_xyz123...'   # Your API key
SHEET_NAME = 'Chat Data'                      # Your sheet name
```

### Step 3: Create Google Sheet (1 minute)

Create a new Google Sheet with these columns in order:
1. Sno
2. Chat ID
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

Add a few sample rows with chat data.

### Step 4: Run the App (1 minute)

```bash
python app.py
```

Visit: `http://localhost:5000/dashboard`

## What You'll See

### Dashboard
- Table with: Sno | Chat ID | Name | Class | Target Exam | School Board | Type | Timestamp | Action
- "Open Chat" button for each row
- "Refresh Sheets" button to sync data

### Chat Interface
- Previous conversation context at the top
- Shows: User Intent, AI Response, Doubt, Conversation State
- Live chat area below
- Agent can respond to customer

## API Quick Reference

**Load all chats:**
```
GET /api/chat-sessions
```

**Load context for a chat:**
```
GET /api/chat-context/{chatId}
```

**Refresh Google Sheets cache:**
```
POST /api/refresh-sheets
```

## Common Issues

| Issue | Solution |
|-------|----------|
| No chats showing | Check API key and Sheet ID in app.py |
| "Unauthorized" error | Make sure you're logged in with agent/admin |
| Context not showing | Verify Chat IDs match between sheet and chat |
| API key error | Regenerate API key in Google Cloud Console |

## File Structure Created

```
vedantu/
├── app.py                    (Updated with Google Sheets)
├── SETUP_GUIDE.md            (Detailed setup guide)
├── UPDATE_SUMMARY.md         (Complete change summary)
├── CONFIG_TEMPLATE.py        (Configuration reference)
├── templates/
│   ├── dashboard.html        (Updated with new columns)
│   └── chat.html             (Updated with context display)
└── requirements.txt          (No changes needed)
```

## Next Steps

1. Read [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed instructions
2. Check [UPDATE_SUMMARY.md](./UPDATE_SUMMARY.md) for all changes made
3. Use [CONFIG_TEMPLATE.py](./CONFIG_TEMPLATE.py) as reference

## Example Data for Testing

Add this to your Google Sheet to test:

| Sno | Chat ID | Name | Type | User Intent | AI Response | Class | Target Exam | School Board |
|-----|---------|------|------|-------------|-------------|-------|------------|--------------|
| 1 | CHAT_001 | Arjun Singh | Student | How to solve quadratic equations? | Use the quadratic formula... | 10 | JEE | CBSE |
| 2 | CHAT_002 | Priya Patel | Parent | Physics concepts for class 12 | Here are key physics topics... | 12 | NEET | CBSE |
| 3 | CHAT_003 | Rohan Kumar | Student | NCERT solutions available? | Yes, all NCERT solutions free on Vedantu | 11 | JEE | ICSE |

## Support

- Check browser console (F12) for errors
- Verify all credentials are correctly entered
- Test API endpoints with Postman or curl
- Review logs in terminal where Flask is running

---

**Last Updated:** December 20, 2025
**Version:** 1.0
