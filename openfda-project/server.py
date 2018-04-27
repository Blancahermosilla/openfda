import http.server
import socketserver
import http.client
import json

##-- IP and the port of the server
IP = "localhost"  # local machine
PORT = 8000

socketserver.TCPServer.allow_reuse_address = True


##HTTPRequestHandler class
class server_blanca(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        def send_query(req,p1,limit):

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?search=" + req + p1 + '&limit=' + limit, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            drugs = json.loads(repos_raw)

            return drugs




        if self.path == '/':
            message= ''
            with open('search2.html', 'r') as f:
                message = f.read()
            self.wfile.write(bytes(message, "utf8"))

        elif 'search' in self.path:


            # print(self.path)
            params = self.path.strip('search?').split('&')
            p1 = params[0].split('=')[1]
            limit = params[1].split('=')[1]
            # print(drug,limit)

            if 'drug' in self.path:
                # self.wfile.write(bytes(self.path, "utf8"))
                req = 'generic_name:'

            elif 'company' in self.path:
                req = 'manufacturer_name:'

            drugs= send_query(req,p1,limit)
            self.wfile.write(bytes(str(drugs), "utf8"))



        elif 'get_list' in self.path:


            params = self.path.strip('get_list?')
            limit = params.split('=')[1]
            req = ''
            p1 = ''
            print(limit)

            drugs= send_query(req,p1,limit)

            mes = ''

            if 'drug' in self.path:
                get = 'generic_name'

            elif 'company' in self.path:
                get = 'manufacturer_name'

            for i in range(len(drugs['results'])):
                try:
                    mes += '<ol>' + str(i + 1) + '. ' + drugs['results'][i]['openfda'][get][0] + '</ol>'

                except KeyError:
                    mes += '<ol>' + str(i + 1) + '. ' + ('No generic name found') + '</ol>'

            self.wfile.write(bytes(mes, "utf8"))

        elif 'listWarnings' in self.path:
            params = self.path.strip('listWarnings?').split('=')
            limit = params[1]
            print(limit)
            req = ''
            p1 = ''

            drugs = send_query(req, p1, limit)
            mes=''
            for i in range(len(drugs['results'])):
                try:
                    mes += '<ol>' + str(i + 1) + '. ' + drugs['results'][i]['warnings'][0] + '</ol>'

                except KeyError:
                    mes += '<ol>' + str(i + 1) + '. ' + ('No warnings found') + '</ol>'

            self.wfile.write(bytes(mes, "utf8"))









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