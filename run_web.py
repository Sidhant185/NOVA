"""
Run NOVA Web Interface
Simple script to start the web server
"""
import sys
import os

# Import compatibility fix FIRST before any other imports
# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import compatibility module to patch importlib.metadata
import compat

if __name__ == '__main__':
    import signal
    
    def signal_handler(sig, frame):
        print("\n\n🛑 Shutting down server...", flush=True)
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        print("Loading web application...", flush=True)
        print("Importing web.app module...", flush=True)
        from web.app import app, socketio
        print("✓ Web app imported successfully", flush=True)
        
        print("\n" + "="*50, flush=True)
        print("🚀 NOVA Web Interface Starting...", flush=True)
        print("="*50, flush=True)
        print(f"📱 Access the interface at: http://localhost:5001", flush=True)
        print(f"🌐 Open in your browser to start chatting with NOVA!", flush=True)
        print("="*50 + "\n", flush=True)
        print("⏳ Starting server (this may take a moment)...", flush=True)
        print("💡 Server will block here - this is normal!", flush=True)
        print("💡 Press Ctrl+C to stop the server\n", flush=True)
        
        # Run the server
        socketio.run(app, 
                    host='0.0.0.0', 
                    port=5001, 
                    debug=True,
                    allow_unsafe_werkzeug=True,
                    use_reloader=False)  # Disable reloader to avoid double startup
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down server...", flush=True)
        sys.exit(0)
    except Exception as e:
        import traceback
        print(f"\n❌ Error starting NOVA Web Interface:", flush=True)
        print(f"Error: {e}", flush=True)
        print("\nFull traceback:", flush=True)
        traceback.print_exc()
        sys.exit(1)

