import json
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ChatPermissions

# Read bot token from token.txt file
with open('token.txt', 'r') as file:
    TOKEN = file.read().strip()

# Replace 'YOUR_CHANNEL_ID' with the ID of your channel
CHANNEL_ID = '@testcricket11'

# Your channel chat ID
CHANNEL_CHAT_ID = -1001745510608  # Replace with your channel chat ID
 
# List to store users who joined through the bot's invite link
users_joined_through_bot = []

# Define a function to handle the /start command
def start(update, context):
    # Get chat ID
    chat_id = update.effective_chat.id

    # Get user details
    user = update.effective_user

    user_data = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username
    }

    # Check if user already exists in the JSON file
    if not is_user_data_exists(user.id):
        # Append user data if it doesn't already exist
        append_user_data(user_data)

    # Check if chat ID already exists in the JSON file
    if not is_chat_id_exists(chat_id):
        # Append chat ID if it doesn't already exist
        append_chat_id(chat_id)

    # Send a welcome message with an image and a button
    message = "Welcome to the Cricket 11 Assistant! Please click the button below to join our broadcast channel or if you want to contact our support then please leave a message below."
    image_url = "https://imagetolink.com/ib/39cotFZ9cY.png"  # Replace with your image URL
    button_text_join = "Join Channel 🔥"
    button_text_support = "Chat Support 📞"
    button_text_rank = "Book 1st Rank ✅"
    join_button = InlineKeyboardButton(button_text_join, url="https://t.me/+UUbLGbBDKCJkZGI1")  # Replace "YourChannel" with your channel username or invite link
    support_button = InlineKeyboardButton(button_text_support, url="https://t.me/Nice2play")  # New button callback_data='contact_support'
    rank_button = InlineKeyboardButton(button_text_rank, url="https://cricket11team.com")  # Replace "YourChannel" with your channel username or invite link
    reply_markup = InlineKeyboardMarkup([[join_button], [support_button], [rank_button]])

    context.bot.send_photo(chat_id=chat_id, photo=image_url, caption=message, reply_markup=reply_markup)

