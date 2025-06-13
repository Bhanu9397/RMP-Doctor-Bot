from flask import Flask
from threading import Thread
import logging

app = Flask('')

@app.route('/')
def home():
    return "🩺 Medical Emergency Assistant Bot is running!"

@app.route('/health')
def health():
    return {
        "status": "healthy",
        "service": "First Aid Telegram Bot",
        "message": "Bot is running and ready to help with emergency situations"
    }

def run():
    """Run the Flask web server"""
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        logging.error(f"Flask server error: {str(e)}")

def keep_alive():
    """Start the web server in a separate thread to keep Replit alive"""
    t = Thread(target=run)
    t.daemon = True
    t.start()
    logging.info("Keep-alive web server started on port 5000")
