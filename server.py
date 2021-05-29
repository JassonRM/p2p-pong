import json
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer
from uuid import uuid4
from players_connection_list import PlayerList
host_port = 8000
player_list = PlayerList()

def save_token(token):
    """This function saves a session token to disk"""

    path = "tokens.json"
    file = open(path, mode="r+")
    tokens = json.loads(file.read())
    tokens.append(token)
    file.seek(0)
    file.truncate()
    json.dump(tokens, file)
    file.close()


class Server(BaseHTTPRequestHandler):
    '''HTTP server with a RESTful API'''

    def do_HEAD(self):
        """This method generates the header for every request path"""

        self.send_response(200)
        mimetype, _ = mimetypes.guess_type(self.path)
        self.send_header('Content-type', mimetype)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        """This method resolves GET requests to the server, whether its for the API or a website"""
        path = self.path.split("?")[0]
        if self.path == "/":
            data = player_list.get_list_as_JSON()
            self.do_HEAD()
            self.wfile.write(data)
        else:
            self.resource_not_found()

    def do_POST(self):
        """This method resolves POST requests to the API"""

        # Get the size of data
        content_length = int(self.headers['Content-Length'])
        # Get the data
        post_data = self.rfile.read(content_length)

        if self.path == "/host":
            player_list.add_or_change(post_data)
        elif self.path == "/remove":
            player_list.remove(post_data)
        else:
            self.resource_not_found()


    def do_OPTIONS(self):
        """This method resolves OPTIONS requests to any path"""
        self.do_HEAD()

    def send_player_list(self, path):
        """This method reads a file from disk and sends it as response of a request"""
        try:
            file = open(path, mode='rb')
            data = file.read()
            file.close()
            self.do_HEAD()
            self.wfile.write(data)
        except IOError:
            self.resource_not_found()


    def resource_not_found(self):
        """This method responds with HTTP error 404 when a resource is not found"""

        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()


if __name__ == '__main__':
    http_server = HTTPServer(('', host_port), Server)
    print("Server started on port: %s" % host_port)

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()