#!/bin/bash

echo "🚀 VOICE STUDIO LICENSE SERVER - HEROKU DEPLOYMENT"
echo "=================================================="

# Check if heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found!"
    echo "   Install from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if user is logged in
if ! heroku auth:whoami &> /dev/null; then
    echo "🔐 Please login to Heroku..."
    heroku login
fi

echo "📋 Enter your app name (e.g., my-voice-studio-license):"
read -r APP_NAME

echo "📦 Creating Heroku app: $APP_NAME"
cd license_server

# Initialize git if not exists
if [ ! -d ".git" ]; then
    git init
fi

# Add files
git add .
git commit -m "Deploy Voice Studio License Server" || echo "No changes to commit"

# Create Heroku app
heroku create "$APP_NAME" || echo "App already exists"

# Deploy
echo "🚀 Deploying to Heroku..."
git push heroku main || git push heroku master

# Create demo licenses
echo "📝 Creating demo licenses..."
heroku run "python admin.py demo" --app "$APP_NAME"

# Show app URL
APP_URL=$(heroku info --app "$APP_NAME" | grep "Web URL" | awk '{print $3}')
echo ""
echo "🎉 DEPLOYMENT SUCCESSFUL!"
echo "========================"
echo "App URL: $APP_URL"
echo "Health Check: ${APP_URL}health"
echo ""
echo "📋 Next steps:"
echo "1. Update src/core/license_manager.py with: self.license_server_url = \"$APP_URL\""
echo "2. Test with: python simple_license_demo.py"
echo "3. Start selling licenses! 💰" 