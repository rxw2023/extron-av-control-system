from extronlib.interface import EthernetClientInterface
from extronlib import event
from datetime import datetime 
import json
# ================= Configuration ====================
THINGSBOARD_HOST = '10.105.5.170'
THINGSBOARD_PORT = 8080
ACCESS_TOKEN = 'SlrUchlUCxC5qrq73FUj'
# ================= Network Interface =================
tb_client = EthernetClientInterface(THINGSBOARD_HOST, THINGSBOARD_PORT)
# ================= Global State =================
tb_connected = False
pending_data = None
# ================= Utility Functions =================
def send_http_request(host, token, endpoint, data=None, method='POST'):
    content = json.dumps(data) if data else ''
    headers = [
        '{0} {1} HTTP/1.1'.format(method, endpoint),
        'Host: {0}'.format(host),
        'Content-Type: application/json',
        'Authorization: Bearer {0}'.format(token),
        'Connection: close'
    ]
    if data:
        headers.append('Content-Length: {0}'.format(len(content)))
    return '\r\n'.join(headers) + '\r\n\r\n' + content
# ================= ThingsBoard Telemetry =================
@event(tb_client, 'Connected')
def on_tb_connected(interface, state):
    global tb_connected
    tb_connected = True
    send_pending_telemetry()
@event(tb_client, 'Disconnected')
def on_tb_disconnected(interface, state):
    global tb_connected
    tb_connected = False
def send_pending_telemetry():
    global pending_data
    if not tb_connected or pending_data is None:
        return
    try:
        req = send_http_request(
            THINGSBOARD_HOST, ACCESS_TOKEN,
            '/api/v1/{0}/telemetry'.format(ACCESS_TOKEN),
            pending_data
        )
        tb_client.Send(req)
        print('TB Report Success:', pending_data)
        pending_data = None
        tb_client.Disconnect()
    except Exception as e:
        print('TB Send Failed:', e)
# ----------------- Status Report -----------------
def send_telemetry(data):
    global pending_data
    try:
        pending_data = data
        if tb_connected:
            send_pending_telemetry()
        else:
            tb_client.Connect()
    except Exception as e:
        print('TB Report Exception:', e)
# ----------------- Event Log (Keep History) -----------------
def send_event(data):
    global pending_data
    try:
        data_with_ts = {
            "ts": int(datetime.now().timestamp() * 1000), 
            "values": data
        }
        pending_data = data_with_ts
        if tb_connected:
            send_pending_telemetry()
        else:
            tb_client.Connect()
    except Exception as e:
        print('TB Event Report Exception:', e)
def start():
    try:
        tb_client.Connect()
        print('Telemetry Service Started')
    except:
        print('Telemetry Start Failed')
