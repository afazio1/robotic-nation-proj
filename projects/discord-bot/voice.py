import discord
from discord.ext import commands
import youtube_dl
import os
# from dbQuery import BAN as ban
from timer import time
import asyncio
from crawling_YT import Crawling_YT_Title, Crawling_YT_Comment
from mutagen.mp3 import MP3

client = commands.Bot(command_prefix="!")
queue = list()
url_queue = list()
searched_title = list()
searched_url = list()
timer = time()
now_playing = str()

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
            print("PermissionError occurd while deletion")

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
    def do_both(self, url) :
        self.download_song(url)
        return self.get_title(url)

class Song_player :
    def play_song(self, voice, title) :
        # now_playing = song    #unused variable
        temp = Song()
        # Crawling_YT_Title.
        temp.download_song(title)
        video_title = temp.get_title(title)
        queue.insert(0, video_title)
        Crawling_YT_Title(title)
        url_queue.insert(0, )

        def after_playing(err) :
            if len(queue) > 0 :
                del queue[0]
                next_song = queue[0]
                self.play_song(voice, next_song)
            else :
                msg = 'Playlist is empty'
                return msg

        voice.play(discord.FFmpegPCMAudio("song.mp3"), after = after_playing)

@client.command()
async def q(ctx) :
    buf = str()
    i = 1
    if queue :
        for var in queue :
            buf = buf + '[' + str(i) + ']' + ' ' + var + '\n'
            i += 1
        await ctx.send("Queue list\n{}" .format(buf))
    else :
        await ctx.send("Queue is empty")

@client.command()
async def artist(ctx) :
    import dbQuery
    buf = 'List of artists in DB'
    buf += dbQuery.READ()
    await ctx.send(buf)

@client.command()
async def auto(ctx, name : str = '') :
    if name == '' :
        await ctx.send("Enter Artist name. To see list of artists, enter !artist")
        return
    import fetch_playlist as fetcher
    for var in fetcher.fetch() :
        queue.append(var)
    buf = 'Added song list\n'
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

def youtube_search(ctx, title) :
    global searched_title
    global searched_url
    i = 1
    buf = 'Search Results\n'
    searched_title.clear()
    searched_url.clear()
    searched_title, searched_url = Crawling_YT_Title(title)
    for var in searched_title :
        buf = buf + '[' + str(i) + ']' + ' ' + var + '\n'
        i += 1
    return buf

def play_infinite() :
    if len(queue) > 1 :
        del queue[0]
        del url_queue[0]
        song_manager = Song()
        video_title = song_manager.do_both(url_queue[0])
        queue.append(video_title)
        return True
    else :
        return False

async def song_ended() :
    while any([await timer.end_flag == False]) :
        return
    play_infinite()


