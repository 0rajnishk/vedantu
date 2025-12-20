from flask import Flask, request, jsonify, session, redirect, url_for, send_from_directory
from datetime import datetime
import json
import os
import requests
import csv
import io
from functools import lru_cache

app = Flask(__name__, static_folder='static', template_folder='templates', static_url_path='')
app.secret_key = 'your_secret_key_here_change_this'

# Google Sheets Configuration
GOOGLE_SHEETS_ID = '1-aRmuDOSu38Oid975ZiAvS3XER-cpO-ldsmfPz46kP8'  # Your public sheet ID
GOOGLE_SHEETS_API_KEY = ''  # Not needed for public sheets (leave empty)
SHEET_NAME = 'Sheet1'  # Replace with actual sheet name

# Hardcoded credentials
VALID_CREDENTIALS = {
    'admin': 'password123',
    'agent': 'agent123'
}

# Store active chat sessions and messages
chat_sessions = {}
pending_responses = {}

# ==================== GOOGLE SHEETS INTEGRATION ====================

@lru_cache(maxsize=1)
def get_google_sheets_data():
    """Fetch data from Google Sheets (public sheet - no API key needed)"""
    try:
        # Method 1: Try using Google Sheets API v4 (works for public sheets)
        url = f'https://sheets.googleapis.com/v4/spreadsheets/{GOOGLE_SHEETS_ID}/values/{SHEET_NAME}'
        params = {}
        
        # If API key is provided, use it; otherwise request will work for public sheets
        if GOOGLE_SHEETS_API_KEY:
            params['key'] = GOOGLE_SHEETS_API_KEY
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('values', [])
        elif response.status_code == 403:
            # If API fails, try CSV export method
            print("API access denied, trying CSV export method...")
            return get_google_sheets_csv()
        else:
            print(f"Error fetching sheets: {response.status_code}")
            print(f"Response: {response.text}")
            return []
    except Exception as e:
        print(f"Error in get_google_sheets_data (API method): {str(e)}")
        # Fallback to CSV method
        try:
            return get_google_sheets_csv()
        except Exception as csv_error:
            print(f"Error in CSV method: {str(csv_error)}")
            return []

def get_google_sheets_csv():
    """Alternative method: Fetch Google Sheets data via CSV export (works for public sheets)"""
    try:
        # CSV export URL for public Google Sheets
        csv_url = f'https://docs.google.com/spreadsheets/d/{GOOGLE_SHEETS_ID}/export?format=csv'
        response = requests.get(csv_url, timeout=10)
        
        if response.status_code == 200:
            # Parse CSV data
            import csv
            import io
            
            csv_content = response.text
            reader = csv.reader(io.StringIO(csv_content))
            rows = list(reader)
            return rows
        else:
            print(f"Error fetching CSV: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error in get_google_sheets_csv: {str(e)}")
        return []

def parse_sheets_to_chats(rows):
    """Parse Google Sheets rows to chat format"""
    if len(rows) < 2:
        return []
    
    headers = rows[0]
    chats = []
    
    try:
        # Create header mapping
        header_map = {h.strip(): i for i, h in enumerate(headers)}
        
        for row in rows[1:]:
            if len(row) < len(headers):
                continue
            
            chat_data = {
                'sno': row[header_map.get('Sno', 0)] if 'Sno' in header_map else '',
                'chatId': row[header_map.get('Chat ID', 1)] if 'Chat ID' in header_map else '',
                'name': row[header_map.get('Name', 2)] if 'Name' in header_map else '',
                'type': row[header_map.get('Type (Parent/Student/Visitor)', 3)] if 'Type (Parent/Student/Visitor)' in header_map else '',
                'userIntent': row[header_map.get('User Intent', 4)] if 'User Intent' in header_map else '',
                'aiResponse': row[header_map.get('AI Response', 5)] if 'AI Response' in header_map else '',
                'class': row[header_map.get('Class', 6)] if 'Class' in header_map else '',
                'targetExam': row[header_map.get('Target Exam', 7)] if 'Target Exam' in header_map else '',
                'schoolBoard': row[header_map.get('School Board', 8)] if 'School Board' in header_map else '',
                'schoolMedium': row[header_map.get('School Medium', 9)] if 'School Medium' in header_map else '',
                'location': row[header_map.get('Location', 10)] if 'Location' in header_map else '',
                'doubt': row[header_map.get('Doubt', 11)] if 'Doubt' in header_map else '',
                'freeContent': row[header_map.get('Free Content', 12)] if 'Free Content' in header_map else '',
                'ranking': row[header_map.get('Ranking', 13)] if 'Ranking' in header_map else '',
                'agentTransferred': row[header_map.get('Agent Transferred', 14)] if 'Agent Transferred' in header_map else '',
                'timestamp': row[header_map.get('Time Stamp', 15)] if 'Time Stamp' in header_map else '',
                'conversationState': row[header_map.get('Conversation State', 16)] if 'Conversation State' in header_map else ''
            }
            
            if chat_data['chatId']:  # Only add if chatId exists
                chats.append(chat_data)
    except Exception as e:
        print(f"Error parsing sheets data: {str(e)}")
    
    return chats

