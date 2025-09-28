import discord
import os
from dotenv import load_dotenv

from markov_model import MarkovModel

load_dotenv()
TOKEN = os.getenv('TOKEN')

SAVE_INTERVAL = 5
message_counter = 0

if not TOKEN:
    print("ERROR: 'TOKEN' not found in .env file!")
    print("Please create a .env file and add a token.")
    exit()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)
model = MarkovModel()

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
        # Save to a local database
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