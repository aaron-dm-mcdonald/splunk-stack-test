# log-generator/app.py
import json
import time
import random
import socket
import requests
import threading
import os
from flask import Flask

app = Flask(__name__)

# Config from env vars
SPLUNK_HEC_URL = os.getenv('SPLUNK_HEC_URL', 'http://splunk:8088/services/collector')
SPLUNK_HEC_TOKEN = os.getenv('SPLUNK_HEC_TOKEN', '12345678-1234-1234-1234-123456789012')
SYSLOG_SERVER = os.getenv('SYSLOG_SERVER', 'rsyslog')
SYSLOG_PORT = int(os.getenv('SYSLOG_PORT', '514'))

# Stats
stats = {"total": 0, "hec": 0, "syslog": 0}

def send_to_splunk(data):
    headers = {'Authorization': f'Splunk {SPLUNK_HEC_TOKEN}'}
    payload = {"time": int(time.time()), "event": data}
    requests.post(SPLUNK_HEC_URL, json=payload, headers=headers)
    stats["hec"] += 1

def send_to_syslog(message):
    syslog_msg = f"<134>log-generator: {message}"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(syslog_msg.encode(), (SYSLOG_SERVER, SYSLOG_PORT))
    sock.close()
    stats["syslog"] += 1

def generate_log():
    logs = [
        {"level": "INFO", "message": f"User login: user{random.randint(1,100)}"},
        {"level": "ERROR", "message": f"Database timeout: {random.randint(30,120)}s"},
        {"level": "WARNING", "message": f"High CPU: {random.randint(80,95)}%"},
    ]
    return random.choice(logs)

def log_worker():
    while True:
        log_data = generate_log()
        stats["total"] += 1
        send_to_splunk(log_data)
        send_to_syslog(f"[{log_data['level']}] {log_data['message']}")
        time.sleep(random.uniform(2, 8))

@app.route('/')
def home():
    return f'''
    <h1>Log Generator</h1>
    <p>Stats: {stats}</p>
    <button onclick="fetch('/generate', {{method: 'POST'}}).then(() => location.reload())">
        Generate Log
    </button>
    <br><br>
    <a href="/monitoring">Splunk</a> | <a href="/">Home</a>
    '''

@app.route('/generate', methods=['POST'])
def manual_generate():
    log_data = generate_log()
    stats["total"] += 1
    send_to_splunk(log_data)
    send_to_syslog(f"[{log_data['level']}] {log_data['message']}")
    return json.dumps(log_data)

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    # Start background logging
    threading.Thread(target=log_worker, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)