def parse_conversation_messages(user_intent, ai_response):
    """Parse User Intent and AI Response into interleaved messages (user, bot, user, bot...)"""
    user_messages = []
    bot_messages = []
    
    # Extract all User messages
    if user_intent:
        lines = user_intent.split('\n')
        for line in lines:
            clean_line = line.strip()
            if clean_line.startswith('User:'):
                msg_text = clean_line[5:].strip()  # Remove "User:" prefix
                if msg_text:
                    user_messages.append(msg_text)
    
    # Extract all Bot messages
    if ai_response:
        lines = ai_response.split('\n')
        for line in lines:
            clean_line = line.strip()
            if clean_line.startswith('Bot:'):
                msg_text = clean_line[4:].strip()  # Remove "Bot:" prefix
                if msg_text:
                    bot_messages.append(msg_text)
    
    # Interleave messages (user, bot, user, bot, ...)
    messages = []
    max_len = max(len(user_messages), len(bot_messages))
    
    for i in range(max_len):
        # Add user message if available
        if i < len(user_messages):
            messages.append({
                'sender': 'user',
                'text': user_messages[i]
            })
        # Add bot message if available
        if i < len(bot_messages):
            messages.append({
                'sender': 'bot',
                'text': bot_messages[i]
            })
    
    return messages

# ==================== AUTH ROUTES ====================

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login')
def login():
    return app.send_static_file('login.html')

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.get_json()
    user_id = data.get('user_id')
    password = data.get('password')
    
    if user_id in VALID_CREDENTIALS and VALID_CREDENTIALS[user_id] == password:
        session['user_id'] = user_id
        return jsonify({'success': True, 'message': 'Login successful', 'user_id': user_id})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out'})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/auth/check', methods=['GET'])
def check_auth():
    if 'user_id' not in session:
        return jsonify({'authenticated': False}), 401
    return jsonify({'authenticated': True, 'user_id': session['user_id']})

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return send_from_directory('templates', 'dashboard.html')

