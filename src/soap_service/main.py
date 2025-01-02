from wsgiref.simple_server import make_server
from .nfl_service import wsgi_application
import os

def run_server():
    port = int(os.environ.get('PORT', 8000))
    server = make_server('0.0.0.0', port, wsgi_application)
    print(f"SOAP service running on port {port}...")
    server.serve_forever()

if __name__ == "__main__":
    run_server() 