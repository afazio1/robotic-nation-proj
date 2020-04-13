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
