"""
Run NOVA Web Interface
Simple script to start the web server
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    from web.app import app, socketio
    
    print("\n" + "="*50)
    print("🚀 NOVA Web Interface Starting...")
    print("="*50)
    print(f"📱 Access the interface at: http://localhost:5001")
    print(f"🌐 Open in your browser to start chatting with NOVA!")
    print("="*50 + "\n")
    
    socketio.run(app, 
                host='0.0.0.0', 
                port=5001, 
                debug=True,
                allow_unsafe_werkzeug=True)