@app.route('/chat/<chat_id>')
def chat(chat_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return send_from_directory('templates', 'chat.html')

# ==================== CHAT API ROUTES ====================

@app.route('/api/send-message', methods=['POST'])
def send_message():
    """Receive message from chat interface and send to N8N webhook"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    chat_id = data.get('chatId')
    message = data.get('message')
    sender = data.get('sender', 'agent')
    
    if not chat_id or not message:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Initialize chat session if not exists
    if chat_id not in chat_sessions:
        chat_sessions[chat_id] = {
            'messages': [],
            'created_at': datetime.now().isoformat(),
            'user_name': 'Customer'
        }
    
    # Store message locally
    chat_sessions[chat_id]['messages'].append({
        'sender': sender,
        'text': message,
        'timestamp': datetime.now().isoformat()
    })
    
    # Prepare payload for N8N webhook
    payload = {
        'chatId': chat_id,
        'sender': sender,
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'agentId': session.get('user_id')
    }
    
    # Forward to N8N webhook
    try:
        import requests
        webhook_url = 'https://vikramautomation.app.n8n.cloud/webhook/vedantu-chat'
        response = requests.post(webhook_url, json=payload, timeout=5)
        
        print(f"Webhook response: {response.status_code}")
        
        return jsonify({
            'success': True,
            'message': 'Message sent',
            'messageId': len(chat_sessions[chat_id]['messages'])
        })
    except Exception as e:
        print(f"Error sending to webhook: {str(e)}")
        return jsonify({
            'success': True,
            'message': 'Message queued (webhook unavailable)',
            'error': str(e)
        })

@app.route('/api/get-messages/<chat_id>', methods=['GET'])
def get_messages(chat_id):
    """Get all messages for a chat session"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if chat_id not in chat_sessions:
        return jsonify({'messages': []})
    
    return jsonify({
        'messages': chat_sessions[chat_id]['messages'],
        'chatId': chat_id
    })

@app.route('/api/webhook/response', methods=['POST'])
def webhook_response():
    """Receive response from N8N webhook"""
    data = request.get_json()
    chat_id = data.get('chatId')
    message = data.get('message')
    sender = data.get('sender', 'system')
    
    if not chat_id:
        return jsonify({'error': 'Missing chatId'}), 400
    
    # Initialize if not exists
    if chat_id not in chat_sessions:
        chat_sessions[chat_id] = {
            'messages': [],
            'created_at': datetime.now().isoformat(),
            'user_name': 'Customer'
        }
    
    # Store the response
    chat_sessions[chat_id]['messages'].append({
        'sender': sender,
        'text': message,
        'timestamp': datetime.now().isoformat()
    })
    
    # Store in pending responses so chat can poll it
    if chat_id not in pending_responses:
        pending_responses[chat_id] = []
    
    pending_responses[chat_id].append({
        'sender': sender,
        'text': message,
        'timestamp': datetime.now().isoformat()
    })
    
    print(f"Response received for chat {chat_id}: {message}")
    
    return jsonify({'success': True, 'message': 'Response received'})

@app.route('/api/poll-messages/<chat_id>', methods=['GET'])
def poll_messages(chat_id):
    """Poll for new messages (long polling alternative to WebSocket)"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if chat_id in pending_responses and pending_responses[chat_id]:
        messages = pending_responses[chat_id]
        pending_responses[chat_id] = []
        return jsonify({'messages': messages, 'hasMessages': True})
    
    return jsonify({'messages': [], 'hasMessages': False})

@app.route('/api/chat-sessions', methods=['GET'])
def get_chat_sessions():
    """Get all chat sessions from Google Sheets"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Fetch from Google Sheets
        rows = get_google_sheets_data()
        chats = parse_sheets_to_chats(rows)
        
        # Format for dashboard display
        sessions = []
        for chat in chats:
            sessions.append({
                'sno': chat['sno'],
                'chatId': chat['chatId'],
                'name': chat['name'],
                'class': chat['class'],
                'targetExam': chat['targetExam'],
                'schoolBoard': chat['schoolBoard'],
                'type': chat['type'],
                'agentTransferred': chat['agentTransferred'],
                'userIntent': chat['userIntent'],
                'timestamp': chat['timestamp']
            })
        
        return jsonify({'sessions': sessions})
    except Exception as e:
        print(f"Error in get_chat_sessions: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat-context/<chat_id>', methods=['GET'])
def get_chat_context(chat_id):
    """Get previous chat context for a specific chat"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        rows = get_google_sheets_data()
        chats = parse_sheets_to_chats(rows)
        
        # Find all conversations for this chat ID
        relevant_chats = [c for c in chats if c['chatId'] == chat_id]
        
        messages = []
        for chat in relevant_chats:
            # Parse User Intent and AI Response into messages
            parsed = parse_conversation_messages(chat['userIntent'], chat['aiResponse'])
            messages.extend(parsed)
        
        return jsonify({'messages': messages, 'chatId': chat_id})
    except Exception as e:
        print(f"Error in get_chat_context: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/refresh-sheets', methods=['POST'])
def refresh_sheets():
    """Manually refresh Google Sheets cache"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Clear cache
        get_google_sheets_data.cache_clear()
        
        # Fetch fresh data
        rows = get_google_sheets_data()
        chats = parse_sheets_to_chats(rows)
        
        return jsonify({
            'success': True,
            'message': f'Refreshed {len(chats)} chat records'
        })
    except Exception as e:
        print(f"Error in refresh_sheets: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    print("=" * 60)
    print("Flask Server Starting...")
    print("=" * 60)
    print("\nValid Credentials:")
    for user_id, password in VALID_CREDENTIALS.items():
        print(f"  User ID: {user_id}")
        print(f"  Password: {password}")
    print("\n" + "=" * 60)
    print(f"Server running on: http://localhost:{port}")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=port)
