from dotenv import load_dotenv
load_dotenv()

import telebot
import csv
import logging
import os
import io
from gtts import gTTS
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from keep_alive import keep_alive

# Configure logging
logging.basicConfig(
    filename='first_aid_bot.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

# Also log to console for Replit monitoring
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

# Initialize the Telegram bot with token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logging.error("BOT_TOKEN environment variable not found!")
    raise ValueError("BOT_TOKEN environment variable is required")

bot = telebot.TeleBot(BOT_TOKEN)

# Store user conversation states
user_states = {}

# Load first aid instructions from CSV
def load_csv():
    instructions = []
    csv_file_path = "firstaid.csv"
    
    try:
        with open(csv_file_path, "r", encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            required_fields = ['label', 'scenario', 'adult_instructions', 'child_instructions']
            
            for row in reader:
                if all(field in row and row[field].strip() for field in required_fields):
                    instructions.append({
                        'label': row['label'].strip(),
                        'scenario': row['scenario'].strip(),
                        'adult_instructions': row['adult_instructions'].strip(),
                        'child_instructions': row['child_instructions'].strip()
                    })
                else:
                    logging.warning(f"Skipping invalid row: {row}")
                    
        if not instructions:
            logging.error("No valid rows loaded from CSV. Using fallback data.")
            return get_fallback_data()
            
        logging.info(f"Successfully loaded {len(instructions)} scenarios from CSV")
        
    except FileNotFoundError:
        logging.error(f"CSV file '{csv_file_path}' not found. Using fallback data.")
        return get_fallback_data()
        
    except Exception as e:
        logging.error(f"Error loading CSV: {str(e)}. Using fallback data.")
        return get_fallback_data()
        
    return instructions

def get_fallback_data():
    """Fallback first aid data in case CSV loading fails"""
    return [
        {
            'label': 'burns',
            'scenario': 'Burns',
            'adult_instructions': 'Cool the burn with running water for 10-20 minutes. Remove any jewelry or tight clothing near the burn before swelling occurs. Cover with a clean, non-stick dressing or cling film. Do not apply creams, ice, or butter. Seek immediate medical help if the burn is larger than 3 inches, on the face/hands/feet/genitals, or appears deep.',
            'child_instructions': 'Cool the burn with running water for 10-20 minutes. Remove any jewelry or tight clothing before swelling occurs. Cover with a clean, non-stick dressing. Do not apply creams, ice, or butter. For children, seek medical help immediately for any burn larger than a coin or if the child is in severe pain.'
        },
        {
            'label': 'choking',
            'scenario': 'Choking',
            'adult_instructions': 'If conscious: Encourage coughing. If ineffective, give 5 sharp back blows between shoulder blades. If still choking, perform 5 abdominal thrusts (Heimlich maneuver). Alternate between back blows and abdominal thrusts. Call emergency services immediately.',
            'child_instructions': 'For infants (<1 year): 5 back blows on chest with infant face down, then 5 chest thrusts. For children (>1 year): 5 back blows, then 5 gentle abdominal thrusts. Call emergency services immediately. Never use abdominal thrusts on infants under 1 year.'
        },
        {
            'label': 'bleeding',
            'scenario': 'Severe Bleeding',
            'adult_instructions': 'Apply direct pressure to the wound with a clean cloth or bandage. Maintain pressure and add more layers if blood soaks through. Elevate the injured area above heart level if possible. If bleeding is severe or from an artery, call emergency services immediately. Do not remove embedded objects.',
            'child_instructions': 'Apply gentle but firm pressure with a clean cloth. Keep the injured area elevated if possible. For children, even moderate bleeding can be serious - call emergency services if bleeding doesn\'t stop within 5-10 minutes of direct pressure.'
        },
        {
            'label': 'unconscious',
            'scenario': 'Unconscious Person',
            'adult_instructions': 'Check for responsiveness by shouting and gently shaking shoulders. Check for breathing for 10 seconds. If breathing normally, place in recovery position. If not breathing, begin CPR immediately. Call emergency services. Stay with the person until help arrives.',
            'child_instructions': 'Check for responsiveness by shouting their name and gently tapping. Check for breathing for 10 seconds. If breathing, place in recovery position. If not breathing, begin pediatric CPR. Call emergency services immediately. Children can deteriorate quickly - never leave them alone.'
        }
    ]

# Load instructions on startup
instructions = load_csv()
scenario_list = [instr['scenario'] for instr in instructions]

# Handle the /start command and display scenario buttons
@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name or "User"
    
    user_states[chat_id] = {'state': 'idle'}
    
    # Create keyboard with scenario buttons
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [KeyboardButton(scenario['scenario']) for scenario in instructions]
    
    # Add buttons in rows of 2
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.add(buttons[i], buttons[i + 1])
        else:
            markup.add(buttons[i])
    
    welcome_message = f"🩺 Namaste {user_name}! I'm Dr. Priya, your medical emergency assistant.\n\n" \
                     "As a young practicing physician in India, I'll provide you with immediate " \
                     "clinical guidance using Indian medications and protocols. I cover common " \
                     "medical emergencies with age-specific treatment plans.\n\n" \
                     "Please select a medical condition or describe your emergency:"
    
    bot.send_message(chat_id, welcome_message, reply_markup=markup)
    logging.info(f"User {chat_id} ({user_name}) started bot. Scenarios offered: {len(scenario_list)}")

# Handle scenario button clicks
@bot.message_handler(func=lambda message: message.text in scenario_list)
def handle_scenario(message):
    chat_id = message.chat.id
    scenario_name = message.text
    
    user_states[chat_id] = {'state': 'awaiting_age', 'scenario': scenario_name}
    
    age_message = f"📋 **Selected Condition: {scenario_name}**\n\n" \
                  "Please provide the patient's age for age-specific clinical protocols (e.g., 25, 5, 67):"
    
    bot.send_message(chat_id, age_message, parse_mode='Markdown')
    logging.info(f"User {chat_id} selected scenario: {scenario_name}")

# Handle user input
@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_text(message):
    chat_id = message.chat.id
    user_input = message.text.strip()
    
    # Initialize user state if not exists
    if chat_id not in user_states:
        user_states[chat_id] = {'state': 'idle'}

    # Handle age input
    if user_states[chat_id]['state'] == 'awaiting_age':
        try:
            age = int(user_input)
            
            if age < 0 or age > 120:
                bot.send_message(chat_id, "⚠️ Please enter a valid age between 0 and 120.")
                return
            
            scenario = user_states[chat_id]['scenario']
            
            # Find the matching instruction
            for instr in instructions:
                if instr['scenario'] == scenario:
                    # Determine which instructions to use based on age
                    if age >= 16:
                        response = instr['adult_instructions']
                        age_category = "Adult"
                    else:
                        response = instr['child_instructions']
                        age_category = "Child/Infant"
                    
                    # Format the response message with Indian medical persona
                    doctor_intro = "Dr. Priya here! Let me guide you through this emergency:"
                    
                    response_message = f"🩺 **{scenario} - {age_category} Treatment Protocol**\n\n" \
                                     f"{doctor_intro}\n\n" \
                                     f"**Immediate Care Steps:**\n{response}\n\n" \
                                     f"⚠️ **Important:** Call 102 (ambulance) or rush to nearest hospital for severe cases. " \
                                     f"These are standard Indian medical protocols. Always check for drug allergies before giving medications.\n\n" \
                                     f"💊 **Medications mentioned are commonly available in India. Consult your family doctor for follow-up care.**\n\n" \
                                     f"Type /start for other conditions. Stay safe!"
                    
                    bot.send_message(chat_id, response_message, parse_mode='Markdown')
                    
                    # Generate voice response
                    try:
                        voice_text = f"Hello! Dr. Priya here. For {scenario} in {age_category.lower()}, {response}"
                        # Clean text for TTS
                        clean_voice_text = voice_text.replace('*', '').replace('_', '').replace('`', '')
                        clean_voice_text = clean_voice_text.replace('>', '').replace('<', '').replace('#', '')
                        
                        # Generate TTS with Indian English accent and female voice
                        tts = gTTS(text=clean_voice_text, lang='en', tld='co.in', slow=False)
                        
                        # Save to BytesIO buffer
                        audio_buffer = io.BytesIO()
                        tts.write_to_fp(audio_buffer)
                        audio_buffer.seek(0)
                        
                        # Send voice message
                        bot.send_voice(chat_id, audio_buffer, caption="🎤 Dr. Priya's voice guidance")
                        logging.info(f"Voice message sent for {scenario}")
                        
                    except Exception as e:
                        logging.error(f"Voice generation failed: {str(e)}")
                        bot.send_message(chat_id, "🎤 Voice guidance temporarily unavailable, but text instructions are complete!")
                    
                    logging.info(f"User {chat_id} provided age {age} for {scenario}, received {age_category} instructions")
                    break
            
            # Reset user state
            user_states[chat_id]['state'] = 'idle'
            
        except ValueError:
            bot.send_message(
                chat_id, 
                "❌ Please enter a valid age as a number (e.g., 25, 5, 67).\n\n"
                "If you want to start over, type /start"
            )
            logging.warning(f"User {chat_id} provided invalid age: {user_input}")
    
    # Handle scenario search
    else:
        scenario_search = user_input.lower().strip()
        found = False
        
        # Search for matching scenarios
        for instruction in instructions:
            scenario_lower = instruction['scenario'].lower()
            label_lower = instruction['label'].lower()
            
            if (scenario_search in scenario_lower or 
                scenario_search in label_lower or
                any(word in scenario_lower for word in scenario_search.split())):
                
                user_states[chat_id] = {'state': 'awaiting_age', 'scenario': instruction['scenario']}
                
                match_message = f"✅ Found match: **{instruction['scenario']}**\n\n" \
                               f"Please enter your age or the age of the person who needs help (e.g., 25, 5, 67):"
                
                bot.send_message(chat_id, match_message, parse_mode='Markdown')
                logging.info(f"User {chat_id} input '{scenario_search}' matched '{instruction['scenario']}'")
                found = True
                break
        
        if not found:
            # Create keyboard with available scenarios
            markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            buttons = [KeyboardButton(scenario['scenario']) for scenario in instructions]
            
            for i in range(0, len(buttons), 2):
                if i + 1 < len(buttons):
                    markup.add(buttons[i], buttons[i + 1])
                else:
                    markup.add(buttons[i])
            
            no_match_message = f"❌ No match found for '{user_input}'.\n\n" \
                              f"Please select from the available first aid scenarios below:"
            
            bot.send_message(chat_id, no_match_message, reply_markup=markup)
            logging.info(f"User {chat_id} input '{scenario_search}' - no match found")

# Handle /help command
@bot.message_handler(commands=['help'])
def handle_help(message):
    chat_id = message.chat.id
    
    help_message = "🩺 **Medical Emergency Assistant Help**\n\n" \
                  "**Commands:**\n" \
                  "• /start - Display available medical conditions\n" \
                  "• /help - Show this help information\n\n" \
                  "**Usage Protocol:**\n" \
                  "1. Select a medical condition or describe symptoms\n" \
                  "2. Provide patient age for age-specific protocols\n" \
                  "3. Receive evidence-based clinical guidelines\n\n" \
                  "**Available Conditions:**\n"
    
    for i, instruction in enumerate(instructions, 1):
        help_message += f"{i}. {instruction['scenario']}\n"
    
    help_message += "\n⚠️ **Clinical Disclaimer:** This system provides evidence-based emergency protocols. " \
                   "For life-threatening emergencies, contact emergency services (911/112) immediately. " \
                   "Always verify current medications and allergies before administering treatment."
    
    bot.send_message(chat_id, help_message, parse_mode='Markdown')
    logging.info(f"User {chat_id} requested help")

# Handle all other messages
@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    chat_id = message.chat.id
    
    other_message = "🤖 Welcome to the First Aid Bot!\n\n" \
                   "Use /start to see available first aid scenarios.\n" \
                   "Use /help for more information."
    
    bot.send_message(chat_id, other_message)
    logging.info(f"User {chat_id} sent unhandled message: {message.text}")

# Error handler
@bot.message_handler(func=lambda message: True, content_types=['photo', 'video', 'document', 'audio', 'voice', 'sticker'])
def handle_media(message):
    chat_id = message.chat.id
    
    media_message = "📎 I can only process text messages.\n\n" \
                   "Please type /start to see first aid scenarios or type your emergency situation."
    
    bot.send_message(chat_id, media_message)
    logging.info(f"User {chat_id} sent media content")

def main():
    """Main function to run the bot"""
    logging.info("First Aid Bot starting up...")
    
    # Test bot connection
    try:
        bot_info = bot.get_me()
        logging.info(f"Bot connected successfully: @{bot_info.username}")
    except Exception as e:
        logging.error(f"Failed to connect to Telegram: {str(e)}")
        raise
    
    # Keep the web server alive for Replit
    keep_alive()
    
    # Start polling
    logging.info("Bot polling started...")
    
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=60)
        except Exception as e:
            logging.error(f"Bot polling failed: {str(e)}")
            logging.info("Restarting bot in 5 seconds...")
            import time
            time.sleep(5)
            continue

if __name__ == "__main__":
    main()
