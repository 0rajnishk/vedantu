# ✅ DEPLOYMENT CHECKLIST

## Pre-Launch Verification

### Google Sheet Setup
- [ ] Sheet is public (anyone with link can view)
- [ ] First row contains headers
- [ ] Columns in exact order:
  - [ ] 1. Sno
  - [ ] 2. Chat ID (required)
  - [ ] 3. Name
  - [ ] 4. Type (Parent/Student/Visitor)
  - [ ] 5. User Intent
  - [ ] 6. AI Response
  - [ ] 7. Class
  - [ ] 8. Target Exam
  - [ ] 9. School Board
  - [ ] 10. School Medium
  - [ ] 11. Location
  - [ ] 12. Doubt
  - [ ] 13. Free Content
  - [ ] 14. Ranking
  - [ ] 15. Agent Transferred
  - [ ] 16. Time Stamp
  - [ ] 17. Conversation State
- [ ] At least one row of test data added

### Code Configuration
- [ ] app.py has correct GOOGLE_SHEETS_ID: `1-aRmuDOSu38Oid975ZiAvS3XER-cpO-ldsmfPz46kP8`
- [ ] app.py has GOOGLE_SHEETS_API_KEY = '' (empty)
- [ ] app.py SHEET_NAME = 'Sheet1' (or your sheet name)
- [ ] app.py syntax verified ✅

### Files Updated
- [ ] app.py - Google Sheets integration
- [ ] templates/dashboard.html - New table layout
- [ ] templates/chat.html - Context display

### Dependencies
- [ ] requirements.txt has: Flask, requests, Werkzeug
- [ ] Run: `pip install -r requirements.txt`

### Testing
- [ ] Python syntax check passed
- [ ] Flask imports successfully
- [ ] No circular imports
- [ ] Can connect to Google Sheets

---

## Launch Procedure

### Step 1: Verify Sheet
```
✅ Go to your sheet: 
   https://docs.google.com/spreadsheets/d/1-aRmuDOSu38Oid975ZiAvS3XER-cpO-ldsmfPz46kP8/
✅ Check it's public
✅ Verify columns are correct
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Application
```bash
python app.py
```

Expected output:
```
============================================================
Flask Server Starting...
============================================================

Valid Credentials:
  User ID: admin
  Password: password123
  User ID: agent
  Password: agent123