# Define a function to append user data to user_data.json
def append_user_data(user_data):
    try:
        with open('user_data.json', 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    # Check if user data already exists
    if not any(user['id'] == user_data['id'] for user in existing_data):
        existing_data.append(user_data)

        # Write updated data back to the file
        with open('user_data.json', 'w') as file:
            json.dump(existing_data, file, indent=4)

# Define a function to append chat ID to chat_ids.json
def append_chat_id(chat_id):
    try:
        with open('chat_ids.json', 'r') as file:
            existing_chat_ids = json.load(file)
    except FileNotFoundError:
        existing_chat_ids = []

    # Check if chat ID already exists
    if not any(entry['chat_id'] == chat_id for entry in existing_chat_ids):
        existing_chat_ids.append({"chat_id": chat_id})

        # Write updated data back to the file
        with open('chat_ids.json', 'w') as file:
            json.dump(existing_chat_ids, file, indent=4)

# Define a function to check if chat ID exists in chat_ids.json
def is_chat_id_exists(chat_id):
    try:
        with open('chat_ids.json', 'r') as file:
            existing_chat_ids = json.load(file)
            return any(entry['chat_id'] == chat_id for entry in existing_chat_ids)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

# Define a function to check if user data exists in user_data.json
def is_user_data_exists(user_id):
    try:
        with open('user_data.json', 'r') as file:
            existing_data = json.load(file)
            return any(user['id'] == user_id for user in existing_data)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

def load_chat_ids():
    chat_ids = []
    try:
        with open('chat_ids.json', 'r') as file:
            try:
                existing_data = json.load(file)
                chat_ids = [entry['chat_id'] for entry in existing_data]
            except json.JSONDecodeError:
                # Handle case where the file is empty or not valid JSON
                pass
    except FileNotFoundError:
        # Handle case where the file doesn't exist
        pass
    return chat_ids

# Define a function to handle the /broadcast command
def broadcast(update, context):
    # Get the user ID of the user who sent the command
    user_id = update.effective_user.id

    # Load admin IDs from admins.json file
    admin_ids = load_admin_ids()

    # Check if the user is an admin
    if user_id not in admin_ids:
        update.message.reply_text("You need to be admin to do this.")
        return

    # Get the message to be broadcasted
    if not context.args:
        update.message.reply_text("Please provide a message to broadcast.")
        return

    message = ' '.join(context.args)

    # Load chat IDs from chat_ids.json file
    chat_ids = load_chat_ids()

    # Broadcast message to all users
    for chat_id in chat_ids:
        context.bot.send_message(chat_id=chat_id, text=message)

# Define a function to handle the /userlist command
def user_list(update, context):
    # Get the user ID of the user who sent the command
    user_id = update.effective_user.id

    # Load admin IDs from admins.json file
    admin_ids = load_admin_ids()

    # Check if the user is an admin
    if user_id not in admin_ids:
        update.message.reply_text("You need to be an admin to do this.")
        return

    # Read user data from user_data.json file
    try:
        with open('user_data.json', 'rb') as file:
            # Send the file as a document
            context.bot.send_document(chat_id=update.effective_chat.id, document=file, filename='user_data.json')
    except FileNotFoundError:
        update.message.reply_text("User data file not found.")

# Define a function to handle the contact support button callback
def contact_support(update: Update, context):
    # Get the user ID
    user_id = update.effective_user.id

    # Predefined message to be added
    predefined_message = f"Contact Support: \n\n +91 8153815546 | +91 7622991653 \n\n @Nice2play \n\n OR you can send custom message: \n /msg [your message here]"

    # Send the predefined message directly to the user's typing area
    context.bot.send_message(chat_id=user_id, text=predefined_message)

    # Acknowledge the button click (remove the callback query)
    update.callback_query.answer()

# Define a function to handle the /message command
def send_message(update, context):
    # Get the message sent by the user
    if not context.args:
        update.message.reply_text("Please provide a message to send.")
        return
    message = ' '.join(context.args)

    # Get user details
    user = update.effective_user
    user_details = f"User Details:\nFirst Name: {user.first_name}\nLast Name: {user.last_name}\nUsername: @{user.username}\nUser ID: {user.id}"
    full_message = f"{user_details}\n\n{message}"

    # Forward the message to the channel
    context.bot.send_message(chat_id=CHANNEL_ID, text=full_message)

# Function to handle join requests
def handle_join(update: Update, context: CallbackContext):
    # Check if the user is requesting to join a channel
    if update.message.chat.type == "private" and update.message.chat.title is not None:
        # Approve the join request
        context.bot.send_message(chat_id=update.message.chat_id, text="Your join request has been approved!")
        # Add the user to the channel
        context.bot.add_chat_members(chat_id="-1001745510608", user_ids=[update.message.from_user.id])

# Define a function to load admin IDs from admins.json file
def load_admin_ids():
    admin_ids = []
    try:
        with open('admins.json', 'r') as file:
            admins_data = json.load(file)
            admin_ids = admins_data.get('admins', [])
    except FileNotFoundError:
        pass
    return admin_ids

# List of chat IDs where the bot is available
CHAT_IDS = []  # Add chat IDs here if needed

def main():
    # Create an updater object
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register handler for the /start command
    dp.add_handler(CommandHandler("start", start))

    # Register handler for the /broadcast command
    dp.add_handler(CommandHandler("broadcast", broadcast, pass_args=True))

    # Register handler for the /message command
    dp.add_handler(CommandHandler("msg", send_message, pass_args=True))

    # Register handler for the /userlist command
    dp.add_handler(CommandHandler("userlist", user_list))

    # Register the contact support button callback
    dp.add_handler(CallbackQueryHandler(contact_support, pattern='contact_support'))

    # Register the handler for join requests
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, handle_join))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
