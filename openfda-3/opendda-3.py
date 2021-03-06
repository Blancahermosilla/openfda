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

        drugs = json.loads(repos_raw)  # sintax reading


        message = 'This is the list with the ten drugs:'
        for i in range(len(drugs['results'])):
            try:
               message += '<ol>'+ str(i+1) + '. ' + drugs['results'][i]['openfda']['generic_name'][0] + '</ol>'

            except KeyError:
                message += '<ol>'+ str(i+1) + '. ' + ('No generic name found')+ '</ol>'

        # write the content
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