from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import datetime
from TransmittedData import transmittedData
from timeCon import local_to_GPSWeekSecond

# data = {'result': 'this is a test'}
# host = ('192.168.31.107', 8888)
host = ('10.215.20.240',8888)

data = dict()

#data = {'result': 'this is a test'}
def GenerateData():
    global data
    nowTime = datetime.datetime.now().strftime('%Y %m %d %H %M %S')#现在
    second = local_to_GPSWeekSecond(nowTime)

    data = transmittedData(374353)



class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        global data
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        GenerateData()
        self.wfile.write(json.dumps(data).encode())

    

if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
