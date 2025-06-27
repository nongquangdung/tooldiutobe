#!/bin/bash

echo "🌊 VOICE STUDIO LICENSE SERVER - DIGITALOCEAN DEPLOYMENT"
echo "========================================================"

echo "📋 Enter your server IP address:"
read -r SERVER_IP

echo "📋 Enter your domain name (e.g., license.yoursite.com):"
read -r DOMAIN_NAME

echo "🔐 Connecting to server $SERVER_IP..."

# Create deployment script on server
ssh root@$SERVER_IP << EOF
echo "🛠️  Setting up Voice Studio License Server..."

# Update system
apt update && apt upgrade -y

# Install required packages
apt install python3 python3-pip git nginx certbot python3-certbot-nginx htop -y

# Clone repository (assuming you've pushed to GitHub)
echo "📥 Enter your Git repository URL:"
read -r REPO_URL
git clone \$REPO_URL /opt/voice-studio-license
cd /opt/voice-studio-license/license_server

# Install Python dependencies
pip3 install -r requirements.txt

# Create systemd service
cat > /etc/systemd/system/license-server.service << 'SERVICE_EOF'
[Unit]
Description=Voice Studio License Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/voice-studio-license/license_server
ExecStart=/usr/bin/python3 server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE_EOF

# Start and enable service
systemctl daemon-reload
systemctl enable license-server
systemctl start license-server

# Check service status
systemctl status license-server

# Setup Nginx
cat > /etc/nginx/sites-available/license-server << 'NGINX_EOF'
server {
    listen 80;
    server_name $DOMAIN_NAME;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
NGINX_EOF

# Enable Nginx site
ln -sf /etc/nginx/sites-available/license-server /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# Setup SSL with Let's Encrypt
certbot --nginx -d $DOMAIN_NAME --non-interactive --agree-tos --email admin@$DOMAIN_NAME

# Create demo licenses
cd /opt/voice-studio-license/license_server
python3 admin.py demo

echo ""
echo "🎉 DIGITALOCEAN DEPLOYMENT SUCCESSFUL!"
echo "====================================="
echo "Server: https://$DOMAIN_NAME"
echo "Health Check: https://$DOMAIN_NAME/health"
echo ""
echo "📊 Monitoring commands:"
echo "  systemctl status license-server    # Check service"
echo "  journalctl -u license-server -f    # View logs"
echo "  htop                               # Monitor resources"
echo ""
echo "📋 Next steps:"
echo "1. Update src/core/license_manager.py with: self.license_server_url = \"https://$DOMAIN_NAME\""
echo "2. Test with: python simple_license_demo.py"
echo "3. Setup monitoring: https://uptimerobot.com"
echo "4. Start selling licenses! 💰"

EOF

echo ""
echo "🔧 Local setup complete! Server is being configured..."
echo "   SSH connection will show the setup progress." 