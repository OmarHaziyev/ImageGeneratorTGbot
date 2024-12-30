from dotenv import load_dotenv
import os
import telebot
import requests
import io
import threading
import logging
from time import sleep
from PIL import Image
import random  # Import random for generating unique seeds
from sqlite_manager import add_user  # Import database functions

load_dotenv()

# Configure logging
logging.basicConfig(filename="bot_errors.log", level=logging.ERROR, format="%(asctime)s - %(message)s")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large"
BOT_TOKEN = os.getenv('BOT_TOKEN')
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

# Store user states
user_states = {}


# Query Hugging Face API
def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)  # 60-second timeout
        if response.status_code != 200:
            error_message = f"API Error {response.status_code}: {response.text}"
            logging.error(error_message)
            return None, "Sorry, I couldn't generate the image. Please try again."
        return response.content, None
    except requests.exceptions.Timeout:
        logging.error("API request timed out.")
        return None, "The request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        logging.error(f"Network Error: {e}")
        return None, "Network error occurred. Please try again."


# Persistent typing action
def send_typing_action(chat_id):
    while threading.current_thread().keep_running:
        bot.send_chat_action(chat_id=chat_id, action="typing")
        sleep(3)  # Send typing action every 3 seconds


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Fetch username and Telegram ID
    username = message.from_user.username
    telegram_id = message.from_user.id

    # Handle missing username
    if not username:
        username = "<No Username>"

    # Add user to the database
    try:
        add_user(username, telegram_id)
    except Exception as e:
        logging.error(f"Error adding user to database: {e}")
        bot.reply_to(message, "Sorry, there was an issue saving your data. Please try again later.")
        return

    # Welcoming message
    welcome_text = (
        "🎉 *Welcome to the Image Generator Bot!* 🎉\n\n"
        "Here’s how you can use me:\n"
        "1️⃣ Use the /start command to begin interacting with me.\n"
        "2️⃣ Send me a text prompt describing the image you want to generate.\n"
        "3️⃣ I’ll ask how many images you want (up to 3) and generate them for you!\n\n"
        "💡 *Example Prompt*: `A futuristic city in the clouds`\n\n"
        "⚡ *Pro Tip*: The more creative your prompt, the better the image!\n\n"
        "Let’s get started! 🚀"
    )

    bot.reply_to(message, welcome_text, parse_mode="Markdown")


@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id

    if chat_id not in user_states or 'prompt' not in user_states[chat_id]:
        # Handle a new prompt
        if not message.text.strip():
            bot.reply_to(message, "Please enter a valid prompt.")
            return
        if len(message.text.strip()) < 5:
            bot.reply_to(message, "Your prompt is too short. Please provide more details.")
            return
        if len(message.text.strip()) > 200:
            bot.reply_to(message, "Your prompt is too long. Please shorten it to under 200 characters.")
            return

        # Store the prompt and ask for the number of images
        user_states[chat_id] = {'prompt': message.text.strip()}
        bot.reply_to(message, "How many images would you like to generate?")

    elif 'num_images' not in user_states[chat_id]:
        # Handle the number of images input
        try:
            num_images = int(message.text)
            if num_images < 1 or num_images > 3:  # More than 3 takes TOO MUCH time
                bot.reply_to(message, "Please enter a number between 1 and 3.")
                return
            user_states[chat_id]['num_images'] = num_images
        except ValueError:
            bot.reply_to(message, "Please enter a valid number.")
            return

        # Retrieve the stored prompt and number of images
        prompt = user_states[chat_id]['prompt']
        num_images = user_states[chat_id]['num_images']

        # Start typing animation
        typing_thread = threading.Thread(target=send_typing_action, args=(chat_id,))
        typing_thread.keep_running = True
        typing_thread.start()

        images = []
        for _ in range(num_images):
            # Add a unique random seed to the payload
            seed = random.randint(0, 2 ** 32 - 1)  # Generate a random seed
            image_bytes, error = query({
                "inputs": prompt,
                "options": {"seed": seed},  # Pass the seed in the payload
            })
            if error:
                bot.reply_to(message, error)
                typing_thread.keep_running = False
                typing_thread.join()
                del user_states[chat_id]
                return

            # Convert the image bytes to a PIL image
            image = Image.open(io.BytesIO(image_bytes))

            # Save the image to an in-memory byte stream
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            images.append(img_byte_arr)

        # Stop typing animation
        typing_thread.keep_running = False
        typing_thread.join()

        # Send all images to the user
        for i, img in enumerate(images, start=1):
            bot.send_photo(chat_id=chat_id, photo=img, caption=f"Image {i} for: {prompt}")

        # Clear user state and prompt for a new input
        bot.reply_to(message, "If you want another image, give another prompt. Else you can just leave the session.")
        del user_states[chat_id]


# Start the bot
bot.infinity_polling()