@client.command()
async def play(ctx, input : str = '') :
    # global queue                                #queue변수를 local메소드에서 사용하기 위함
    voiceChannel = ctx.author.voice.channel     #메시지 작성자(유저)의 음성채널
    input_is_valid_num = False
    connection_state = False                    #connection_state : 봇이 음성채널에 연결되어있는지 확인하기 위한 변수
    if client.voice_clients :                   #봇이 음성채널에 있으면 connection_state를 True로 변경
        connection_state = True
    
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    try :
        converted_input = int(input)
        if type(converted_input) is not int :
            raise ValueError
        elif converted_input >= 1 and converted_input <= 5 :
            input_is_valid_num = True
            # selection = converted_input
    except ValueError :
        pass
    
    if connection_state is True and not voice.is_playing() :                    #봇이 음성채널에 연결됨 && 음악 재생중이 아님
        if input_is_valid_num is False :                                        #사용자의 메시지가 1부터 5의 값이 아닌 경우, 즉 제목을 입력한 경우 -> input값을 title인자로 넘겨 유튜브 검색 상위 5개 검색결과 가져옴
            await ctx.send('166번 라인')
            buf = youtube_search(ctx, input)
            await ctx.send(buf)
        else :                                                                  #사용자의 메시지가 1부터 5의 값인 경우 -> class Song(기존 파일 삭제, 번호에 맞는 음악 다운로드), method play(재생), nowplaying()
            await ctx.send('170번 라인')
            song_manager = Song()
            queue.clear()
            url_queue.clear()
            player = Song_player()
            player.play_song(voice, searched_url[int(converted_input)-1])
            queue.append('title')   #title 삽입
            url_queue.append('url') #url 삽입

            # voice.play(discord.FFmpegPCMAudio("song.mp3"))
            # timer.set_song_length(MP3("song.mp3").info.length)
            # await song_ended()
            #재활용 대기
            # del queue[0]
            # if queue :
            #     video_title = queue[0]
            #     queue.append(video_title)
            #     voice.play(discord.FFmpegPCMAudio("song.mp3"))
            #     timer.set_song_length(MP3("song.mp3").info.length)
            #     await ctx.send("Now playing : {}" .format(str(queue[0])))
            # else :  #queue is empty
            #     await ctx.send("Queue is empty")
    elif connection_state is True and not voice.is_playing() and not queue :    #봇이 음성채널에 연결됨 && 음악 재생중이 아님 && 큐가 비어있음 -> 음성채널에 연결, 다운로드, 재생, 재생중인 곡 타이틀 알려줌
        if input_is_valid_num is False :                                        #사용자의 메시지가 1부터 5의 값이 아닌 경우, 즉 제목을 입력한 경우 -> input값을 title인자로 넘겨 유튜브 검색 상위 5개 검색결과 가져옴
            await ctx.send('191번 라인')
            youtube_search(ctx, input)
        else :                                                                  #사용자의 메시지가 1부터 5의 값인 경우 -> class Song(기존 파일 삭제, 번호에 맞는 음악 다운로드), connect, method play(재생), nowplaying()
            await ctx.send('194번 라인')
            song_manager = Song()
            video_title = song_manager.do_both(searched_url[converted_input-1])
            queue.clear()
            url_queue.clear()
            # queue.append(video_title)
            

            await voiceChannel.connect()
            player = Song_player()
            player.play_song(voice, searched_url[int(converted_input)-1])
            # voice.play(discord.FFmpegPCMAudio("song.mp3"))
            await ctx.send("Now playing : {}" .format(str(queue[0])))
    elif connection_state is True and not voice.is_playing() and queue :        #봇이 음성채널에 연결됨 && 음악 재생중이 아님 && 큐가 비어있지 않음 -> 큐에서 가져옴, 다운로드, 재생, 재생중인 곡 타이틀 알려줌
        await ctx.send('207번 라인')
        await ctx.send(Crawling_YT_Title(queue[0]))                             #큐의 첫 번째 원소를 Youtube에 검색해 상위 5개의 결과를 메시지로 리턴함
        if input_is_valid_num is False :                                        #사용자의 메시지가 1부터 5의 값이 아닌 경우, 즉 제목을 입력한 경우 -> input값을 title인자로 넘겨 유튜브 검색 상위 5개 검색결과 가져옴
            youtube_search(ctx, input)
            
        else :                                                                  #사용자의 메시지가 1부터 5의 값인 경우 -> class Song(기존 파일 삭제, 번호에 맞는 음악 다운로드), method play(재생), nowplaying()
            await ctx.send('213번 라인')
            song_manager = Song()
            video_title = song_manager.do_both(searched_url[converted_input-1])
            queue.clear()
            url_queue.clear()
            # queue.append(video_title)

            # voice.play(discord.FFmpegPCMAudio("song.mp3"))
            # timer.set_song_length(MP3("song.mp3").info.length)
            player = Song_player()
            player.play_song(voice, searched_url[int(converted_input)-1])
            await ctx.send("Now playing : {}" .format(str(queue[0])))
            # while any([await timer.end_flag == False]) :
            #     pass
            # del queue[0]
            # if queue :
            #     video_title = queue[0]
            #     queue.append(video_title)
            #     voice.play(discord.FFmpegPCMAudio("song.mp3"))
            #     timer.set_song_length(MP3("song.mp3").info.length)
            #     await ctx.send("Now playing : {}" .format(str(queue[0])))
            # else :  #queue is empty
            #     await ctx.send("Queue is empty")
    elif connection_state is True and voice.is_playing() :                      #봇이 음성채널에 연결됨 && 음악 재생중 -> 큐에 추가함
        if input_is_valid_num is False :                                        #사용자의 메시지가 1부터 5의 값이 아닌 경우, 즉 제목을 입력한 경우 -> input값을 title인자로 넘겨 유튜브 검색 상위 5개 검색결과 가져옴
            await ctx.send('237번 라인')
            buf = youtube_search(ctx, input)
            await ctx.send(buf)
        else :                                                                  #사용자의 메시지가 1부터 5의 값인 경우 -> class Song(기존 파일 삭제, 번호에 맞는 음악 다운로드), connect, method play(재생), nowplaying()
            await ctx.send('241번 라인')
            song_manager = Song()
            song_manager.get_title(searched_url[converted_input])
            queue.append(video_title)
            url_queue.append(searched_url[converted_input-1])
    elif connection_state is False :
        queue.clear()
        await voiceChannel.connect()
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if input_is_valid_num is False :                                        #사용자의 메시지가 1부터 5의 값이 아닌 경우, 즉 제목을 입력한 경우 -> input값을 title인자로 넘겨 유튜브 검색 상위 5개 검색결과 가져옴
            await ctx.send('251번 라인')
            buf = youtube_search(ctx, input)
            await ctx.send(buf)
        else :                                                                  #사용자의 메시지가 1부터 5의 값인 경우 -> class Song(기존 파일 삭제, 번호에 맞는 음악 다운로드), connect, method play(재생), nowplaying()
            await ctx.send('268번 라인')
            print('converted_input', converted_input)
            song_manager = Song()
            song_manager.get_title(searched_url[converted_input])
            queue.append(video_title)

            player = Song_player()
            player.play_song(voice, searched_url[int(converted_input)])
            await ctx.send("Now playing : {}" .format(str(queue[0])))


