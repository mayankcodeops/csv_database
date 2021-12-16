from http.server import BaseHTTPRequestHandler, HTTPServer
from form import form_html
import multipart


class Handler(BaseHTTPRequestHandler):
    """Subclass of BaseHTTPRequestHandler from http.server lib to handle requests for the CSV uploading server"""
    def get_path(self):
        """Returns the path or route upon which the GET requests has been made"""
        return self.path[1:]

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """Basic GET request dispatcher with rudimentary route parsing"""
        self._set_headers()

        if self.get_path() == 'upload_csv':
            message = form_html
            self.wfile.write(bytes(message, "utf8"))
        else:
            message = f"<h1>Welcome to CSV Uploader, {self.get_path()}!</h2>"
            self.wfile.write(bytes(message, "utf-8"))

    def do_POST(self):
        """Basic POST request handler to handle the upload of CSV files
            Sends OK response if the CSV file is valid,else will send some error response.
        """
        self._set_headers()
        fields = {}
        files = {}
        if self.get_path() == 'upload_csv':
            def on_field(field):
                fields[field.field_name] = field.value

            def on_file(file):
                files[file.field_name] = {'name': file.file_name, 'file_object': file.file_object}

            multipart_headers = {'Content-Type': self.headers['Content-Type'],
                                 'Content-Length': int(self.headers['Content-Length'])}
            multipart.parse_form(multipart_headers, self.rfile, on_field, on_file)
            print(fields)
            print(files)
            self.send_response(201, 'Created')
            self.end_headers()
            self.wfile.write("<h1>File Uploaded</h1>".encode('utf8'))
        else:
            message = "<h1>File Upload Not successful</h1>"
            self.wfile.write(bytes(message, "utf8"))


with HTTPServer(('', 8000), Handler) as server:
    server.serve_forever()
