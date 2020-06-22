import discord

from discord.ext import commands

client = commands.Bot(command_prefix="!")

@client.command()
async def hello(ctx, arg):
    print(ctx.author)
    print(ctx.message)
    print(ctx.guild)



client.run('YOUR_TOKEN')