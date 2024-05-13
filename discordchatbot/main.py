import discord
import json
from utils import utils
from agents import item_extractor

#Define checklist
class Checklist:
    def __init__(self):
        self.items = []

    async def add_to_checklist(self, message):
        print('adding'+message.content)
        items_to_add = item_extractor.extract_items_from_message(message)  # Extract the content of the message
        self.items.extend(items_to_add)
        await message.channel.send(f"Added '{items_to_add}' to the checklist.")

    def save_checklist(self, filename='checklist.json'):
        with open(filename, 'w') as file:
            json.dump(self.items, file)

    def load_checklist(self, filename='checklist.json'):
        try:
            with open(filename, 'r') as file:
                self.items = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, initialize an empty checklist
            self.items = []

    async def show_checklist(self, message):
        print('showing'+message.content)
        await message.channel.send(self.items)


my_checklist = Checklist()

config = utils.initiate_config()
# Retrieve config details
discord_config = config['DISCORD']
BOT_TOKEN = discord_config['TOKEN']

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        response = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(response)

    if 'add' in message.content:
        response = await my_checklist.add_to_checklist(message)
        await message.channel.send(response)

    if 'show' in message.content:
        response = await my_checklist.show_checklist(message)
        await message.channel.send(response)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    my_checklist.load_checklist()


async def on_disconnect():
    # Save checklist data before shutting down the bot
    my_checklist.save_checklist()


client.run(BOT_TOKEN)
