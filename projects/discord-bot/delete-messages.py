import discord

client = discord.Client()

@client.event
async def on_message(message):
    if str(message.channel) == "general" and message.content != "":
        await message.channel.purge(limit=1)




client.run('YOUR_TOKEN') # copy your token from the developer portal

# If you wish to securely hide your token, you can do so in a .env file.
# 1. Create a .env in the same directory as your Python scripts
# 2. In the .env file format your variables like this: VARIABLE_NAME=your_token_here
# 3. In Python, you can read a .env file using this syntax:
# token = os.getenv(VARIABLE_NAME)