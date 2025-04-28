# keepalive.py
import http.server
import shlex
import socketserver
import logging
import os
import subprocess

PORT = 8080
LOG_FILE = "keepalive.log"

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format="%(asctime)s - %(message)s")

class KeepAliveHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Server is alive!\n")
            logging.info(f"STATUS CHECK from {self.client_address[0]}")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_POST(self):
        if self.path == "/message":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")

            # 🚨 VULNERABILITY: Unvalidated input (can be used for command injection)
            response = os.popen(f"echo {post_data}").read()
            # response = subprocess.run(["echo", shlex.quote(post_data)], capture_output=True, text=True).stdout

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(response.encode())
           
            safe_message = post_data.replace("\n", "\\n").replace("\r", "\\r")
            logging.info(f"Received message: {safe_message}")

            # logging.info(f"Received message: {post_data}")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), KeepAliveHandler) as httpd:
        logging.info(f"Serving on port {PORT}")
        print(f"KeepAlive Server running on port {PORT}...")
        httpd.serve_forever()
