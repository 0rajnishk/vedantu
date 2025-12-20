#!/bin/bash
# Test Script for Vedantu Chat Dashboard API

# ============================================
# Configuration
# ============================================
BASE_URL="http://localhost:5000"
AGENT_COOKIE="agent123"

# ============================================
# 1. LOGIN TEST
# ============================================
echo "=== Testing Login ==="
curl -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "agent",
    "password": "agent123"
  }' \
  -c cookies.txt

echo -e "\n"

# ============================================
# 2. CHECK AUTH
# ============================================
echo "=== Checking Authentication ==="
curl -X GET "$BASE_URL/api/auth/check" \
  -b cookies.txt

echo -e "\n"

# ============================================
# 3. GET CHAT SESSIONS
# ============================================
echo "=== Getting Chat Sessions from Google Sheets ==="
curl -X GET "$BASE_URL/api/chat-sessions" \
  -b cookies.txt

echo -e "\n"

# ============================================
# 4. GET CHAT CONTEXT
# ============================================
echo "=== Getting Chat Context for CHAT_001 ==="
curl -X GET "$BASE_URL/api/chat-context/CHAT_001" \
  -b cookies.txt

echo -e "\n"

# ============================================
# 5. REFRESH SHEETS
# ============================================
echo "=== Refreshing Google Sheets Cache ==="
curl -X POST "$BASE_URL/api/refresh-sheets" \
  -b cookies.txt

echo -e "\n"

# ============================================
# 6. SEND MESSAGE
# ============================================
echo "=== Sending a Message ==="
curl -X POST "$BASE_URL/api/send-message" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "chatId": "CHAT_001",
    "message": "This is a test message from the agent",
    "sender": "agent"
  }'

echo -e "\n"

# ============================================
# 7. GET MESSAGES
# ============================================
echo "=== Getting Messages for CHAT_001 ==="
curl -X GET "$BASE_URL/api/get-messages/CHAT_001" \
  -b cookies.txt

echo -e "\n"

# ============================================
# 8. LOGOUT
# ============================================
echo "=== Logout ==="
curl -X POST "$BASE_URL/api/auth/logout" \
  -b cookies.txt

echo -e "\n"
echo "=== All Tests Complete ==="
