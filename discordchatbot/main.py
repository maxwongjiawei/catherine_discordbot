import discord
import json
from utils import utils
from agents import item_extractor

config = utils.initiate_config()
# Retrieve config details
discord_config = config['DISCORD']
BOT_TOKEN = discord_config['TOKEN']
openai_config = config['OPENAI']

item_llm = utils.initiate_item_llm(openai_config['ITEM_EXTRACTOR_LLM'])

client = discord.Client(intents=discord.Intents.default())


#Define checklist
class Checklist:
    def __init__(self):
        self.items = []

    def add_to_checklist(self, message):
        print('adding ' + message.content)
        items_to_add = item_extractor.extract_items_from_message(item_llm,
                                                                 message.content)  # Extract the content of the message
        self.items.extend(items_to_add)
        reply_message = f"Added '{items_to_add.name}' to the checklist."
        return reply_message

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
        print('showing' + message.content)
        await message.channel.send(self.items)


my_checklist = Checklist()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        response = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(response)

    if 'add' in message.content:
        response = my_checklist.add_to_checklist(message)
        await message.channel.send(response)

    if 'show' in message.content:
        response = await my_checklist.show_checklist(message)


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
