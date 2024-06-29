import json
import re
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading
from productBL import ProductBL
from config import HTTP_SERVER, HTTP_PORT
import http.cookies

class HttpReqHandler(BaseHTTPRequestHandler):
    bl = None
    
    def __init__(self, *args, **kwargs):
        # Initialize ProductBL instance if not already initialized
        if self.bl is None:
            self.bl = ProductBL()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        cookie = http.cookies.SimpleCookie(self.headers.get('Cookie'))
        if 'client_id' in cookie:
            client_id = cookie['client_id'].value
            print(f"Thread assigned : {threading.current_thread().ident}, Client ID: {client_id}")
        if re.search('/orders', self.path):
            length = int(self.headers.get('content-length'))
            data = self.rfile.read(length).decode('utf8')
            json_data = json.loads(data)
            name = json_data.get('name', '')
            quantity = json_data.get('quantity', '')
            # Call the order method from ProductBL and handle response
            resp_data = self.bl.order(name, int(quantity))
            if resp_data.OrderNumber != -1:  
                resp_data = {
                    "data": {
                        "order_number": resp_data.OrderNumber
                    }
                }
            else:
                resp_data = {
                    "error": {
                        "code": 304,
                        "message": "could not post order"
                    }
                }
            # Send response to client
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(resp_data).encode('utf-8'))    
        else:
            # Send forbidden response for non-matching path
            self.send_response(403)
            self.end_headers()

    def do_GET(self):
        cookie = http.cookies.SimpleCookie(self.headers.get('Cookie'))
        if 'client_id' in cookie:
            client_id = cookie['client_id'].value
            print(f"Thread assigned : {threading.current_thread().ident}, Client ID: {client_id}")
        if re.search(r'^/products/[\w-]+$', self.path):
            name = self.path.split('/')[-1]
            # Call the get_catalog method from ProductBL and handle response
            resp_data = self.bl.get_catalog(name)
            if resp_data.Name != "":
                # Send success response with product details
                resp_data = {
                    "data": {
                        "name": resp_data.Name,
                        "price": resp_data.Cost,
                        "quantity": resp_data.Stock
                    }
                }
            else:
                # Send not found response if product name is empty
                resp_data = {
                    "error": {
                        "code": 404,
                        "message": "product not found"
                    }
                }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(resp_data).encode('utf-8'))
        else:
            # Send forbidden response for non-matching path
            self.send_response(403)
            self.end_headers()

if __name__ == '__main__':
    http_service = os.getenv("HTTP_SERVER", HTTP_SERVER)
    server = ThreadingHTTPServer((http_service, HTTP_PORT), HttpReqHandler)
    print(f"Starting server on {http_service}:{HTTP_PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
