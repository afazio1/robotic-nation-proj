import discord

client = discord.Client()


@client.event
async def on_message(message):
    message.content = message.content.lower()
    if message.author == client.user:
        return
    if message.content.startswith("hello"):

        if str(message.author) == "elytra.f#3331":  # make sure to change to your user name with hash code
            await message.channel.send("Hello " + str(message.author) + "!")
        else:
            await message.channel.send("Hello, I am a test bot.")


client.run('YOUR_TOKEN')  # copy your token from the developer portal

# If you wish to securely hide your token, you can do so in a .env file.
# 1. Create a .env in the same directory as your Python scripts
# 2. In the .env file format your variables like this: VARIABLE_NAME=your_token_here
# 3. In Python, you can read a .env file using this syntax:
# token = os.getenv(VARIABLE_NAME)
