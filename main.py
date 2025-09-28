import pickle
import discord
import os
from dotenv import load_dotenv

from markov_model import MarkovModel

load_dotenv()
TOKEN = os.getenv('TOKEN')

MODEL_FILE = 'markov_model.pkl'
SAVE_INTERVAL = 1
message_counter = 0

if not TOKEN:
    print("ERROR: 'TOKEN' not found in .env file!")
    print("Please create a .env file and add a token.")
    exit()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

def load_model():
    try:
        with open(MODEL_FILE, 'rb') as f:
            print("-> Loading existing model...")
            return pickle.load(f)
    except FileNotFoundError:
        print("-> No existing model found, creating a new one.")
        return MarkovModel()
    except Exception as e:
        print(f"Error loading model: {e}. Creating a new one.")
        return MarkovModel()

def save_model(model_to_save):
    try:
        with open(MODEL_FILE, 'wb') as f:
            pickle.dump(model_to_save, f)
            print(f"-> Model saved successfully to {MODEL_FILE}")
    except Exception as e:
        print(f"Error saving model: {e}")

client = discord.Client(intents=intents)
model = load_model()

@client.event
async def on_ready():
    print(f'-> Logged in as {client.user}')
    print(f'-> I am in {len(client.guilds)} server(s).')
    await client.change_presence(activity=discord.Activity(name="You", type=discord.ActivityType.watching))

@client.event
async def on_message(message: discord.Message):
    global message_counter

    if message.author == client.user or message.author.bot:
        return

    model.learn(message.content)
    message_counter += 1

    if message_counter >= SAVE_INTERVAL:
        save_model(model)
        message_counter = 0

    should_speak = client.user.mentioned_in(message)

    if should_speak:
        async with message.channel.typing():
            response = model.generate(max_words=40)
            await message.channel.send(response)

def main():
    try:
        client.run(TOKEN)
    except discord.errors.LoginFailure:
        print("\nERROR: an invalid token has been passed.")
        print("Please make sure your .env file contains the correct TOKEN!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()