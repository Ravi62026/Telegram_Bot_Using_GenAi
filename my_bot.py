from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import logging
import openai
import huggingface_hub

from transformers import Conversation, pipeline

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# GEMINI_API = os.getenv("GEMINI_API")


# Connect with huggingface hub

# huggingface_hub.api_key = HUGGINGFACE_API_KEY

openai.api_key = OPENAI_API_KEY

print("ok")

# MODEL_NAME = "google/gemma-7b"

MODEL_NAME = "gpt-3.5-turbo"

# initialize bot

bot = Bot(token=TOKEN)

# initialize dispatcher

dispatcher = Dispatcher(bot)

# configure logging

logging.basicConfig(level=logging.INFO)

# to remember my previous response
class Reference:
    def __init__(self) -> None:
        self.response = ""  # initially set to empty string

reference = Reference()

# conversation buffer memory in lang chain

def clear_past():
    reference.response = ""
    
# message handler decorator

@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """This will return echo message

    Args:
        message (types.Message): _description_
    """
    
    await message.reply("Hi\nI am a Chat Bot! Created by Ravi Shankar. How can i assist you?") 
  
# helper function to generate response

@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm a bot created by Ravi Shankar! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)

@dispatcher.message_handler()
async def main_bot(message: types.Message):
    """
    A handler to process the user's input and generate a response using the openai API.
    """

    print(f">>> USER: \n\t{message.text}")

    response = openai.ChatCompletion.create(
        model = MODEL_NAME,
        messages = [
            {"role": "assistant", "content": reference.response}, # role assistant
            {"role": "user", "content": message.text} #our query 
        ]
    )
    
    reference.response = response['choices'][0]['message']['content']
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)

# using hugginface_hub

# @dispatcher.message_handler()
# async def process_message(message, reference, bot):
#     # Define your Hugging Face model name or path
#     MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"

#     # Initialize the chat pipeline
#     chat_pipeline = pipeline("conversational", model=MODEL_NAME)

#     # Print user's query
#     print(f">>> USER: \n\t{message.text}")

#     # Create a conversation object
#     conversation = Conversation()

#     # Add assistant's response
#     conversation.add_user_input(reference.response, role="assistant")

#     # Add user's query
#     conversation.add_user_input(message.text, role="user")

#     # Generate response using the Hugging Face model
#     response = chat_pipeline([conversation])

#     # Access the generated response
#     generated_response = response[0]["generated_responses"][0]["text"]

#     # Update reference.response
#     reference.response = generated_response

#     # Print chatGPT's response
#     print(f">>> chatGPT: \n\t{reference.response}")

#     # Send the response to the user
#     await bot.send_message(chat_id=message.chat.id, text=reference.response)

    

if __name__ == '__main__':
    executor.start_polling(dispatcher ,skip_updates=True)