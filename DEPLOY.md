# Deployment Guide

Hướng dẫn deploy Miro to Chatbot Graph Converter cho product team.

## Option 1: Local Development (Dễ nhất)

### Quick Start

```bash
# Clone repository
git clone <repo-url>
cd mindmap2graph

# Run quick start script
chmod +x run.sh
./run.sh
```

Script sẽ tự động:
- Tạo virtual environment
- Install dependencies
- Cho bạn chọn web UI hoặc CLI

### Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run web UI
streamlit run app.py
```

Access tại: http://localhost:8501

---

## Option 2: Docker Deployment

### Prerequisites

- Docker installed
- Docker Compose installed

### Build and Run

```bash
# Build image
docker build -t mindmap2graph:latest .

# Run container
docker run -p 8501:8501 \
  -v $(pwd)/output:/app/output \
  mindmap2graph:latest
```

### Using Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access tại: http://localhost:8501

---

## Option 3: Deploy lên Cloud

### Heroku Deployment

1. **Create Heroku app**:
   ```bash
   heroku create mindmap2graph-app
   ```

2. **Add buildpack**:
   ```bash
   heroku buildpacks:set heroku/python
   ```

3. **Create Procfile**:
   ```bash
   echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
   ```

4. **Deploy**:
   ```bash
   git push heroku main
   ```

5. **Open app**:
   ```bash
   heroku open
   ```

### Streamlit Cloud (Free!)

1. **Push code to GitHub**

2. **Go to Streamlit Cloud**: https://streamlit.io/cloud

3. **Click "New app"**

4. **Connect GitHub repo**:
   - Repository: `yourusername/mindmap2graph`
   - Branch: `main`
   - Main file: `app.py`

5. **Deploy!**

App sẽ có URL dạng: `https://yourusername-mindmap2graph.streamlit.app`

**Advantages**:
- ✅ Free hosting
- ✅ Automatic updates từ GitHub
- ✅ HTTPS built-in
- ✅ Easy setup (5 minutes)

### AWS EC2 Deployment

1. **Launch EC2 instance**:
   - AMI: Ubuntu 22.04
   - Type: t2.micro (free tier)
   - Security Group: Open port 8501

2. **SSH vào instance**:
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Setup application**:
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y

   # Install Python
   sudo apt install python3-pip python3-venv -y

   # Clone repo
   git clone <repo-url>
   cd mindmap2graph

   # Install dependencies
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

   # Run with nohup
   nohup streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &
   ```

4. **Access**: http://your-ec2-ip:8501

### Google Cloud Run

1. **Create Dockerfile** (already included)

2. **Build and push**:
   ```bash
   # Set project
   gcloud config set project YOUR_PROJECT_ID

   # Build image
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/mindmap2graph

   # Deploy
   gcloud run deploy mindmap2graph \
     --image gcr.io/YOUR_PROJECT_ID/mindmap2graph \
     --platform managed \
     --region asia-southeast1 \
     --allow-unauthenticated
   ```

3. **Access**: URL will be provided after deployment

---

## Option 4: Nginx Reverse Proxy (Production)

### Setup

```bash
# Install Nginx
sudo apt install nginx

# Create Nginx config
sudo nano /etc/nginx/sites-available/mindmap2graph
```

Add config:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/mindmap2graph /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### SSL with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renew
sudo certbot renew --dry-run
```

---

## Production Checklist

### Security

- [ ] Change default port (8501 → custom)
- [ ] Setup SSL/TLS (HTTPS)
- [ ] Use strong passwords for .env
- [ ] Limit API rate limiting
- [ ] Setup firewall rules
- [ ] Enable CORS properly
- [ ] Hide sensitive errors in production

### Performance

- [ ] Use production WSGI server (Gunicorn)
- [ ] Enable caching
- [ ] Setup CDN for static files
- [ ] Use persistent storage for outputs
- [ ] Setup database for results (if needed)

### Monitoring

- [ ] Setup logging (ELK, CloudWatch)
- [ ] Error tracking (Sentry)
- [ ] Uptime monitoring (UptimeRobot)
- [ ] Performance monitoring (New Relic)
- [ ] Setup alerts

### Backup

- [ ] Backup .env files
- [ ] Backup output files
- [ ] Database backups (if applicable)
- [ ] Code versioning (Git)

---

## Environment Variables

### Development (.env.example)

```bash
MIRO_ACCESS_TOKEN=your_dev_token
MIRO_BOARD_ID=your_dev_board_id
MIRO_API_BASE_URL=https://api.miro.com/v2
```

### Production

Use secrets management:

**AWS Secrets Manager**:
```bash
aws secretsmanager create-secret \
    --name mindmap2graph/miro-token \
    --secret-string "your_token"
```

**Heroku**:
```bash
heroku config:set MIRO_ACCESS_TOKEN=your_token
```

**Docker**:
```bash
docker run -e MIRO_ACCESS_TOKEN=your_token ...
```

---

## Troubleshooting

### Port already in use

```bash
# Find process using port 8501
lsof -i :8501

# Kill process
kill -9 <PID>
```

### Permission denied

```bash
# Make run.sh executable
chmod +x run.sh

# Fix file permissions
chmod 644 *.py
chmod 755 .
```

### Module not found

```bash
# Activate venv first
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Docker build fails

```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t mindmap2graph:latest .
```

---

## Scaling

### Horizontal Scaling

Use load balancer với multiple instances:

```yaml
# docker-compose-scaled.yml
version: '3.8'
services:
  web:
    build: .
    deploy:
      replicas: 3
    ports:
      - "8501-8503:8501"
```

Run:
```bash
docker-compose -f docker-compose-scaled.yml up --scale web=3
```

### Vertical Scaling

Increase container resources:

```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

---

## Monitoring Commands

### Check app status

```bash
# Check if Streamlit is running
ps aux | grep streamlit

# Check port
netstat -tulpn | grep 8501

# Check logs
tail -f nohup.out  # if using nohup
docker-compose logs -f  # if using Docker
```

### Health check

```bash
# HTTP health check
curl http://localhost:8501/_stcore/health
```

---

## Update Deployment

### Update code

```bash
# Pull latest code
git pull origin main

# Restart application
# Option 1: Kill and restart
pkill -f streamlit
streamlit run app.py &

# Option 2: Docker
docker-compose down
docker-compose up -d --build
```

### Update dependencies

```bash
pip install -r requirements.txt --upgrade
```

---

## Cost Estimation

### Free Tier Options

1. **Streamlit Cloud**: Free (1 GB RAM)
2. **Heroku Free Tier**: Deprecated (use hobby $7/month)
3. **AWS Free Tier**: t2.micro for 1 year
4. **Google Cloud**: $300 credit for 3 months

### Paid Options

1. **AWS EC2 t2.small**: ~$17/month
2. **Digital Ocean Droplet**: $6-12/month
3. **Heroku Hobby**: $7/month
4. **Google Cloud Run**: Pay per use (~$5-20/month)

**Recommended for Small Team**: Streamlit Cloud (Free) or Digital Ocean ($6/month)

---

## Support

Nếu gặp vấn đề khi deploy:

1. Check logs first
2. Read error messages carefully
3. Search GitHub Issues
4. Create new issue với:
   - Environment details
   - Error logs
   - Steps to reproduce

Happy deploying! 🚀
