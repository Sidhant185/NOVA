"""
NOVA Web Interface - Flask Application
Main entry point for the web-based interface.
"""
import os
import sys

# Import compatibility fix FIRST - before any other imports
# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    import compat  # This patches importlib.metadata for Python 3.9
except ImportError:
    pass  # If compat module doesn't exist, continue (might be Python 3.10+)

from flask import Flask, render_template, jsonify, send_from_directory
from flask_socketio import SocketIO
from flask_cors import CORS
import logging

from utils.logger import setup_logging
from config import Config

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# Get Flask secret key from environment - REQUIRED for production
flask_secret_key = os.getenv('FLASK_SECRET_KEY')
if not flask_secret_key:
    import secrets
    # Generate a random secret key for development if not set
    # WARNING: This will change on every restart - set FLASK_SECRET_KEY in .env for production
    flask_secret_key = secrets.token_hex(32)
    logger.warning("FLASK_SECRET_KEY not set in .env - using randomly generated key (will change on restart)")
app.config['SECRET_KEY'] = flask_secret_key

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', logger=True, engineio_logger=True)

# Import API routes
try:
    print("  → Importing API routes...", flush=True)
    print("    → Importing chat...", flush=True)
    from web.api import chat
    print("    ✓ chat imported", flush=True)
    
    print("    → Importing memory...", flush=True)
    from web.api import memory
    print("    ✓ memory imported", flush=True)
    
    print("    → Importing voice...", flush=True)
    from web.api import voice
    print("    ✓ voice imported", flush=True)
    
    print("    → Importing websocket...", flush=True)
    from web.api import websocket
    print("    ✓ websocket imported", flush=True)
    
    print("    → Importing profile...", flush=True)
    from web.api.profile import bp as profile_bp
    print("    ✓ profile imported", flush=True)
    
    print("    → Importing search...", flush=True)
    from web.api.search import bp as search_bp
    print("    ✓ search imported", flush=True)
    
    print("    → Importing emotions...", flush=True)
    from web.api.emotions import bp as emotions_bp
    print("    ✓ emotions imported", flush=True)
    
    print("    → Importing care...", flush=True)
    from web.api.care import bp as care_bp
    print("    ✓ care imported", flush=True)
    
    print("    → Importing milestones...", flush=True)
    from web.api.milestones import bp as milestones_bp
    print("    ✓ milestones imported", flush=True)
    
    print("  ✓ API routes imported", flush=True)
except Exception as e:
    print(f"  ✗ Error importing API routes: {e}", flush=True)
    logger.error(f"Error importing API routes: {e}", exc_info=True)
    raise

# Register blueprints
try:
    print("  → Registering blueprints...", flush=True)
    app.register_blueprint(chat.bp, url_prefix='/api/chat')
    app.register_blueprint(memory.bp, url_prefix='/api/memory')
    app.register_blueprint(voice.bp, url_prefix='/api/voice')
    app.register_blueprint(profile_bp, url_prefix='/api/profile')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(emotions_bp, url_prefix='/api/emotions')
    app.register_blueprint(care_bp, url_prefix='/api/care')
    app.register_blueprint(milestones_bp, url_prefix='/api/milestones')
    print("  ✓ Blueprints registered", flush=True)
except Exception as e:
    print(f"  ✗ Error registering blueprints: {e}", flush=True)
    logger.error(f"Error registering blueprints: {e}", exc_info=True)
    raise

# Register WebSocket events
try:
    print("  → Registering WebSocket events...", flush=True)
    websocket.register_events(socketio)
    print("  ✓ WebSocket events registered", flush=True)
except Exception as e:
    print(f"  ✗ Error registering WebSocket events: {e}", flush=True)
    logger.error(f"Error registering WebSocket events: {e}", exc_info=True)
    raise

print("  ✓ Web application initialization complete", flush=True)

@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template('index.html', 
                          assistant_name=Config.ASSISTANT_NAME,
                          username=Config.USERNAME)

@app.route('/favicon.ico')
def favicon():
    """Serve favicon."""
    try:
        return send_from_directory(
            os.path.join(app.root_path, 'static', 'images'),
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )
    except:
        # Return a simple SVG favicon if file doesn't exist
        from flask import Response
        svg_favicon = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="45" fill="#8b5cf6"/>
            <text x="50" y="65" font-size="50" text-anchor="middle" fill="white">✨</text>
        </svg>'''
        return Response(svg_favicon, mimetype='image/svg+xml')

@app.route('/api/config')
def get_config():
    """Get configuration (non-sensitive)."""
    return jsonify({
        'assistant_name': Config.ASSISTANT_NAME,
        'username': Config.USERNAME,
        'tts_enabled': Config.TTS_ENABLED,
        'input_language': Config.INPUT_LANGUAGE,
        'max_chat_history': Config.MAX_CHAT_HISTORY
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Validate configuration
    is_valid, error_msg = Config.validate()
    if not is_valid:
        logger.error(error_msg)
        print(error_msg)
        sys.exit(1)
    
    logger.info("Starting NOVA Web Interface...")
    logger.info(f"Access the interface at: http://localhost:5001")
    
    # Run the app
    socketio.run(app, 
                host='0.0.0.0', 
                port=5001, 
                debug=True,
                allow_unsafe_werkzeug=True)

