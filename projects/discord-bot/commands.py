import discord

from discord.ext import commands

client = commands.Bot(command_prefix="!")

@client.command()
async def hello(ctx, arg):
    print(ctx.author)
    print(ctx.message)
    print(ctx.guild)



client.run('YOUR_TOKEN')

# If you wish to securely hide your token, you can do so in a .env file.
# 1. Create a .env in the same directory as your Python scripts
# 2. In the .env file format your variables like this: VARIABLE_NAME=your_token_here
# 3. At the top of the Python script, import os
# 4. In Python, you can read a .env file using this syntax:
# token = os.getenv(VARIABLE_NAME)