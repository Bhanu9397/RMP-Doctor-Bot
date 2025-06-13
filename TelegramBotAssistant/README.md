# 🩺 Dr. Priya - Indian Medical Emergency Assistant Bot

A comprehensive Telegram bot providing immediate medical emergency guidance with Indian medications and protocols, featuring voice responses from Dr. Priya, a young female Indian physician.

## 🌟 Features

- **53+ Medical Conditions**: Covers common emergencies encountered in Indian clinical practice
- **Age-Specific Protocols**: Separate treatment guidelines for adults and children
- **Indian Medications**: Uses locally available medicines (Crocin, Dolo, Grilinctus, Electral, etc.)
- **Voice Guidance**: AI-generated voice responses with Indian English accent
- **Dr. Priya Persona**: Friendly young female doctor personality
- **24/7 Availability**: Continuous operation on Replit platform
- **Emergency Numbers**: Indian emergency services (102 ambulance)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- Replit account (for hosting)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/dr-priya-medical-bot.git
   cd dr-priya-medical-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   export BOT_TOKEN="your_telegram_bot_token"
   ```

4. **Run the bot**
   ```bash
   python main.py
   ```

## 📱 Usage

1. Start a conversation with your bot on Telegram
2. Send `/start` to see available medical conditions
3. Select a condition or type your emergency
4. Provide the patient's age when prompted
5. Receive both text and voice guidance from Dr. Priya

### Example Interaction
```
User: /start
Bot: 🩺 Namaste! I'm Dr. Priya, your medical emergency assistant...

User: [Selects "Fever"]
Bot: Please provide the patient's age...

User: 25
Bot: 🩺 Fever - Adult Treatment Protocol
Dr. Priya here! Let me guide you through this emergency:
[Detailed instructions with Indian medications]
[Voice message follows]
```

## 🏥 Medical Conditions Covered

### Common Emergencies
- Burns, Choking, Bleeding, Fractures
- Fever, Cough, Common Cold
- Asthma Attack, Allergic Reactions
- Heart Attack, Stroke, Seizures

### Specialized Conditions
- Diabetes Emergency, Hypertension Crisis
- Gastroenteritis, Food Poisoning
- UTI, Kidney Stones, Migraines
- Anxiety Attacks, Substance Overdose

### Pediatric Care
- Age-appropriate dosing guidelines
- Child-specific safety protocols
- Pediatric emergency procedures

## 🛠️ Technical Architecture

### Core Components
- **Telegram Bot API**: Message handling and user interaction
- **CSV Database**: Medical conditions and treatment protocols
- **Text-to-Speech**: Google TTS with Indian English accent
- **Flask Web Server**: Keep-alive functionality for 24/7 operation

### File Structure
```
├── main.py              # Main bot application
├── firstaid.csv         # Medical conditions database
├── keep_alive.py        # Web server for continuous operation
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (template)
└── README.md           # This file
```

## 🇮🇳 Indian Medical Context

### Medications Used
- **Pain Relief**: Crocin, Dolo, Combiflam, Zerodol-P
- **Cough**: Grilinctus, Alex, Tixylix, Chericof
- **Cold**: Cetrizine, Sinarest, Nasivion S
- **Digestive**: Eno, Pudin Hara, Cyclopam, Electral
- **Probiotics**: Vizylac, Econorm

### Emergency Services
- **Ambulance**: 102
- **Police**: 100
- **Fire**: 101

## 🔧 Configuration

### Environment Variables
```bash
BOT_TOKEN=your_telegram_bot_token_from_botfather
```

### Customization
- Edit `firstaid.csv` to add/modify medical conditions
- Adjust age thresholds in `main.py` (currently 16+ for adult protocols)
- Modify voice settings in TTS configuration

## 🚨 Medical Disclaimer

**Important**: This bot provides general medical guidance based on standard protocols. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always:

- Contact emergency services (102) for life-threatening situations
- Verify medication allergies before administration
- Consult healthcare professionals for persistent symptoms
- Follow up with your family doctor

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-condition`)
3. Add medical conditions to `firstaid.csv` following the existing format
4. Test thoroughly with different age groups
5. Submit a pull request

### Medical Content Guidelines
- Use evidence-based protocols
- Include Indian medication names and dosages
- Provide age-specific instructions
- Reference local emergency services

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Medical protocols based on Indian clinical guidelines
- Medication information from CIMS and MIMS India
- Voice synthesis powered by Google Text-to-Speech
- Built with love for the Indian healthcare community

## 📞 Support

- **Telegram**: [@YourBotUsername](https://t.me/QRdeveop_bot)
- **Issues**: [GitHub Issues](https://github.com/yourusername/dr-priya-medical-bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/dr-priya-medical-bot/discussions)

---

**Made with ❤️ for Indian healthcare** | **Always prioritize professional medical care**