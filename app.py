from flask import Flask, render_template, jsonify
import os
import socket
import datetime
import psutil
from collections import Counter

app = Flask(__name__)

# Visit counter
visit_count = Counter()

@app.route('/')
def home():
    visit_count['total'] += 1
    return render_template('index.html')

@app.route('/api/info')
def get_info():
    """API endpoint to get container and system information"""
    try:
        # Get container/host information
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        
        # Get system resources
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Get environment variables
        env_vars = {
            'ENVIRONMENT': os.getenv('ENVIRONMENT', 'development'),
            'APP_VERSION': os.getenv('APP_VERSION', '1.0.0'),
            'CUSTOM_MESSAGE': os.getenv('CUSTOM_MESSAGE', 'Welcome to Docker Workshop!'),
        }
        
        return jsonify({
            'success': True,
            'container': {
                'hostname': hostname,
                'ip_address': ip_address,
            },
            'stats': {
                'cpu_usage': f"{cpu_percent}%",
                'memory_usage': f"{memory.percent}%",
                'memory_available': f"{memory.available / (1024**3):.2f} GB",
                'disk_usage': f"{disk.percent}%",
            },
            'environment': env_vars,
            'visits': visit_count['total'],
            'timestamp': datetime.datetime.now().isoformat(),
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint for Docker"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.datetime.now().isoformat()})

if __name__ == '__main__':
    print(f"Starting Docker Workshop Demo App...")
    print(f"🌐 Server running on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
    