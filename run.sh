#!/bin/bash

echo "Starting Telegram Trading Bot..."
nohup python3 api/main.py > logs/bot.log 2>&1 &

echo "Bot started successfully!"
