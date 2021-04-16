import discord
import requests

client = discord.Client()

key = "YOUR_API_KEY"
channelId = "UCdNnHNkhaRYr-3nhQqY7_dw"



@client.event
async def on_message(message):

    if str(message.author) == "elytra.f#3331" and message.content.startswith("$roboticnation"):
        r = requests.get(
            'https://www.googleapis.com/youtube/v3/search?key=' + key + '&channelId=' + channelId + '&part=snippet,id&order=date&maxResults=1')
        json_data = r.json()
        videoId = json_data["items"][0]["id"]["videoId"]
        await message.channel.purge(limit=1)
        await message.channel.send("Hey @everyone, go check out Robotic Nation's latest video!\n"
                                  + "https://youtu.be/" + videoId)
        print(videoId)




client.run('YOUR_TOKEN')

# If you wish to securely hide your token, you can do so in a .env file.
# 1. Create a .env in the same directory as your Python scripts
# 2. In the .env file format your variables like this: VARIABLE_NAME=your_token_here
# 3. In Python, you can read a .env file using this syntax:
# token = os.getenv(VARIABLE_NAME)
