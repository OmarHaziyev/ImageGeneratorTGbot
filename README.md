# Image Generator Telegram Bot

## Overview
This project is a Telegram bot that uses an AI image generation API (Stability AI) to create images based on user prompts. Users interact with the bot by providing text prompts, specifying the number of images they want, and receiving generated images directly in the chat. The bot also tracks users by storing their Telegram usernames and IDs in a database.

---

## Features
- Responds to `/start` command with a welcome message and instructions.
- Accepts user-provided prompts for generating images.
- Allows users to specify the number of images (1 to 3).
- Validates input for both prompts and number of images.
- Uses the Stability AI API to generate high-quality images.
- Provides the option to submit new prompts after image generation.
- Stores user information (Telegram username and ID) in an SQLite database.

---

## How It Works
1. **Start Interaction**: Users initiate the bot with the `/start` command.
2. **Provide Prompt**: The bot asks users to send a text prompt for the image.
3. **Specify Image Count**: Users specify how many images (1 to 3) they want.
4. **Generate Images**: The bot fetches images from Stability AI and sends them to the user.
5. **Repeat or End**: After generating images, the bot prompts the user to send another prompt if they wish to generate more images.

---

## Technologies Used
- **Python**: Core programming language.
- **Telebot Library**: For handling Telegram bot interactions.
- **Requests Library**: For making API requests to Stability AI.
- **Pillow**: For processing and handling images.
- **SQLite**: For storing user information.
- **dotenv**: For managing environment variables securely.

---

## Prerequisites
1. Python 3.7 or higher.
2. A Telegram Bot Token. [Get one from BotFather](https://core.telegram.org/bots#botfather).
3. A Stability AI API key. [Get it from Hugging Face](https://huggingface.co/).
4. SQLite installed on your machine (optional for viewing `.db` files).

---

## Setup Instructions
1. Clone the repository.
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project directory and add the following:
   ```env
   BOT_TOKEN=<your-telegram-bot-token>
   HUGGINGFACE_TOKEN=<your-stability-ai-token>
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

---

## File Structure
- **bot.py**: Main file containing bot logic and interactions.
- **sqlite_manager.py**: Handles SQLite database operations.
- **users.db**: SQLite database file storing Telegram user data.
- **requirements.txt**: Lists project dependencies.
- **README.md**: Project documentation (this file).

---

## How to Use
1. Start the bot by sending `/start` in Telegram.
2. Follow the bot's instructions:
   - Provide a text prompt (e.g., "A futuristic city in the clouds").
   - Specify the number of images (1 to 5).
3. Receive the generated images directly in the chat.
4. To generate more images, simply send another prompt.

---

## Error Handling
- **Invalid Prompts**: The bot will ask the user to provide a valid prompt if the input is too short or empty.
- **Invalid Image Count**: The bot ensures the number of images is between 1 and 5, asking for correction if necessary.
- **API Errors**: Any issues with Stability AI are logged, and the user is notified.
- **Database Errors**: Issues with SQLite are logged, ensuring the bot remains functional.

---

## Future Enhancements
- Add support for additional AI models.
- Allow users to customize image resolution or style.
- Provide a web interface for managing the bot.
- Enhance database features for analytics and reporting.

---

## License
This project is licensed under the MIT License. Feel free to use and modify it as needed.

