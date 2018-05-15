import http.server
import socketserver
import http.client
import json

##-- IP and the port of the server
IP = "localhost"  # local machine
PORT = 8000

socketserver.TCPServer.allow_reuse_address = True

#https://api.fda.gov/drug/label.json?search=manunfacturer_name=bayer&limit=10
#req = the parameter ex: manufacturer_name=
#p1 = the value of the parameter ex: bayer


#includes the logic to communicate with the openFDA API
class OpenFDAClient():

    def send_query(self, req, p1, limit):
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json?search=" + req + p1 + '&limit=' + limit, None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode("utf-8")
        conn.close()

        drugs = json.loads(repos_raw)

        return drugs


class OpenFDAParser():  # includes the logic to extract the data

    def parse_drugs(self, drugs): #when searching drugs according to active ingredient or company name, return brand name list
        list_ = []
        for i in range(len(drugs['results'])):
            try:
                list_.append(str(i + 1) + '. ' + drugs['results'][i]['openfda']['brand_name'][0])

            except KeyError:
                list_.append(str(i + 1) + '. ' + 'Not found')

        return list_

    def parse_companies(self, drugs): #return the manufactureer name
        list_ = []
        for i in range(len(drugs['results'])):
            try:
                list_.append(str(i + 1) + '. ' + drugs['results'][i]['openfda']['manufacturer_name'][0])

            except KeyError:
                list_.append(str(i + 1) + '. ' + 'Not found')

        return list_

    def parse_warnings(self, drugs):
        list_ = []
        for i in range(len(drugs['results'])):
            try:
                list_.append(str(i + 1) + '. ' + drugs['results'][i]['warnings'][0])

            except KeyError:
                list_.append(str(i + 1) + '. ' + 'Not found')

        return list_


#ncludes the logic to html visualization
class OpenFDAHTML():
    def html_list(self, list_):
        html = '<ul>'
        for i in list_:
            html += '<li>' + i + '</li>'
        html += '</ul>'

        return html

#HTTPRequestHandler class
class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):

        client = OpenFDAClient()
        parser = OpenFDAParser()
        html = OpenFDAHTML()

        #iniciar variables
        code = 200
        limit = '10'
        req = ''
        p1 = ''
        info = ''
        http_res= ''

        if self.path == '/' or self.path == '/favicon.ico':
            with open('search.html', 'r') as f:
                http_res = f.read()

        elif 'search' in self.path:

            if 'searchDrug' in self.path:
                #  Se supone parametro 1 DRUG
                #            parametro 2 LIMIT
                params =self.path.split('&')
                req = 'active_ingredient='

            elif 'searchCompany' in self.path:
                params = self.path.split('&')
                req = 'manufacturer_name='

            p1 = params[0].split('=')[1]
            if 'limit' in self.path:
                limit = params[1].split('=')[1]
                if params[1].split('=')[1]== '':
                    limit= '10'

            else:
                limit

            try:
                drugs = client.send_query(req, p1, limit)
                info = parser.parse_drugs(drugs)
                http_res = html.html_list(info)

            except KeyError:
                code = 404
                with open('error.html', 'r') as f:
                    http_res = f.read()


        elif 'list' in self.path:
            params = self.path.strip('?')
            if params.split('=')[1]== '':
                limit
            else:
                limit = params.split('=')[1]

            # print(limit)
            if 'listDrug' in self.path:
                drugs = client.send_query(req, p1, limit)
                info = parser.parse_drugs(drugs)
                http_res = html.html_list(info)

            elif 'listCompanies' in self.path:
                drugs = client.send_query(req, p1, limit)
                info = parser.parse_companies(drugs)
                http_res = html.html_list(info)

            elif 'listWarnings' in self.path:
                params = self.path.strip('listWarnings?').split('=')
                if params[1]== '':
                    limit
                else:
                    limit=params[1]

                drugs = client.send_query(req, p1, limit)
                info = parser.parse_warnings(drugs)
                http_res = html.html_list(info)

        elif 'secret' in self.path:
            code = 401

        elif 'redirect' in self.path:
            code = 302

        else:
            code = 404
            with open('error.html', 'r') as f:
                http_res = f.read()

        # Send response status code
        self.send_response(code)

        # Send the correct header
        if 'secret' in self.path:
            self.send_header('WWW-Authenticate', 'Basic realm="OpenFDA Private Zone"')
            self.end_headers()
        elif 'redirect' in self.path:
            self.send_header('Location', 'http://localhost:8000/')
            self.end_headers()
        else:
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        #  Write content as utf-8 data
        self.wfile.write(bytes(str(http_res), "utf8"))
        return

# Handler = http.server.SimpleHTTPRequestHandler
Handler = HTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Server stopped!")

#by Blanca Hermosilla Campos