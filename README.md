# README.md
# Monitoring Stack with Docker Compose

This Docker Compose stack provides a complete monitoring solution with Splunk, syslog, Nginx reverse proxy, and Apache web server.

## Architecture

```
Internet → Nginx (Port 80) → {
    / → Apache HTTP Server
    /monitoring → Splunk Web UI (Port 8000)
    /test → Log Generator Service (Port 5000)
}

Log Flow:
Log Generator → {
    Splunk HEC (Port 8088)
    Rsyslog (Port 514)
} → Splunk Indexer
```

## 📁 Directory Structure

```
monitoring-stack/
├── docker-compose.yml
├── startup.sh
├── nginx/
│   ├── nginx.conf
│   └── conf.d/default.conf
├── apache/
│   └── index.html
├── splunk/
│   └── inputs.conf
├── rsyslog/
│   └── rsyslog.conf
└── log-generator/
    └── app.py
```

## 🔧 Configuration

### Splunk
- **URL:** `http://your-ec2-ip:8000`
- **Username:** `admin`
- **Password:** `changeme123`
- **HEC Token:** `12345678-1234-1234-1234-123456789012`

### Ports Exposed
- **80:** Nginx reverse proxy
- **8000:** Splunk Web UI (direct access)
- **8088:** Splunk HEC
- **514:** Rsyslog (UDP/TCP)

## 🔍 Monitoring Features

1. **HTTP Event Collector (HEC):** Enabled on port 8088
2. **Syslog Collection:** UDP/TCP on port 514
3. **Log Generation:** Automated test log generation
4. **Web Interface:** Easy access via reverse proxy

## 📊 Usage

1. **View Logs in Splunk:**
   - Go to `/monitoring`
   - Login with admin/changeme123
   - Search for `index=main` to see all logs

2. **Generate Test Logs:**
   - Visit `/test` to see the log generator interface
   - Logs are automatically generated every 1-5 seconds
   - Manual log generation available via web interface

3. **Monitor System:**
   - Check service status: `docker-compose ps`
   - View logs: `./logs.sh [service_name]`
   - Stop stack: `./stop.sh`

## 🔒 Security Notes

- **Change default passwords** before production use
- **Configure firewall** to restrict access to necessary ports
- **Use SSL/TLS** for production deployments
- **Rotate HEC tokens** regularly

## 🐛 Troubleshooting

1. **Services not starting:**
   ```bash
   docker-compose logs [service_name]
   ```

2. **Splunk not accessible:**
   - Wait 2-3 minutes for Splunk to fully initialize
   - Check if port 8000 is accessible

3. **Logs not appearing in Splunk:**
   - Check HEC configuration in Splunk
   - Verify network connectivity between services

## 📈 Scaling

To scale the log generator:
```bash
docker-compose up -d --scale log-generator=3
```

## 🛠️ Customization

- **Modify log types:** Edit `log-generator/log_generator.py`
- **Change proxy rules:** Edit `nginx/conf.d/default.conf`
- **Add Splunk apps:** Mount additional volumes to `/opt/splunk/etc/apps/`# splunk-stack-test
