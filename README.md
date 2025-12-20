# Vedantu Chat System

A professional chat application with Flask backend, HTTP-based REST API communication, and N8N webhook integration. Pure REST API - No Jinja templating.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Flask Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 3. Access the Application

- **Login Page**: http://localhost:5000/login
- **Dashboard**: http://localhost:5000/dashboard (after login)

## Demo Credentials

### Admin User
- **User ID**: `admin`
- **Password**: `password123`

### Agent User
- **User ID**: `agent`
- **Password**: `agent123`

## System Architecture

### Frontend (Pure HTML + Vue.js)
- **Login Page** (`static/login.html`): Secure authentication interface
- **Dashboard** (`static/dashboard.html`): Chat sessions overview
- **Chat** (`static/chat.html`): Real-time chat interface with polling

All frontend pages are static HTML served from `/static` folder. No Jinja templating - all data is loaded via REST API calls from Vue.js applications.

### Backend
- **Flask App** (`app.py`): REST API server
- **Authentication**: Session-based with hardcoded credentials
- **Communication**: HTTP polling (2-second intervals) instead of WebSocket
- **Webhook Integration**: Forwards messages to N8N at `https://vikramautomation.app.n8n.cloud/webhook/vedantu-chat`

## API Endpoints

### Authentication
- `POST /api/auth/login` - User authentication
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/check` - Check authentication status

### Chat Operations
- `POST /api/send-message` - Send message to N8N webhook
- `GET /api/poll-messages/<chat_id>` - Poll for new messages
- `GET /api/get-messages/<chat_id>` - Get all messages for a chat
- `GET /api/chat-sessions` - Get all active chat sessions

### Webhook
- `POST /api/webhook/response` - Receive responses from N8N

## How It Works

1. **User Login**: Agent logs in with credentials via `/api/auth/login`
2. **View Dashboard**: Dashboard fetches active chats via `/api/chat-sessions`
3. **Open Chat**: Agent opens a specific chat session (static chat.html page)
4. **Send Message**: 
   - Agent types and sends message
   - Message sent to `/api/send-message` via HTTP POST
   - Backend forwards it to N8N webhook
5. **Receive Response**:
   - N8N processes the message
   - Sends response back to `/api/webhook/response`
   - Chat polls `/api/poll-messages` every 2 seconds
   - Response appears in chat UI

## Message Flow

```
Agent Chat UI (Vue.js)
    ↓
POST /api/send-message (HTTP)
    ↓
Flask Backend
    ↓
N8N Webhook (https://vikramautomation.app.n8n.cloud/webhook/vedantu-chat)
    ↓
N8N Processing
    ↓
POST /api/webhook/response (Response from N8N)
    ↓
Flask Backend (stores in memory)
    ↓
GET /api/poll-messages (Chat polls every 2s)
    ↓
Chat UI (displays new messages)
```

## Features

✓ Pure REST API (no Jinja templating)
✓ Static HTML pages with Vue.js
✓ Professional login system with hardcoded credentials
✓ Dashboard with active chat sessions
✓ Real-time chat with HTTP polling
✓ Message history tracking
✓ N8N webhook integration
✓ Responsive UI with glassmorphism design
✓ Session management
✓ Chat statistics

## File Structure

```
vedantu/
├── app.py                          # Flask backend (REST API only)
├── requirements.txt                # Python dependencies
├── static/
│   ├── login.html                 # Login page (Vue.js + static)
│   ├── dashboard.html             # Dashboard (Vue.js + static)
│   └── chat.html                  # Chat interface (Vue.js + static)
├── run.bat                         # Run script (Windows)
├── setup.bat                       # Setup script (Windows)
└── README.md                       # This file
```

## No Templates Approach

This system uses **pure REST API** with static HTML files:
- All HTML files are static (no Jinja templates)
- Data is fetched via REST API endpoints from Vue.js
- No server-side rendering
- Pages are completely decoupled from backend
- Easy to deploy (can be hosted on CDN if needed)

## Environment Variables (Optional)

You can customize the following in `app.py`:
- `N8N_WEBHOOK_URL` - N8N webhook endpoint
- `VALID_CREDENTIALS` - User credentials
- Server port and host

## Troubleshooting

### Session Expires
- Sessions are stored in-memory, so they'll be cleared on server restart
- Add session persistence by using Flask-SQLAlchemy if needed

### Messages Not Showing
- Check browser console for errors
- Verify N8N webhook is returning responses properly
- Check that `/api/webhook/response` is being called

### Login Issues
- Use exact credentials: `admin` / `password123` or `agent` / `agent123`
- Check browser cookies are enabled

### 401 Unauthorized
- Session might have expired
- User will be automatically redirected to login

## Next Steps

1. **Production Deployment**
   - Use a proper WSGI server (Gunicorn, uWSGI)
   - Set proper secret key
   - Use environment variables for credentials

2. **Database Integration**
   - Replace in-memory storage with proper database
   - Implement chat history persistence

3. **Authentication**
   - Replace hardcoded credentials with database
   - Add JWT tokens for better security

4. **Static File Hosting**
   - Can host static HTML files on CDN (CloudFront, Netlify, etc)
   - API remains on Flask backend

