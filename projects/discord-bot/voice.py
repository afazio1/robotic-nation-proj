import discord
from discord.ext import commands
import youtube_dl
import os
from crawling_YT import Crawling_YT_Title, Crawling_YT_Comment

client = commands.Bot(command_prefix="!")
queue = list()
comment_chk = False

class Song :
    def __init__(self) :
        ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
        }
        self.ydl_opts = ydl_opts
    def download_song(self, url) :
        song_there = os.path.isfile("song.mp3")
        try :
            if song_there :
                os.remove("song.mp3")
        except PermissionError:
            return

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
    def get_title(self, url) :
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
        return video_title

@client.command()
async def auto(ctx) :
    import fetch_playlist as fetcher
    for var in fetcher.fetch() :
        queue.append(var)
    buf = 'Added song list'
    i = 1
    for var in queue :
        buf = buf + '[' + str(i) + ']' + ' ' + var + '\n'
        i += 1
    await ctx.send(buf)

@client.command()
async def is_connected(ctx) :
    if client.voice_clients :
        await ctx.send("State : connected")
    else :
        await ctx.send("State : not connected")

@client.command()
async def newplay(ctx, url : str):
    voiceChannel = ctx.author.voice.channel
    
    connection_state = False
    # if client.voice_clients :
    #     connection_state = True
    
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    if connection_state is True and not voice.is_playing() :    #기존 파일 삭제, 다운로드, 재생, nowplaying()
        song_manager = Song()
        song_manager.download_song(url)
        video_title = song_manager.get_title(url)
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        queue.append(video_title)
        await ctx.send("Now playing : {}" .format(str(queue[0]))) 
    elif connection_state is True and voice.is_playing() :
        song_manager = Song()
        new_song_title = song_manager.get_title(url)
        queue.append(new_song_title)
        await ctx.send("Now playing : {}" .format(str(queue[0])))
        await ctx.send("Added new song : {}" .format(new_song_title))
    elif connection_state is False :                            #음성채널 연결, 다운로드, 재생
        await voiceChannel.connect()
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        song_manager = Song()
        song_manager.download_song(url)
        video_title = song_manager.get_title(url)
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        queue.append(video_title)
        await ctx.send("Now playing : {}" .format(str(queue[0])))
    

@client.command()
async def nowplaying(ctx) :
    if queue :
        await ctx.send("Now playing : {}" .format(str(queue[0])))
    else :
        await ctx.send("Queue is empty")

@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    # voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    voiceChannel = ctx.author.voice.channel
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
        queue.append(video_title)
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    nowplaying(ctx)


@client.command()
async def leave(ctx):
    # voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    # if voice.is_connected():
    #     await voice.disconnect()
    # else:
    #     await ctx.send("The bot is not connected to a voice channel.")

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if client.voice_clients :
        await voice.disconnect()
    else :
        await ctx.send("The bot is not connected to a voice channel.")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

@client.command()
async def comment(ctx, url:str):
    yt_id, yt_comment, yt_like = Crawling_YT_Comment(url)
    if len(yt_id)>10:
        yt_id, yt_comment, yt_like = yt_id[:10], yt_comment[:10], yt_like[:10]
    
    if url.find("youtube.com/watch"):
        emb = discord.Embed(title="TOP 10 Comments",description="This is comment about {}".format(url),color=discord.Color.blue())
        emb.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        for i in range(len(yt_id)):
            emb.add_field(name="{} (🧡{})".format(yt_id[i], yt_like[i]), value="{}".format(yt_comment[i]),inline=False)
        else:
            emb.add_field(name="Error or No comment", value="Please check the url")
        await ctx.send(embed=emb)

    else:
        titles, hrefs = Crawling_YT_Title(str)
        emb = discord.Embed(title="Select the title", description = "Typing the number", color=discord.Color.dark_blue())
        for i in range(len(titles)):
            emb.add_field(name="{}번".format(i), value="{}".format(titles[i]), inline=False)
        comment_queue = True
        await ctx.send(embed=emb)

client.run('Nzk4NDY1MzE4MTEyNDYwODIw.X_1axg.vPkSAskjdOBrW1jo_lhuGKXvxLE')