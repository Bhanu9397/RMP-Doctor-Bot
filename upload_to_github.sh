#!/bin/bash

echo "🩺 Dr. Priya Medical Bot - GitHub Upload Helper"
echo "=============================================="

# Check if repository exists
REPO_URL="https://github.com/Bhanu9397/TelegramBotAssistant"

echo "Step 1: Checking repository..."
curl -s -o /dev/null -w "%{http_code}" $REPO_URL | grep -q "200"
if [ $? -eq 0 ]; then
    echo "✅ Repository exists at $REPO_URL"
else
    echo "❌ Repository not found. Please create it first at:"
    echo "   https://github.com/new"
    echo "   Name: TelegramBotAssistant"
    exit 1
fi

echo ""
echo "Step 2: Files ready for upload:"
echo "📄 main.py - $(wc -l < main.py) lines"
echo "📄 firstaid.csv - $(wc -l < firstaid.csv) conditions"
echo "📄 keep_alive.py - $(wc -l < keep_alive.py) lines"
echo "📄 README.md - Project documentation"
echo "📄 LICENSE - MIT license"
echo "📄 .gitignore - Git exclusions"
echo "📄 .env.example - Environment template"

echo ""
echo "Step 3: Manual upload instructions:"
echo "1. Go to: $REPO_URL"
echo "2. Click 'uploading an existing file'"
echo "3. Upload these files in order:"
echo "   - main.py"
echo "   - firstaid.csv" 
echo "   - keep_alive.py"
echo "   - README.md"
echo "   - LICENSE"
echo "   - .gitignore"
echo "   - .env.example"
echo ""
echo "4. Commit message: 'Initial commit: Dr. Priya Medical Emergency Bot'"
echo "5. Click 'Commit changes'"

echo ""
echo "🎉 Your medical bot will be live on GitHub!"