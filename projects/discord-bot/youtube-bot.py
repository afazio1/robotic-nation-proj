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


