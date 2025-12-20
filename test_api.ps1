# Test Script for Vedantu Chat Dashboard API (PowerShell)
# Run in Windows PowerShell

# ============================================
# Configuration
# ============================================
$BASE_URL = "http://localhost:5000"
$cookieFile = "cookies.txt"

# ============================================
# Helper function to make requests
# ============================================
function Make-Request {
    param(
        [string]$Method,
        [string]$Endpoint,
        [hashtable]$Body = $null,
        [switch]$WithCookies
    )
    
    $url = "$BASE_URL$Endpoint"
    $headers = @{ "Content-Type" = "application/json" }
    
    $params = @{
        Method = $Method
        Uri = $url
        Headers = $headers
        SessionVariable = 'session'
    }
    
    if ($Body) {
        $params['Body'] = ($Body | ConvertTo-Json)
    }
    
    if ($WithCookies) {
        $params['WebSession'] = $session
    }
    
    try {
        $response = Invoke-RestMethod @params
        return $response | ConvertTo-Json -Depth 10
    } catch {
        return $_.Exception.Message
    }
}

# ============================================
# 1. LOGIN TEST
# ============================================
Write-Host "=== Testing Login ===" -ForegroundColor Green
$loginBody = @{
    user_id = "agent"
    password = "agent123"
}

$loginResponse = Invoke-RestMethod -Method Post `
    -Uri "$BASE_URL/api/auth/login" `
    -Headers @{"Content-Type" = "application/json"} `
    -Body ($loginBody | ConvertTo-Json) `
    -SessionVariable 'WebSession'

Write-Host ($loginResponse | ConvertTo-Json)

# ============================================
# 2. CHECK AUTH
# ============================================
Write-Host "`n=== Checking Authentication ===" -ForegroundColor Green
$authResponse = Invoke-RestMethod -Method Get `
    -Uri "$BASE_URL/api/auth/check" `
    -WebSession $WebSession

Write-Host ($authResponse | ConvertTo-Json)

# ============================================
# 3. GET CHAT SESSIONS
# ============================================
Write-Host "`n=== Getting Chat Sessions from Google Sheets ===" -ForegroundColor Green
try {
    $sessionsResponse = Invoke-RestMethod -Method Get `
        -Uri "$BASE_URL/api/chat-sessions" `
        -WebSession $WebSession
    
    Write-Host ($sessionsResponse | ConvertTo-Json -Depth 5)
} catch {
    Write-Host "Error: $_"
}

# ============================================
# 4. GET CHAT CONTEXT
# ============================================
Write-Host "`n=== Getting Chat Context for CHAT_001 ===" -ForegroundColor Green
try {
    $contextResponse = Invoke-RestMethod -Method Get `
        -Uri "$BASE_URL/api/chat-context/CHAT_001" `
        -WebSession $WebSession
    
    Write-Host ($contextResponse | ConvertTo-Json -Depth 5)
} catch {
    Write-Host "Error: $_"
}

# ============================================
# 5. REFRESH SHEETS
# ============================================
Write-Host "`n=== Refreshing Google Sheets Cache ===" -ForegroundColor Green
try {
    $refreshResponse = Invoke-RestMethod -Method Post `
        -Uri "$BASE_URL/api/refresh-sheets" `
        -WebSession $WebSession
    
    Write-Host ($refreshResponse | ConvertTo-Json)
} catch {
    Write-Host "Error: $_"
}

# ============================================
# 6. SEND MESSAGE
# ============================================
Write-Host "`n=== Sending a Message ===" -ForegroundColor Green
try {
    $messageBody = @{
        chatId = "CHAT_001"
        message = "This is a test message from the agent"
        sender = "agent"
    }
    
    $sendResponse = Invoke-RestMethod -Method Post `
        -Uri "$BASE_URL/api/send-message" `
        -Headers @{"Content-Type" = "application/json"} `
        -Body ($messageBody | ConvertTo-Json) `
        -WebSession $WebSession
    
    Write-Host ($sendResponse | ConvertTo-Json)
} catch {
    Write-Host "Error: $_"
}

# ============================================
# 7. GET MESSAGES
# ============================================
Write-Host "`n=== Getting Messages for CHAT_001 ===" -ForegroundColor Green
try {
    $messagesResponse = Invoke-RestMethod -Method Get `
        -Uri "$BASE_URL/api/get-messages/CHAT_001" `
        -WebSession $WebSession
    
    Write-Host ($messagesResponse | ConvertTo-Json -Depth 5)
} catch {
    Write-Host "Error: $_"
}

# ============================================
# 8. POLL MESSAGES
# ============================================
Write-Host "`n=== Polling Messages for CHAT_001 ===" -ForegroundColor Green
try {
    $pollResponse = Invoke-RestMethod -Method Get `
        -Uri "$BASE_URL/api/poll-messages/CHAT_001" `
        -WebSession $WebSession
    
    Write-Host ($pollResponse | ConvertTo-Json -Depth 5)
} catch {
    Write-Host "Error: $_"
}

# ============================================
# 9. LOGOUT
# ============================================
Write-Host "`n=== Logout ===" -ForegroundColor Green
try {
    $logoutResponse = Invoke-RestMethod -Method Post `
        -Uri "$BASE_URL/api/auth/logout" `
        -WebSession $WebSession
    
    Write-Host ($logoutResponse | ConvertTo-Json)
} catch {
    Write-Host "Error: $_"
}

Write-Host "`n=== All Tests Complete ===" -ForegroundColor Green
