# Vedantu Chat Dashboard - Google Sheets Integration Setup Guide

## Overview
This guide explains how to integrate Google Sheets with the Vedantu Chat Dashboard to display chat sessions and conversation history with AI responses.

## New Google Sheet Format
The expected Google Sheet should have the following columns in order:

| Column | Type | Description |
|--------|------|-------------|
| Sno | String | Serial Number |
| Chat ID | String | Unique identifier for each chat |
| Name | String | Student/Customer name |
| Type (Parent/Student/Visitor) | String | User type classification |
| User Intent | String | What the user is asking for |
| AI Response | String | Previous AI response (if any) |
| Class | String | Student's class (e.g., "10", "12") |
| Target Exam | String | Target exam (e.g., "JEE", "NEET", "CBSE") |
| School Board | String | School board (e.g., "CBSE", "ICSE", "State Board") |
| School Medium | String | Medium of instruction (e.g., "English", "Hindi") |
| Location | String | Geographic location |
| Doubt | String | Specific doubt/topic area |
| Free Content | String | Free content information |
| Ranking | String | User ranking/level |
| Agent Transferred | String | Whether transferred to agent |
| Time Stamp | String | Timestamp of interaction |
| Conversation State | String | Current state (e.g., "Active", "Resolved") |

## Setup Instructions

### 1. Create Google Sheet
1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet with the columns listed above
3. Add your chat data with multiple rows for different conversations

### 2. Get Google Sheets API Credentials

#### Enable Google Sheets API:
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select an existing one
3. Search for "Google Sheets API" and click "Enable"
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. Copy your API Key

#### Get Your Sheet ID:
1. Open your Google Sheet
2. The Sheet ID is in the URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`
3. Copy the SHEET_ID

### 3. Update Configuration in app.py

Open `app.py` and update these values:

```python
# Google Sheets Configuration
GOOGLE_SHEETS_ID = 'your-google-sheet-id-here'  # Replace with actual Sheet ID
GOOGLE_SHEETS_API_KEY = 'your-google-api-key-here'  # Replace with actual API key
SHEET_NAME = 'Sheet1'  # Replace with actual sheet name if different
```

### 4. Dashboard Features

The dashboard now displays:
- **Sno**: Serial number
- **Chat ID**: Unique chat identifier
- **Name**: Student/customer name
- **Class**: Student's class
- **Target Exam**: Target exam (JEE, NEET, etc.)
- **School Board**: CBSE, ICSE, etc.
- **Type**: Parent/Student/Visitor
- **Timestamp**: When the interaction occurred
- **Action**: "Open Chat" button to view conversation

#### Dashboard Actions:
- **Refresh**: Reload chat sessions from current memory
- **Refresh Sheets**: Fetch latest data from Google Sheets and clear cache

### 5. Chat Interface Features

When opening a chat, the interface shows:

#### Header Information:
- Student name
- Class (from query parameter)
- Target exam (from query parameter)
- Chat ID

#### Previous Conversation Context Section:
Displays all previous conversations for this chat ID including:
- **User Intent**: What the user asked
- **AI Response**: Previous AI responses
- **Doubt**: Specific topic area
- **Conversation State**: Current state

#### Message Area:
- Live chat interface for agent interaction
- Message history
- Real-time polling for new messages

### 6. API Endpoints

New endpoints added:

#### `/api/chat-sessions` (GET)
Returns all chat sessions from Google Sheets
```json
{
  "sessions": [
    {
      "sno": "1",
      "chatId": "CHAT_001",
      "name": "Student Name",
      "class": "10",
      "targetExam": "JEE",
      "schoolBoard": "CBSE",
      "type": "Student",
      "timestamp": "2025-12-20 14:30"
    }
  ]
}
```

#### `/api/chat-context/<chat_id>` (GET)
Returns previous conversation context for a specific chat
```json
{
  "context": [
    {
      "userIntent": "How to solve quadratic equations?",
      "aiResponse": "Quadratic equations can be solved using...",
      "doubt": "Quadratic Equations",
      "conversationState": "Active"
    }
  ],
  "chatId": "CHAT_001"
}
```

#### `/api/refresh-sheets` (POST)
Manually refresh Google Sheets cache
```json
{
  "success": true,
  "message": "Refreshed 42 chat records"
}
```

### 7. Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask server
python app.py
```

Access the application at: `http://localhost:5000`

### 8. Troubleshooting

#### Google Sheets API Not Returning Data
- Check that Google Sheets API is enabled in Google Cloud Console
- Verify the API Key is correct
- Verify the Sheet ID is correct
- Ensure the sheet is publicly accessible or shared with the API credentials

#### Chat Context Not Showing
- Check that the Chat ID matches between dashboard and sheet data
- Verify that the User Intent and AI Response columns have data
- Check browser console for any errors

#### Cache Issues
- Use "Refresh Sheets" button to clear cache and fetch fresh data
- Cache is automatically cleared after 5 minutes (adjustable in code)

### 9. Data Mapping Logic

The application maps Google Sheet columns as follows:

```python
header_map = {
    'Sno': index 0,
    'Chat ID': index 1,
    'Name': index 2,
    'Type (Parent/Student/Visitor)': index 3,
    'User Intent': index 4,
    'AI Response': index 5,
    'Class': index 6,
    'Target Exam': index 7,
    'School Board': index 8,
    'School Medium': index 9,
    'Location': index 10,
    'Doubt': index 11,
    'Free Content': index 12,
    'Ranking': index 13,
    'Agent Transferred': index 14,
    'Time Stamp': index 15,
    'Conversation State': index 16
}
```

### 10. Example Bot Response Format

The AI Response column can contain formatted responses like:

```
Bot: Yes, NCERT Solutions for Classes 1–12 are available for FREE download on Vedantu. 
They are chapter-wise, aligned with the CBSE 2025–26 syllabus, and cover subjects like 
Maths, Science, Physics, Chemistry, Biology, Accountancy, Economics, English, Hindi, and Social Science.

These solutions are prepared by master teachers to help with concept clarity, homework, 
and exam preparation.

For more details, you can visit https://www.vedantu.com/ncert-solutions
```

This will be displayed in the "Previous Conversation Context" section for agent reference.

## Support & Maintenance

- Auto-refresh of dashboard: Every 10 seconds
- Google Sheets cache: Expires automatically
- Message polling: Every 2 seconds
- All timestamps are formatted to user's local timezone

