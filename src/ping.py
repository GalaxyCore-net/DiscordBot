import threading
import http.server
import socketserver

PORT = 9660


def ping_server(logger):
    thread_name = threading.current_thread().getName()

    class MyServer(http.server.BaseHTTPRequestHandler):

        def do_GET(self):
            self.send_response(200)
            self.send_header('Powered-By', 'Electricity')
            self.end_headers()

            self.wfile.write(f"{thread_name} running as a Ping Server.".encode("UTF-8"))

    with socketserver.TCPServer(("", PORT), MyServer) as httpd:
        logger.info("Serving forever")
        httpd.serve_forever()
