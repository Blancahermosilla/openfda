import http.server
import socketserver
import http.client
import json

##-- IP and the port of the server
IP = "localhost"  # local machine
PORT = 8002

##HTTPRequestHandler class
class server_blanca(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        headers = {'User-Agent': 'http-client'}

        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json?limit=10", None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode("utf-8")
        conn.close()

        repos = json.loads(repos_raw)  # sintax reading

        # send message back to client
        if self.path == "/get10drugs":
            filename = "10drugs.html"

            # write content of the file
            with open('10drugs.html', "w") as f:
                self.wfile.write(bytes('''<html><head>
                        <h3>This is the list with the 10 drugs:<h3></head><body><ol>''', "utf8"))
                for i in range(len(repos['results'])):
                    self.wfile.write(bytes('<li>', "utf8"))
                    try:
                        self.wfile.write(bytes(repos['results'][i]['openfda']['generic_name'][0], "utf8"))
                    except KeyError:
                        self.wfile.write(bytes('no generic name found', "utf8"))
                    self.wfile.write(bytes('\n', "utf8"))

                self.wfile.write(bytes('</li></ol></body></html>', "utf8"))
                f.close()
            print(filename, "served!")

        elif self.path == "/":
            filename = "empty.html"
            # content of the file
            with open('empty.html', 'w')as g:
                self.wfile.write(bytes('''<html><head>
                            <h3>There is no request<h3>
                            </head>
                            <body><a href="http://localhost:8002/get10drugs"></a> 
                            </body></html>''', "utf8"))
                g.close

            print(filename, "served!")


        else:
            filename = "error.html"
            # content of the file
            with open('error.html', 'w')as h:
                self.wfile.write(bytes('<html><head><h3>ERROR!<h3></head></html>',"utf8"))
                h.close()
            print(filename, "served!")


        return


# Handler = http.server.SimpleHTTPRequestHandler
Handler = server_blanca

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Server stopped!")