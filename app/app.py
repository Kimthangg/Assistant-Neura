import os
import time
import json
import uuid
import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

from langchain_core.chat_history import InMemoryChatMessageHistory 
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "./..")))

# Import required modules from your project
from bot import call_api, gen_llm

from db.db_manager import MongoDBManager
# --- Initialization ---
app = Flask(__name__)
# Set a secret key for session management
app.secret_key = os.urandom(24)

# Initialize MongoDB Manager
db_manager = MongoDBManager()

# --- Helper Functions ---
def ensure_user_id():
    """Ensure user_id exists in session"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session['chat_history'] = []
        session['context'] = {}
        session['flag'] = False
        session['conversation_name_set'] = False

# --- Flask Routes ---
@app.route('/')
def index():
    """Render the main chat interface"""
    ensure_user_id()
    
    # Get list of saved conversations
    conversation_list = db_manager.get_all_conversations()
    
    # Chuyển đổi múi giờ từ UTC sang UTC+7 (Việt Nam)
    for conv in conversation_list:
        if 'updated_at' in conv and isinstance(conv['updated_at'], datetime.datetime):
            # Thêm 7 tiếng cho múi giờ Việt Nam
            conv['updated_at'] = conv['updated_at'] + datetime.timedelta(hours=7)
    
    return render_template('index.html', 
                          chat_history=session.get('chat_history', []), 
                          conversation_list=conversation_list,
                          current_user_id=session.get('user_id', ''))

@app.route('/chat', methods=['POST'])
def chat():
    """Handle incoming chat messages"""
    ensure_user_id()
    
    # Get user message from request
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400
    
    user_message = data['message']
    
    # Process message with LLM - Truyền chat_history từ session vào gen_llm
    response, context = gen_llm(user_message, session.get('chat_history', []))
    
    #Kiểm tra xem gọi api có lỗi gì khôngz
    if context.get('error'):
        print("chạy có lỗi")
        response = context.get('error')
    # Check if action button should be displayed
    show_action_button = False
    if context and context.get('intent') in ['create_normal_event', 'update_event', 'delete_event']:
        show_action_button = True
        session['flag'] = True
    else:
        session['flag'] = False
    
    # Save context for potential action
    session['context'] = context
    
    # Update chat history
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    session['chat_history'].append({"type": "user", "content": user_message})
    session['chat_history'].append({"type": "assistant", "content": response})
    
    # Set conversation name if this is the first message
    if not session.get('conversation_name_set', False):
        conversation_name = user_message[:50]
        if len(user_message) >= 50:
            conversation_name += "..."
        session['conversation_name_set'] = True
        db_manager.save_chat_history(session['user_id'], session['chat_history'], conversation_name)
    else:
        db_manager.save_chat_history(session['user_id'], session['chat_history'])
    
    # Mark session as modified to ensure it's saved
    session.modified = True
    
    return jsonify({
        'response': response,
        'show_action_button': show_action_button
    })

@app.route('/execute', methods=['POST'])
def execute_action():
    """Execute calendar action based on context"""
    ensure_user_id()
    
    if not session.get('context'):
        return jsonify({'success': False, 'message': 'No context available'}), 400
    
    # Call API to execute action
    success = call_api(session['context'])
    
    if success.get('error'):
        message = "Có lỗi xảy ra khi thực hiện!"
        session['chat_history'].append({"type": "assistant", "content": message})
        db_manager.save_chat_history(session['user_id'], session['chat_history'])
        session.modified = True
        return jsonify({'success': False, 'message': message})
    
    if success:
        message = "Đã thực hiện thành công!"
        session['chat_history'].append({"type": "assistant", "content": message})
        db_manager.save_chat_history(session['user_id'], session['chat_history'])
        session['flag'] = False
        session.modified = True
        return jsonify({'success': True, 'message': message})

@app.route('/new_conversation', methods=['POST'])
def new_conversation():
    """Start a new conversation"""
    
    # Create new conversation
    session['user_id'] = str(uuid.uuid4())
    session['chat_history'] = []
    session['context'] = {}
    session['flag'] = False
    session['conversation_name_set'] = False
    session.modified = True
    
    return jsonify({'success': True, 'message': 'Đã bắt đầu hội thoại mới!'})

@app.route('/load_conversation/<user_id>', methods=['POST'])
def load_conversation(user_id):
    """Load a saved conversation"""
    if user_id == session.get('user_id'):
        return jsonify({'success': False, 'message': 'Đây là hội thoại hiện tại'})
    
    # Load chat history from database
    chat_history = db_manager.load_chat_history(user_id)
    
    # Update session
    session['user_id'] = user_id
    session['chat_history'] = chat_history
    session['context'] = {}
    session['flag'] = False
    session['conversation_name_set'] = True
    session.modified = True
    
    return jsonify({'success': True, 'chat_history': chat_history})

@app.route('/delete_conversation/<user_id>', methods=['POST'])
def delete_conversation(user_id):
    """Delete a conversation"""
    success = db_manager.delete_chat_history(user_id)
    
    if success:
        # If deleted the current conversation, create a new one
        if user_id == session.get('user_id'):
            session['user_id'] = str(uuid.uuid4())
            session['chat_history'] = []
            session['context'] = {}
            session['flag'] = False
            session['conversation_name_set'] = False
            session.modified = True
        
        return jsonify({'success': True, 'message': 'Đã xóa hội thoại thành công!'})
    else:
        return jsonify({'success': False, 'message': 'Có lỗi khi xóa hội thoại!'})

@app.route('/get_conversations', methods=['GET'])
def get_conversations():
    """Get the list of saved conversations"""
    conversations = db_manager.get_all_conversations()
    
    # Chuyển đổi đối tượng datetime thành chuỗi ISO8601 để JavaScript xử lý nhất quán
    for conv in conversations:
        if 'updated_at' in conv and isinstance(conv['updated_at'], datetime.datetime):
            # Thêm +07:00 để chỉ rõ múi giờ Việt Nam
            vietnam_time = conv['updated_at'] + datetime.timedelta(hours=7)
            conv['updated_at'] = vietnam_time.strftime("%Y-%m-%dT%H:%M:%S+07:00")
    
    return jsonify({'conversations': conversations})

if __name__ == '__main__':
    app.run(
        # host='0.0.0.0',  # Cho phép truy cập từ bên ngoài nếu cần
        port=5000,       # Hoặc bất kỳ port nào Cậu muốn
        debug=True       # Bật debug mode, auto-reload khi thay code
    )



