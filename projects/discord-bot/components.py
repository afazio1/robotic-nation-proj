# install and import discord and discord_components

import discord
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select
import discord.ext.commands as commands

# set up the client

client = commands.Bot("!")
DiscordComponents(client)

# send a message with Button components
# involve some attributes
# recieve an interaction

@client.command()
async def hello(ctx):
    await ctx.send("hello", components = [
        [Button(label="Hi", style="3", emoji = "🥴", custom_id="button1"), Button(label="Bye", style="4", emoji = "😔", custom_id="button2")]
        ])
    interaction = await client.wait_for("button_click", check = lambda i: i.custom_id == "button1")
    await interaction.send(content = "Button clicked!", ephemeral=False)


# send a message with a Select component
# recieve an interaction
# scan for interaction in while loop

@client.command()
async def select(ctx):
    await ctx.send("Select", components = [
        Select(
            placeholder = "Select something!",
            options = [
                SelectOption(label="A", value="A"),
                SelectOption(label="B", value="B")
            ]
        )
    ])

    while True:
        try:
            select_interaction = await client.wait_for("select_option")
            await select_interaction.send(content = f"{select_interaction.values[0]} selected!", ephemeral = False)
        except:
            await ctx.send("urmom")
    

client.run('YOUR_TOKEN')


# If you wish to securely hide your token, you can do so in a .env file.
# 1. Create a .env in the same directory as your Python scripts
# 2. In the .env file format your variables like this: VARIABLE_NAME=your_token_here
# 3. At the top of the Python script, import os
# 4. In Python, you can read a .env file using this syntax:
# token = os.getenv(VARIABLE_NAME)