============================================================
Server running on: http://localhost:5000
============================================================
```

### Step 4: Test Dashboard
```
1. Open: http://localhost:5000/dashboard
2. Login: agent / agent123
3. Verify table shows with columns: Sno | Chat ID | Name | Class | Exam | Board | Type | Time | Action
4. Click "Refresh Sheets" - should show data
```

### Step 5: Test Chat Interface
```
1. Click "Open Chat" on any row
2. Verify previous context shows at top
3. Check User Intent, AI Response, Doubt displayed
4. Verify chat message area works
```

### Step 6: Test API Endpoints
```
1. Get all chats: GET /api/chat-sessions
2. Get context: GET /api/chat-context/CHAT_001
3. Refresh: POST /api/refresh-sheets
```

---

## Troubleshooting During Launch

### Issue: "Sheet not found"
```
Solution:
1. Verify Sheet ID is correct
2. Check SHEET_NAME matches exact sheet name
3. Make sheet public
4. Click "Refresh Sheets" button
```

### Issue: "No columns showing"
```
Solution:
1. Check column names are EXACT match
2. Verify column order is correct
3. Ensure first row is headers
4. Check no merged cells in header row
```

### Issue: "Connection error"
```
Solution:
1. Check internet connection
2. Verify Google Sheet is accessible
3. Try "Refresh Sheets" button
4. Check firewall/proxy settings
```

### Issue: "Context not loading"
```
Solution:
1. Verify Chat ID is filled in sheet
2. Check Chat ID matches exactly (case-sensitive)
3. Verify User Intent/AI Response have data
4. Try manual refresh
```

---

## Performance Verification

### Dashboard Load Time
- [ ] First load: 1-2 seconds (acceptable)
- [ ] Subsequent: <500ms (cached)

### Message Polling
- [ ] Messages appear within 2-3 seconds

### Cache Refresh
- [ ] "Refresh Sheets" clears cache
- [ ] New data appears after refresh

---

## Security Checklist

- [ ] Change VALID_CREDENTIALS in production:
  ```python
  VALID_CREDENTIALS = {
      'admin': 'your-new-password',
      'agent': 'your-new-password'
  }
  ```

- [ ] Keep N8N webhook URL private (already in code)
- [ ] Only share dashboard link with authorized agents
- [ ] Regularly update passwords
- [ ] Monitor access logs

---

## Maintenance Tasks

### Weekly
- [ ] Check Google Sheet for new data
- [ ] Verify dashboard loads correctly
- [ ] Monitor error logs in console

### Monthly
- [ ] Review conversation history
- [ ] Update agent credentials
- [ ] Check for any data inconsistencies
- [ ] Backup Google Sheet data

### As Needed
- [ ] Add new columns to sheet
- [ ] Update agent credentials
- [ ] Modify conversation rules
- [ ] Fix any reported issues

---

## Documentation Files Created

| File | Purpose |
|------|---------|
| COMPLETE_SETUP.md | Full setup guide (this file) |
| QUICK_REF.md | Quick reference card |
| SETUP_GUIDE.md | Detailed setup instructions |
| QUICK_START.md | 5-minute quick start |
| SHEET_CONFIG.md | Your specific configuration |
| CONFIG_TEMPLATE.py | Configuration reference |
| test_api.sh | Bash test script |
| test_api.ps1 | PowerShell test script |

---

## Support Contact Points

### Debug Information to Collect
```
1. Browser console errors (F12)
2. Flask console output
3. Network tab in DevTools
4. API response status code
5. Google Sheet structure screenshot
```

### Common Support Tasks
```
1. "How to add new chat?" → Add row to Google Sheet
2. "Context not showing?" → Check Chat ID matches
3. "Slow dashboard?" → Click "Refresh Sheets"
4. "Can't login?" → Check agent credentials
5. "Messages not sending?" → Verify N8N webhook
```

---

## Success Criteria

### Dashboard ✅
- [ ] Loads without errors
- [ ] Shows all chats from Google Sheet
- [ ] 9 columns display correctly
- [ ] Refresh button works
- [ ] Click "Open Chat" navigates to chat interface

### Chat Interface ✅
- [ ] Previous context displays at top
- [ ] Shows User Intent, AI Response, Doubt
- [ ] Message area functional
- [ ] Agent can send messages
- [ ] Connection status shows

### API ✅
- [ ] /api/chat-sessions returns data
- [ ] /api/chat-context/{id} returns context
- [ ] /api/refresh-sheets clears cache
- [ ] Authentication working
- [ ] Error handling working

---

## Final Verification

```bash
# Run these commands to verify:

# 1. Check Python syntax
python -m py_compile app.py

# 2. Check imports
python -c "from app import *; print('✅ Imports OK')"

# 3. Start app
python app.py

# 4. In another terminal, test API:
# PowerShell:
Invoke-RestMethod http://localhost:5000/api/chat-sessions -Method Get

# OR Curl:
curl http://localhost:5000/api/chat-sessions
```

Expected response:
```json
{
  "sessions": [
    {
      "sno": "1",
      "chatId": "CHAT_001",
      "name": "Student Name",
      ...
    }
  ]
}
```

---

## Go-Live Checklist

- [ ] All code changes committed
- [ ] Configuration set correctly
- [ ] Google Sheet formatted properly
- [ ] All tests passing
- [ ] Documentation reviewed
- [ ] Performance acceptable
- [ ] Security reviewed
- [ ] Backup of Google Sheet taken
- [ ] Team trained on new interface
- [ ] Monitoring in place

---

## Post-Launch

### First 24 Hours
- [ ] Monitor for any errors
- [ ] Check data accuracy
- [ ] Verify performance
- [ ] Collect user feedback

### First Week
- [ ] Make any quick fixes
- [ ] Document any issues
- [ ] Update procedures if needed
- [ ] Train additional users

### Ongoing
- [ ] Regular backups
- [ ] Monitor performance
- [ ] Update as needed
- [ ] Gather feedback

---

## Emergency Procedures

### If Dashboard is Down:
```
1. Check if Flask is running
2. Check if Google Sheet is accessible
3. Look at console for errors
4. Restart Flask: python app.py
5. If still down, check internet connection
```

### If Data Not Updating:
```
1. Click "Refresh Sheets" button
2. Check Google Sheet is public
3. Verify column names are correct
4. Restart Flask
```

### If Chat Not Working:
```
1. Check if agent is logged in
2. Verify Chat ID exists in sheet
3. Check browser console for errors
4. Try refreshing page
```

---

**Status**: Ready for Launch ✅  
**Date**: December 20, 2025  
**Approvals**: 
- [ ] Development Complete
- [ ] Testing Complete
- [ ] Approved for Production
