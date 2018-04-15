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

        # return search.html by default
        message = ''
        if self.path == '/':
            with open('search.html', 'r') as f:
                message = f.read()
            self.wfile.write(bytes(message, "utf8"))

        elif 'search' in self.path:
            #self.wfile.write(bytes(self.path, "utf8"))
            #print(self.path)
            list1 = self.path.strip('search?').split('&')
            drug =list1[0].split('=')[1]
            limit = list1[1].split('=')[1]
            #print(drug,limit)


            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?search=generic_name:" + drug + "&limit=" + limit , None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            drugs = json.loads(repos_raw)

            message = ''
            for i in range(len(drugs['results'])):
                message += "<ol>" + drugs["results"][i]["id"] + "</ol>"

            self.wfile.write(bytes(message, "utf8"))


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
