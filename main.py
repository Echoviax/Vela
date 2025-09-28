import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print("ERROR: 'TOKEN' not found in .env file!")
    print("Please create a .env file and add a token.")
    exit()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'-> Logged in as {client.user}')
    print(f'-> I am in {len(client.guilds)} server(s).')
    await client.change_presence(activity=discord.Game(name="Learning..."))

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