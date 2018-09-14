from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
import workbook
import builder
import urllib
import os
 
__author__ = 'Luiz Fernando Surian Filho'

class StaticServer(BaseHTTPRequestHandler):
 
    def do_GET(self):
        root = os.path.join(os.path.dirname(__file__), 'bin')
        if self.path == '/':
            filename = root + '/index.html'
        else:
            filename = root + self.path
 
        self.send_response(200)
        if filename[-5:] == '.xlsx':
            self.send_header('Content-type', 'application/octet-stream')
        elif filename[-5:] == '.json':
            self.send_header('Content-type', 'application/json')
        elif filename[-3:] == '.js':
            self.send_header('Content-type', 'application/javascript')
        elif filename[-4:] == '.ico':
            self.send_header('Content-type', 'image/x-icon')
        elif filename[-4:] == '.css':
            self.send_header('Content-type', 'text/css')
        else:
            self.send_header('Content-type', 'text/html')
            
        self.end_headers()
        with open(filename, 'rb') as fh:
            html = fh.read()
            self.wfile.write(html)

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        file_name = workbook.write(post_data)
        self.wfile.write( file_name.encode('utf-8') )
 
def run(server_class=HTTPServer, handler_class=StaticServer, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port', port)
    webbrowser.open(f'http://localhost:{port}', new=2)
    httpd.serve_forever()

if __name__ == "__main__":
    if builder.build():
        run()

    else:
        print('stopping')
        os.system('pause')
 
