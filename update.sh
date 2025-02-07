#!/bin/bash

echo "Pulling latest code from GitHub..."
git pull origin main

echo "Restarting the bot..."
pkill -f api/main.py
nohup python3 api/main.py > logs/bot.log 2>&1 &

echo "Bot updated and restarted successfully!"
