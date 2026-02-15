#!/usr/bin/env python3
"""Web interface for GLM terminal - accessible from WeChat browser."""
import os
from flask import Flask, request, jsonify, render_template_string
from glm_langchain_client import GLMClient
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import subprocess

app = Flask(__name__)

# Initialize GLM client
client = GLMClient(api_key=os.getenv("ZHIPUAI_API_KEY"))

# Store conversation history per session (simple in-memory storage)
conversations = {}

SYSTEM_PROMPT = """You are a helpful AI assistant with access to various tools.

When user asks you to search or find information, you MUST execute the actual command:

**News Search**: EXECUTE: python skills/news-search/search_news.py "search query" --limit 10
**China Content Search**: EXECUTE: python skills/china-search/china_search.py "search query" --type [movie|tv|entertainment]

After seeing search results, summarize them in Chinese with key information."""

def execute_command(cmd):
    """Execute shell command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {e}"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GLM Assistant</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f5f5f5;
            padding-bottom: 80px;
        }
        .header {
            background: #07c160;
            color: white;
            padding: 15px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
        }
        .chat-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .message {
            margin-bottom: 15px;
            display: flex;
        }
        .message.user {
            justify-content: flex-end;
        }
        .message-content {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 8px;
            word-wrap: break-word;
        }
        .message.user .message-content {
            background: #07c160;
            color: white;
        }
        .message.assistant .message-content {
            background: white;
            color: #333;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            padding: 10px;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        }
        .input-box {
            max-width: 800px;
            margin: 0 auto;
            display: flex;
            gap: 10px;
        }
        input {
            flex: 1;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 20px;
            font-size: 16px;
            outline: none;
        }
        button {
            padding: 12px 24px;
            background: #07c160;
            color: white;
            border: none;
            border-radius: 20px;
            font-size: 16px;
            cursor: pointer;
        }
        button:active {
            background: #06ad56;
        }
        .loading {
            text-align: center;
            color: #999;
            padding: 10px;
        }
    </style>
</head>
<body>
    <div class="header">GLM 智能助手</div>
    <div class="chat-container" id="chat"></div>
    <div class="input-container">
        <div class="input-box">
            <input type="text" id="input" placeholder="输入消息..." />
            <button onclick="sendMessage()">发送</button>
        </div>
    </div>

    <script>
        const sessionId = Date.now().toString();
        
        function addMessage(text, isUser) {
            const chat = document.getElementById('chat');
            const msg = document.createElement('div');
            msg.className = 'message ' + (isUser ? 'user' : 'assistant');
            msg.innerHTML = '<div class="message-content">' + text.replace(/\\n/g, '<br>') + '</div>';
            chat.appendChild(msg);
            chat.scrollTop = chat.scrollHeight;
        }
        
        async function sendMessage() {
            const input = document.getElementById('input');
            const text = input.value.trim();
            if (!text) return;
            
            addMessage(text, true);
            input.value = '';
            
            const chat = document.getElementById('chat');
            const loading = document.createElement('div');
            loading.className = 'loading';
            loading.textContent = '正在思考...';
            chat.appendChild(loading);
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text, session_id: sessionId })
                });
                const data = await response.json();
                loading.remove();
                addMessage(data.response, false);
            } catch (error) {
                loading.remove();
                addMessage('抱歉，发生错误：' + error.message, false);
            }
        }
        
        document.getElementById('input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the chat interface."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages."""
    data = request.json
    message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    # Get or create conversation history
    if session_id not in conversations:
        conversations[session_id] = [SystemMessage(content=SYSTEM_PROMPT)]
    
    messages = conversations[session_id]
    messages.append(HumanMessage(content=message))
    
    # Get AI response
    response = client.invoke(messages)
    
    # Check if response contains EXECUTE command
    if "EXECUTE:" in response:
        for line in response.split("\n"):
            if line.startswith("EXECUTE:"):
                cmd = line.replace("EXECUTE:", "").strip()
                output = execute_command(cmd)
                
                # Add result and ask for summary
                messages.append(AIMessage(content=f"Command executed: {cmd}\nResult: {output}"))
                messages.append(HumanMessage(content="请用中文总结上面的搜索结果，提取关键信息。"))
                response = client.invoke(messages)
                messages.append(AIMessage(content=response))
                break
    else:
        messages.append(AIMessage(content=response))
    
    # Keep conversation history manageable (last 20 messages)
    if len(messages) > 20:
        conversations[session_id] = [messages[0]] + messages[-19:]
    
    return jsonify({'response': response})

if __name__ == '__main__':
    print("\n🚀 GLM Web Assistant starting...")
    print("📱 Access from WeChat: http://your-ip:5000")
    print("💻 Local access: http://localhost:5000\n")
    app.run(host='0.0.0.0', port=5000, debug=False)
