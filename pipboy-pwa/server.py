#!/usr/bin/env python3
"""
Pip-Boy Framework Server
Serves the PWA on port 5000 with proper headers for service workers
"""

import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import mimetypes

class PipBoyHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler with proper MIME types and headers for PWA"""
    
    def end_headers(self):
        # Add headers for service worker and CORS
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Service-Worker-Allowed', '/')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    
    def guess_type(self, path):
        """Ensure correct MIME types for PWA files"""
        mimetype = super().guess_type(path)
        if path.endswith('.js'):
            return 'application/javascript'
        elif path.endswith('.json'):
            return 'application/json'
        elif path.endswith('.css'):
            return 'text/css'
        elif path.endswith('.html'):
            return 'text/html'
        return mimetype

def run_server(port=5000):
    """Start the Pip-Boy Framework server"""
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Set up MIME types
    mimetypes.init()
    mimetypes.add_type('application/javascript', '.js')
    mimetypes.add_type('application/json', '.json')
    mimetypes.add_type('text/css', '.css')
    
    # Create server
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, PipBoyHTTPRequestHandler)
    
    print(f"""
╔══════════════════════════════════════════╗
║         PIP-BOY FRAMEWORK SERVER         ║
╠══════════════════════════════════════════╣
║  Status: ONLINE                          ║
║  Port: {port}                              ║
║  Access: http://localhost:{port}           ║
║                                          ║
║  Press Ctrl+C to shutdown                ║
╚══════════════════════════════════════════╝
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n[SHUTDOWN] Pip-Boy Framework server stopping...")
        httpd.shutdown()
        sys.exit(0)

if __name__ == '__main__':
    run_server()