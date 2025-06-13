# GitHub Setup Guide for Dr. Priya Medical Bot

## Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and log in
2. Click "New" repository button
3. Repository name: `dr-priya-medical-bot`
4. Description: `Indian Medical Emergency Assistant Telegram Bot with Dr. Priya AI`
5. Make it Public
6. Don't initialize with README (we already have one)
7. Click "Create repository"

## Step 2: Download Project Files

Download these files from your Replit project:

### Core Files:
- `main.py` - Main bot application
- `firstaid.csv` - Medical conditions database  
- `keep_alive.py` - Web server for continuous operation
- `README.md` - Project documentation
- `LICENSE` - MIT license
- `.gitignore` - Git ignore rules
- `.env.example` - Environment variables template

### Create .env.example:
```bash
# Telegram Bot Token from @BotFather
BOT_TOKEN=your_bot_token_here

# Optional: Set to production for less verbose logging  
ENVIRONMENT=development
```

## Step 3: Upload to GitHub

### Option A: Using GitHub Web Interface
1. Go to your new repository
2. Click "uploading an existing file"
3. Drag and drop all project files
4. Commit message: "Initial commit: Dr. Priya Medical Emergency Bot"
5. Click "Commit changes"

### Option B: Using Git Commands (Local)
```bash
git clone https://github.com/yourusername/dr-priya-medical-bot.git
cd dr-priya-medical-bot
# Copy all project files here
git add .
git commit -m "Initial commit: Dr. Priya Medical Emergency Bot"
git push origin main
```

## Step 4: Configure Repository

1. **Add Topics**: medical, telegram-bot, healthcare, india, emergency, ai
2. **Enable Issues**: For bug reports and feature requests
3. **Enable Discussions**: For community support
4. **Add Description**: "🩺 Indian Medical Emergency Assistant Telegram Bot with AI voice guidance"
5. **Set Website**: Your bot's Telegram link

## Step 5: Deploy on Replit

1. Import from GitHub in Replit
2. Set environment variable `BOT_TOKEN`
3. Run the project
4. Enable "Always On" for 24/7 operation

## Files Created:

✅ README.md - Comprehensive project documentation
✅ LICENSE - MIT license with medical disclaimer  
✅ .gitignore - Proper Python/Replit exclusions
✅ SETUP.md - This setup guide

Your repository is ready for GitHub!