# @client.command()
# async def newplay(ctx, url : str):
#     voiceChannel = ctx.author.voice.channel
    
#     connection_state = False
#     # if client.voice_clients :
#     #     connection_state = True
    
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
#     if connection_state is True and not voice.is_playing() :    #기존 파일 삭제, 다운로드, 재생, nowplaying()
#         song_manager = Song()
#         song_manager.download_song(url)
#         video_title = song_manager.get_title(url)
#         voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#         voice.play(discord.FFmpegPCMAudio("song.mp3"))
#         queue.append(video_title)
#         await ctx.send("Now playing : {}" .format(str(queue[0]))) 
#     elif connection_state is True and voice.is_playing() :
#         song_manager = Song()
#         new_song_title = song_manager.get_title(url)
#         queue.append(new_song_title)
#         await ctx.send("Now playing : {}" .format(str(queue[0])))
#         await ctx.send("Added new song : {}" .format(new_song_title))
#     elif connection_state is False :                            #음성채널 연결, 다운로드, 재생
#         await voiceChannel.connect()
#         voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#         song_manager = Song()
#         song_manager.download_song(url)
#         video_title = song_manager.get_title(url)
#         voice.play(discord.FFmpegPCMAudio("song.mp3"))
#         queue.append(video_title)
#         await ctx.send("Now playing : {}" .format(str(queue[0])))
    

@client.command()
async def nowplaying(ctx) :
    if queue :
        await ctx.send("Now playing : {}" .format(str(queue[0])))
    else :
        await ctx.send("Queue is empty")

# @client.command()
# async def play(ctx, url : str):
#     song_there = os.path.isfile("song.mp3")
#     try:
#         if song_there:
#             os.remove("song.mp3")
#     except PermissionError:
#         await ctx.send("Wait for the current playing music to end or use the 'stop' command")
#         return

#     # voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
#     voiceChannel = ctx.author.voice.channel
#     await voiceChannel.connect()
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#     }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])
#         info_dict = ydl.extract_info(url, download=False)
#         video_title = info_dict.get('title', None)
#         queue.append(video_title)
#     for file in os.listdir("./"):
#         if file.endswith(".mp3"):
#             os.rename(file, "song.mp3")
#     voice.play(discord.FFmpegPCMAudio("song.mp3"))
#     nowplaying(ctx)


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if client.voice_clients :
        await voice.disconnect()
        os.remove("song.mp3")
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
    def chk_user(chk):
        return ctx.author == chk.author

    if len(yt_id)>10:
        yt_id, yt_comment, yt_like = yt_id[:10], yt_comment[:10], yt_like[:10]

    if url.find("youtube.com/watch"):
        emb = discord.Embed(title="TOP 10 Comments",description="This is comment about {}".format(url),color=discord.Color.blue())
        emb.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        for i in range(len(yt_id)):
            emb.add_field(name="{} (🧡{})".format(yt_id[i], yt_like[i]), value="{}".format(yt_comment[i]),inline=False)
        if len(yt_id)==0:
            emb.add_field(name="Error or No comment", value="Please check the url")
        await ctx.send(embed=emb)

    else:
        titles, hrefs = Crawling_YT_Title(str)
        emb1 = discord.Embed(title="Select the title", description = "Typing the number", color=discord.Color.dark_blue())
        for i in range(len(titles)):
            emb1.add_field(name="{}번".format(i), value="{}".format(titles[i]), inline=False)

        await ctx.send(embed=emb1)

        emb2 = discord.Embed(title="", description="" ,color=discord.Color.dark_blue())
        try:
            tmp = await client.wait_for('message', timeout=30.0, check = chk_user)
        except asyncio.TimeoutError:
            emb.add_field(name="Time out", value="처음부터 다시 입력해주세요")
            ctx.send(embed=emb)
            return
        else:
            pass

        

client.run('Song_player')    #YOUR_TOKEN