import discord

client = discord.Client()

@client.event
async def on_message(message):
    if str(message.channel) == "general" and message.content != "":
        await message.channel.purge(limit=1)




client.run('YOUR_TOKEN') # copy your token from the developer portal
